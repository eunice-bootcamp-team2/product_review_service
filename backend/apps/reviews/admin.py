# apps/reviews/admin.py

from django.contrib import admin

from .models import Review, ReviewAI, ReviewImage


@admin.action(description="선택한 리뷰 복구")
def restore_reviews(modeladmin, request, queryset):
    for obj in queryset:
        obj.restore()


@admin.action(description="선택한 리뷰 완전 삭제")
def hard_delete_reviews(modeladmin, request, queryset):
    for obj in queryset:
        obj.hard_delete()


@admin.action(description="선택한 리뷰 삭제(논리 삭제)")
def soft_delete_reviews(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


class ReviewAIInline(admin.StackedInline):
    model = ReviewAI
    extra = 0
    can_delete = False


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product",
        "user",
        "rating",
        "is_public",
        "is_deleted",
        "deleted_at",
        "created_at",
    ]
    list_filter = ["is_public", "is_deleted", "created_at"]
    search_fields = ["content", "product__name", "user__username"]
    actions = [soft_delete_reviews, restore_reviews, hard_delete_reviews]
    inlines = [ReviewImageInline, ReviewAIInline]

    def get_queryset(self, request):
        return Review.all_objects.select_related("user", "product").all()

    def delete_model(self, request, obj):
        obj.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()
