from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MyReviewListAPIView,
    ReviewAIResultAPIView,
    ReviewImageUploadAPIView,
    ReviewViewSet,
)

router = DefaultRouter()
router.register("", ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:review_id>/images/",
        ReviewImageUploadAPIView.as_view(),
        name="review-image-upload",
    ),
    path(
        "<int:review_id>/ai/", ReviewAIResultAPIView.as_view(), name="review-ai-result"
    ),
    path("my/", MyReviewListAPIView.as_view(), name="my-review-list"),
]
