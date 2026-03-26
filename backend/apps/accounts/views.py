from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User
from .serializers import SignupSerializer, UserSerializer


# -------------------------------------------------
# API Views
# -------------------------------------------------
class UserViewSet(ViewSet):
    """
    사용자 조회용 ViewSet
    """

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SignupAPIView(generics.CreateAPIView):
    """
    회원가입 API
    """

    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class MeAPIView(generics.RetrieveAPIView):
    """
    현재 로그인한 사용자 정보 조회 API
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------------------------------
# Template Views
# -------------------------------------------------
class SignupPageView(TemplateView):
    template_name = "accounts/signup.html"


class LoginPageView(TemplateView):
    template_name = "accounts/login.html"


class MyPageView(TemplateView):
    template_name = "accounts/mypage.html"
