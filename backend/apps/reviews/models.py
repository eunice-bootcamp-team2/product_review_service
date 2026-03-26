from apps.core.models import SoftDeleteModel
from apps.products.models import Product
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Review(SoftDeleteModel):
    """
    제품 리뷰
    - Soft Delete 적용
    """

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="reviews",
    )
    content = models.TextField()
    rating = models.IntegerField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        username = self.user.username if self.user else "탈퇴한 사용자"
        return f"{self.product} - {username}"


class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="reviews/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReviewImage(review_id={self.review_id})"


class ReviewAI(models.Model):
    review = models.OneToOneField(
        Review,
        on_delete=models.CASCADE,
        related_name="ai_result",
    )
    sentiment = models.CharField(max_length=50)
    confidence = models.FloatField()
    keywords = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ReviewAI(review_id={self.review_id})"
