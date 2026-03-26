from rest_framework import serializers

from .models import ReviewBookmark, ReviewComment, ReviewLike, ReviewReport


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = [
            "id",
            "user",
            "review",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


class ReviewBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewBookmark
        fields = [
            "id",
            "user",
            "review",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]


class ReviewCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ReviewComment
        fields = [
            "id",
            "user",
            "username",
            "review",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "username",
            "review",
            "created_at",
            "updated_at",
        ]


class ReviewReportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ReviewReport
        fields = [
            "id",
            "user",
            "username",
            "review",
            "reason",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "username",
            "review",
            "created_at",
        ]
