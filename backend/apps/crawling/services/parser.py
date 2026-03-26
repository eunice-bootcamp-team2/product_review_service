from bs4 import BeautifulSoup


def get_soup(html: str) -> BeautifulSoup:
    """
    HTML 문자열을 BeautifulSoup 객체로 변환합니다.
    """
    return BeautifulSoup(html, "lxml")


def extract_page_info(html: str) -> dict:
    """
    페이지의 공통 정보를 추출합니다.

    [수정 핵심]
    기존에는 soup.get_text()로 페이지 전체 텍스트를 긁어서
    광고/메뉴/로그인/배너 문구까지 raw_text로 저장되기 쉬웠습니다.

    그래서 이제는:
    - title
    - 링크 개수
    정도만 저장하고,
    text_preview는 아주 짧은 참고용 정보만 넣습니다.
    """
    soup = get_soup(html)

    title = soup.title.get_text(strip=True) if soup.title else ""

    # [수정] 페이지 전체 텍스트를 길게 저장하지 않도록 최소화
    body = soup.body.get_text(" ", strip=True)[:200] if soup.body else ""

    return {
        "title": title[:255],
        "a_count": len(soup.select("a[href]")),
        "contains_review_word": "리뷰" in body,
        "contains_keyword": "수분크림" in body,
        "text_preview": body,  # [수정] 기존보다 짧게 유지
    }
