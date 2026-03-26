from django.urls import path

from .views import (
    ReviewBookmarkToggleAPIView,
    ReviewCommentCreateAPIView,
    ReviewCommentDetailAPIView,
    ReviewCommentListAPIView,
    ReviewLikeToggleAPIView,
    ReviewReportCreateAPIView,
    ReviewReportListAPIView,
)

urlpatterns = [
    # -----------------------------
    # 좋아요 토글
    # POST /interaction/like/<review_id>/
    # -----------------------------
    path(
        "like/<int:review_id>/",
        ReviewLikeToggleAPIView.as_view(),
        name="review-like-toggle",
    ),
    # -----------------------------
    # 북마크 토글
    # POST /interaction/bookmark/<review_id>/
    # -----------------------------
    path(
        "bookmark/<int:review_id>/",
        ReviewBookmarkToggleAPIView.as_view(),
        name="review-bookmark-toggle",
    ),
    # -----------------------------
    # 댓글 등록
    # POST /interaction/comment/<review_id>/
    # -----------------------------
    path(
        "comment/<int:review_id>/",
        ReviewCommentCreateAPIView.as_view(),
        name="review-comment-create",
    ),
    # -----------------------------
    # 댓글 목록 조회
    # GET /interaction/comments/<review_id>/
    # -----------------------------
    path(
        "comments/<int:review_id>/",
        ReviewCommentListAPIView.as_view(),
        name="review-comment-list",
    ),
    # -----------------------------
    # 댓글 수정 / 삭제
    # PATCH /interaction/comment/detail/<comment_id>/
    # DELETE /interaction/comment/detail/<comment_id>/
    # -----------------------------
    path(
        "comment/detail/<int:comment_id>/",
        ReviewCommentDetailAPIView.as_view(),
        name="review-comment-detail",
    ),
    # -----------------------------
    # 신고 등록
    # POST /interaction/report/<review_id>/
    # -----------------------------
    path(
        "report/<int:review_id>/",
        ReviewReportCreateAPIView.as_view(),
        name="review-report-create",
    ),
    # -----------------------------
    # 신고 목록
    # GET /interaction/reports/<review_id>/
    # -----------------------------
    path(
        "reports/<int:review_id>/",
        ReviewReportListAPIView.as_view(),
        name="review-report-list",
    ),
]
