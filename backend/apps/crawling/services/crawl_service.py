# backend/apps/crawling/services/crawl_service.py

from apps.crawling.models import CrawlRawData
from django.utils import timezone

from .http import fetch_page
from .parser import extract_page_info


def crawl_search_target(target):
    """
    [유지 + 부분수정]
    검색 페이지를 크롤링해서:
    - 페이지 정보 추출
    - 상품 상세 링크 후보 저장
    - 마지막 크롤링 시간 갱신
    - 요약 정보 반환
    """

    response = fetch_page(target.url)
    html = response.text

    page_info = extract_page_info(html)

    # [수정] extract_candidate_links 함수가 현재 없으므로 임시로 빈 리스트 처리
    candidate_links = []

    CrawlRawData.objects.create(
        target=target,
        source_url=target.url,
        page_title=page_info["title"],
        raw_text=page_info["text_preview"],
        raw_html=html[:5000],
        extra_data={
            "a_count": page_info["a_count"],
            "contains_review_word": page_info["contains_review_word"],
            "contains_keyword": page_info["contains_keyword"],
            "type": "page_info",
        },
    )

    for item in candidate_links[:20]:
        CrawlRawData.objects.create(
            target=target,
            source_url=target.url,
            page_title=page_info["title"],
            item_title=item["title"],
            item_url=item["url"],
            raw_text="",
            raw_html="",
            extra_data={
                "type": "candidate_link",
            },
        )

    target.last_crawled_at = timezone.now()
    target.save(update_fields=["last_crawled_at"])

    return {
        "page_title": page_info["title"],
        "candidate_count": len(candidate_links),
    }
