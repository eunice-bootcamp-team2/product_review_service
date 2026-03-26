from fastapi import APIRouter
from schemas.recommend_schema import (
    EmbeddingRequest,
    SimilarityRequest,
    SimilarityResponse,
)
from services.recommend_service import calculate_similarity, make_embeddings

router = APIRouter(prefix="/api/v1/recommend", tags=["recommend"])


@router.post("/embed")
def embed_text(request: EmbeddingRequest):
    vectors = make_embeddings(request.texts)
    return {"embeddings": vectors}


@router.post("/similarity", response_model=SimilarityResponse)
def similarity(payload: SimilarityRequest):
    return {"similarity": calculate_similarity(payload.text1, payload.text2)}
