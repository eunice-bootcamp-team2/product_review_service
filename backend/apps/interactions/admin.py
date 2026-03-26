from django.contrib import admin

from .models import ReviewBookmark, ReviewComment, ReviewLike, ReviewReport

admin.site.register(ReviewLike)
admin.site.register(ReviewBookmark)
admin.site.register(ReviewComment)
admin.site.register(ReviewReport)
