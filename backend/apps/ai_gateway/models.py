# backend/apps/ai_gateway/models.py
# [추가] AI 추론 결과를 DRF DB에 저장하기 위한 모델 파일

from django.conf import settings
from django.db import models
from pgvector.django import VectorField


class ReviewSimilarityResult(models.Model):
    """
    [추가]
    특정 기준 리뷰(source_review)와 비교 리뷰(compared_review)의
    유사도 결과를 저장하는 모델
    """

    # [추가] 어떤 상품 안에서 비교했는지 저장
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="ai_similarity_results",
    )

    # [추가] 기준이 되는 리뷰
    source_review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="source_similarity_results",
    )

    # [추가] 비교 대상 리뷰
    compared_review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="compared_similarity_results",
    )

    # [추가] 버튼을 누른 사용자 (비로그인 사용자일 수 있으므로 null 허용)
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_similarity_results",
    )

    # [추가] FastAPI 모델 이름 저장
    model_name = models.CharField(
        max_length=100,
        default="upskyy/e5-small-korean",
    )

    # [추가] 유사도 점수
    similarity_score = models.FloatField()

    # [추가] 프론트에서 쓰는 해석 문구도 같이 저장
    similarity_label = models.CharField(max_length=30)

    # [추가] 기준 점수(threshold) 저장
    similarity_threshold = models.FloatField(default=0.45)

    # [추가] 당시의 텍스트 스냅샷 저장
    source_review_snapshot = models.TextField()
    compared_review_snapshot = models.TextField()

    # [추가] 비교 리뷰 작성자명을 스냅샷으로 저장
    compared_username_snapshot = models.CharField(max_length=150, blank=True)

    # [추가] 추론 시각
    analyzed_at = models.DateTimeField(auto_now=True)

    # [추가] 최초 생성 시각
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # [추가] 같은 기준 리뷰 + 비교 리뷰 + 모델 이름 조합은 1개만 유지
        constraints = [
            models.UniqueConstraint(
                fields=["source_review", "compared_review", "model_name"],
                name="unique_review_similarity_result",
            )
        ]
        ordering = ["-similarity_score", "-analyzed_at"]

    def __str__(self):
        return (
            f"[{self.model_name}] "
            f"source={self.source_review_id} "
            f"vs compared={self.compared_review_id} "
            f"score={self.similarity_score:.4f}"
        )


class AIAnalysisTask(models.Model):
    """
    [추가]
    Celery 비동기 작업 상태를 DB에서도 확인하기 위한 모델
    """

    STATUS_PENDING = "PENDING"
    STATUS_STARTED = "STARTED"
    STATUS_SUCCESS = "SUCCESS"
    STATUS_FAILURE = "FAILURE"

    STATUS_CHOICES = [
        (STATUS_PENDING, "대기중"),
        (STATUS_STARTED, "진행중"),
        (STATUS_SUCCESS, "완료"),
        (STATUS_FAILURE, "실패"),
    ]

    source_review = models.ForeignKey(
        "reviews.Review",
        on_delete=models.CASCADE,
        related_name="ai_analysis_tasks",
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_analysis_tasks",
    )

    task_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    model_name = models.CharField(
        max_length=100,
        default="upskyy/e5-small-korean",
    )

    similarity_threshold = models.FloatField(default=0.45)

    candidate_count = models.PositiveIntegerField(default=0)
    result_count = models.PositiveIntegerField(default=0)

    error_message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.task_id} - {self.status}"


class ReviewEmbedding(models.Model):
    """
    핵심 모델 (Vector DB 역할)
    """

    review = models.OneToOneField(
        "reviews.Review", on_delete=models.CASCADE, related_name="embedding"
    )

    # e5-small-korean = 384 차원
    embedding = VectorField(dimensions=384)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReviewEmbedding(review_id={self.review_id})"
