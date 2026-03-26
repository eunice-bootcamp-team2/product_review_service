import requests
from bs4 import BeautifulSoup


class DanawaReviewCollector:

    def collect_reviews(self, url: str, limit: int = 20):
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select(".prod_item")  # 상품 리스트

        results = []

        for item in items[:limit]:

            # ================================
            # [수정 1] 상품명 제대로 가져오기
            # ================================
            name_tag = item.select_one(".prod_name a")  # ✅ 올바른 선택자

            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)

            # ================================
            # [수정 2] 상품 링크 가져오기
            # ================================
            link = name_tag.get("href")

            # ================================
            # [수정 3] 가격은 따로 (옵션)
            # ================================
            price_tag = item.select_one(".price_real")  # 또는 .prod_pric

            price = price_tag.get_text(strip=True) if price_tag else ""

            results.append(
                {
                    "title": name,  # ✅ 이제 정상적으로 상품명
                    "url": link,
                    "price": price,
                }
            )

        return results
