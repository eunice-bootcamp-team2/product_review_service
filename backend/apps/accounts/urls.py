from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (  # -------------------------------; [추가] 템플릿 페이지용 View
    LoginPageView,
    MeAPIView,
    MyPageView,
    SignupAPIView,
    SignupPageView,
    UserViewSet,
)

router = DefaultRouter()

# -----------------------------------
# [수정] UserViewSet는 API이므로 api/users/ 아래로 들어가게 구성
# 실제 최종 URL: /accounts/api/users/
# -----------------------------------
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    # =================================================
    # Template Page URLs
    # =================================================
    # -----------------------------------
    # [추가] 회원가입 페이지
    # 실제 최종 URL: /accounts/signup/
    # -----------------------------------
    path("signup/", SignupPageView.as_view(), name="signup-page"),
    # -----------------------------------
    # [추가] 로그인 페이지
    # 실제 최종 URL: /accounts/login/
    # -----------------------------------
    path("login/", LoginPageView.as_view(), name="login-page"),
    # -----------------------------------
    # [추가] 마이페이지
    # 실제 최종 URL: /accounts/mypage/
    # -----------------------------------
    path("mypage/", MyPageView.as_view(), name="mypage"),
    # =================================================
    # API URLs
    # =================================================
    # -----------------------------------
    # [수정] 기존 UserViewSet는 루트가 아니라 api/ 아래로 이동
    # 실제 최종 URL: /accounts/api/users/
    # -----------------------------------
    path("api/", include(router.urls)),
    # -----------------------------------
    # [수정] 기존 signup/ API는 페이지와 충돌하므로 api/signup/ 로 변경
    # 실제 최종 URL: /accounts/api/signup/
    # -----------------------------------
    path("api/signup/", SignupAPIView.as_view(), name="signup-api"),
    # -----------------------------------
    # [수정] 기존 login/ API는 페이지와 충돌하므로 api/login/ 로 변경
    # 실제 최종 URL: /accounts/api/login/
    # -----------------------------------
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # -----------------------------------
    # [수정] JWT 재발급 API
    # 실제 최종 URL: /accounts/api/token/refresh/
    # -----------------------------------
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # -----------------------------------
    # [수정] 현재 로그인한 사용자 정보 조회 API
    # 실제 최종 URL: /accounts/api/me/
    # -----------------------------------
    path("api/me/", MeAPIView.as_view(), name="me-api"),
]
