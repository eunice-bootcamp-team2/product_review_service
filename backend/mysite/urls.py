from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect  # [추가] 루트 리다이렉트용
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # [추가] 루트("/") 접속 시 /products/ 로 이동
    path("", lambda request: redirect("/products/")),
    path("accounts/", include("apps.accounts.urls")),
    path("products/", include("apps.products.urls")),
    # [수정] reviews API / Web 분리
    path("reviews/", include("apps.reviews.urls")),
    path("interactions/", include("apps.interactions.urls")),
    path("ai/", include("apps.ai_gateway.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
