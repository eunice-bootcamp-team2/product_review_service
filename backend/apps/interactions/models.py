from django.conf import settings
from django.db import models


class ReviewLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "review")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"


class ReviewBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "review")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"


class ReviewComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"


class ReviewReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="reports"
    )
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "review")
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user} - {self.review}"
