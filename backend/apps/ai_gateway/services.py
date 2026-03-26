import requests
from django.conf import settings

FASTAPI_URL = "http://fastapi:8001"


class FastAPIClient:
    """
    FastAPI AI 서버 호출 전용 클라이언트
    """

    @staticmethod
    def get_embedding(text: str):
        response = requests.post(
            f"{FASTAPI_URL}/api/v1/recommend/embed",
            json={"texts": [text]},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()["embeddings"][0]

    @staticmethod
    def get_similarity(text1: str, text2: str) -> dict:
        url = f"{settings.FASTAPI_BASE_URL}/api/v1/recommend/similarity"

        payload = {"text1": text1, "text2": text2}

        response = requests.post(url, json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
