from urllib.parse import parse_qs, urljoin, urlparse

from apps.crawling.services.http import fetch_page
from apps.crawling.services.parser import extract_page_info, get_soup


def _normalize_danawa_product_url(url: str) -> str:
    """
    [수정]
    다나와 상품 URL을 가능한 한 대표 URL 형태로 정규화합니다.

    예:
    https://prod.danawa.com/info/?pcode=123456&cate=... -> https://prod.danawa.com/info/?pcode=123456
    """
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    pcode = query.get("pcode", [None])[0]

    if pcode:
        return f"https://prod.danawa.com/info/?pcode={pcode}"

    return url


def collect_danawa_search(target) -> dict:
    """
    다나와 검색 페이지를 수집해서
    페이지 기본 정보와 '상품 상세 링크 후보'만 반환합니다.

    [수정 핵심]
    - 아무 prod.danawa.com 링크나 저장하지 않음
    - 반드시 /info/ 와 pcode가 있는 상품 상세 URL만 저장
    - 의미 없는 anchor text 제거
    """
    response = fetch_page(target.url)
    html = response.text

    page_info = extract_page_info(html)
    soup = get_soup(html)

    candidates = []
    seen = set()

    for a in soup.select("a[href]"):
        href = (a.get("href") or "").strip()
        text = a.get_text(" ", strip=True)

        if not href:
            continue

        full_url = urljoin(target.url, href)

        # [수정] 다나와 상품 상세 URL만 허용
        if "prod.danawa.com/info/" not in full_url:
            continue

        # [수정] pcode 없는 링크는 제외
        if "pcode=" not in full_url:
            continue

        # [수정] 대표 URL 형태로 정규화
        normalized_url = _normalize_danawa_product_url(full_url)

        # [수정] 너무 짧거나 의미 없는 텍스트 제외
        if not text or len(text.strip()) < 2:
            continue

        # [수정] 불필요한 메뉴/버튼성 텍스트 제외
        blocked_words = [
            "더보기",
            "보기",
            "이동",
            "바로가기",
            "클릭",
            "광고",
            "로그인",
            "회원가입",
            "장바구니",
        ]
        if any(word in text for word in blocked_words):
            continue

        if normalized_url in seen:
            continue

        seen.add(normalized_url)

        candidates.append(
            {
                "title": text[:255],
                "url": normalized_url,
            }
        )

    return {
        "site": "danawa",
        "page_info": page_info,
        "candidate_links": candidates[:20],
        "html": html,
    }
