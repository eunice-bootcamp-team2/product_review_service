import hashlib

from apps.crawling.services.repository import upsert_raw_data
from django.db import transaction
from django.utils import timezone


def make_hash(value: str) -> str:
    """
    문자열을 SHA256 해시값으로 변환합니다.
    """
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_page_info_unique_key(target) -> str:
    raw = f"{target.site}:page_info:{target.url}"
    return make_hash(raw)


def build_candidate_unique_key(target, item_url: str) -> str:
    raw = f"{target.site}:candidate_link:{item_url}"
    return make_hash(raw)


def build_page_info_defaults(target, result: dict) -> dict:
    """
    page_info 레코드 저장용 defaults 조립
    """
    page_info = result["page_info"]
    html = result["html"]

    return {
        "target": target,
        "source_url": target.url,
        "page_title": page_info["title"][:255],
        "item_title": "",
        "item_url": "",
        # [수정] raw_text는 너무 긴 본문 대신 짧은 미리보기만 저장
        "raw_text": page_info["text_preview"][:200],
        # [수정] raw_html도 과도하게 저장하지 않도록 축소
        "raw_html": html[:2000],
        "record_type": "page_info",
        "extra_data": {
            "a_count": page_info["a_count"],
            "contains_review_word": page_info["contains_review_word"],
            "contains_keyword": page_info["contains_keyword"],
        },
    }


def build_candidate_defaults(target, page_title: str, item: dict) -> dict:
    """
    candidate_link 레코드 저장용 defaults 조립
    """
    return {
        "target": target,
        "source_url": target.url,
        "page_title": page_title[:255],
        "item_title": item["title"][:255],
        "item_url": item["url"],
        # [수정] candidate_link에는 raw_text/raw_html 저장하지 않음
        "raw_text": "",
        "raw_html": "",
        "record_type": "candidate_link",
        "extra_data": {},
    }


@transaction.atomic
def save_search_result(target, result: dict) -> dict:
    """
    검색 결과를 DB에 저장합니다.

    [수정 핵심]
    - page_info는 1건 유지
    - candidate_link는 item_url 기준으로 중복 방지
    - item_title이 너무 이상한 데이터면 저장하지 않음
    """
    created_count = 0
    updated_count = 0
    skipped_count = 0  # [수정]

    page_info = result["page_info"]
    candidate_links = result["candidate_links"]

    # 1) 페이지 정보 upsert
    page_info_key = build_page_info_unique_key(target)
    _, created = upsert_raw_data(
        unique_key=page_info_key,
        defaults={
            **build_page_info_defaults(target, result),
            "unique_key": page_info_key,
        },
    )

    if created:
        created_count += 1
    else:
        updated_count += 1

    # 2) 후보 링크 upsert
    for item in candidate_links:
        title = (item.get("title") or "").strip()
        item_url = (item.get("url") or "").strip()

        # [수정] 제목 없으면 저장하지 않음
        if not title:
            skipped_count += 1
            continue

        # [수정] 너무 짧은 제목 제외
        if len(title) < 2:
            skipped_count += 1
            continue

        # [수정] URL 없으면 제외
        if not item_url:
            skipped_count += 1
            continue

        candidate_key = build_candidate_unique_key(target, item_url)
        _, created = upsert_raw_data(
            unique_key=candidate_key,
            defaults={
                **build_candidate_defaults(target, page_info["title"], item),
                "unique_key": candidate_key,
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    # 3) 마지막 크롤링 시간 갱신
    target.last_crawled_at = timezone.now()
    target.save(update_fields=["last_crawled_at"])

    return {
        "page_title": page_info["title"],
        "candidate_count": len(candidate_links),
        "created_count": created_count,
        "updated_count": updated_count,
        "skipped_count": skipped_count,  # [수정]
    }
