# backend/apps/ai_gateway/admin.py
# [추가] AI 추론 결과를 Django admin에서 확인하기 위한 파일

from django.contrib import admin

from .models import AIAnalysisTask, ReviewSimilarityResult


@admin.register(ReviewSimilarityResult)
class ReviewSimilarityResultAdmin(admin.ModelAdmin):
    # [추가] 목록에서 주요 필드 확인
    list_display = (
        "id",
        "product",
        "source_review",
        "compared_review",
        "similarity_score",
        "similarity_label",
        "model_name",
        "analyzed_at",
    )

    # [추가] 검색 기능
    search_fields = (
        "product__name",
        "source_review__content",
        "compared_review__content",
        "compared_username_snapshot",
        "model_name",
    )

    # [추가] 필터
    list_filter = (
        "model_name",
        "similarity_label",
        "analyzed_at",
    )

    # [추가] 정렬
    ordering = ("-analyzed_at",)


# [추가] 비동기 작업 상태를 관리자에서 추적
@admin.register(AIAnalysisTask)
class AIAnalysisTaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "task_id",
        "source_review",
        "status",
        "candidate_count",
        "result_count",
        "model_name",
        "created_at",
        "finished_at",
    )
    search_fields = (
        "task_id",
        "source_review__content",
        "model_name",
    )
    list_filter = (
        "status",
        "model_name",
        "created_at",
    )
    ordering = ("-created_at",)
