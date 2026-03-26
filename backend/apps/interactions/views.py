from apps.reviews.models import Review
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReviewBookmark, ReviewComment, ReviewLike, ReviewReport
from .serializers import ReviewCommentSerializer, ReviewReportSerializer


class ReviewLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        obj, created = ReviewLike.objects.get_or_create(
            review=review, user=request.user
        )

        if not created:
            obj.delete()
            liked = False
        else:
            liked = True

        count = ReviewLike.objects.filter(review=review).count()

        return Response(
            {
                "liked": liked,
                "like_count": count,
            },
            status=status.HTTP_200_OK,
        )


class ReviewBookmarkToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        obj, created = ReviewBookmark.objects.get_or_create(
            review=review, user=request.user
        )

        if not created:
            obj.delete()
            bookmarked = False
        else:
            bookmarked = True

        count = ReviewBookmark.objects.filter(review=review).count()

        return Response(
            {
                "bookmarked": bookmarked,
                "bookmark_count": count,
            },
            status=status.HTTP_200_OK,
        )


class ReviewCommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        content = request.data.get("content", "").strip()

        if not content:
            return Response(
                {"detail": "내용이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        comment = ReviewComment.objects.create(
            review=review, user=request.user, content=content
        )

        serializer = ReviewCommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewCommentListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        comments = ReviewComment.objects.filter(review=review).order_by("-created_at")

        serializer = ReviewCommentSerializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, comment_id):
        comment = get_object_or_404(ReviewComment, id=comment_id)

        if comment.user != request.user:
            return Response(
                {"detail": "본인 댓글만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        content = request.data.get("content", "").strip()

        if not content:
            return Response(
                {"detail": "내용이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        comment.content = content
        comment.save()

        serializer = ReviewCommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        comment = get_object_or_404(ReviewComment, id=comment_id)

        if comment.user != request.user:
            return Response(
                {"detail": "본인 댓글만 삭제할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        comment.delete()

        return Response(
            {"detail": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
        )


class ReviewReportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        reason = request.data.get("reason", "").strip()

        if not reason:
            return Response(
                {"detail": "신고 사유가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        report = ReviewReport.objects.create(
            review=review, user=request.user, reason=reason
        )

        serializer = ReviewReportSerializer(report)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewReportListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)

        reports = ReviewReport.objects.filter(review=review).order_by("-created_at")

        serializer = ReviewReportSerializer(reports, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
