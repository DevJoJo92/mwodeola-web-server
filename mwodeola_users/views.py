from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings

from .serializers import SignUpSerializer
from mwodeola_tokens.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer


# Create your views here.
class SignBaseView(generics.GenericAPIView):
    permission_classes = []
    authentication_classes = []

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)


class SignUpView(SignBaseView):
    serializer_class = SignUpSerializer


class SignInView(SignBaseView):
    serializer_class = TokenObtainPairSerializer


class SignOutView(SignBaseView):
    serializer_class = TokenBlacklistSerializer


# 회원 탈퇴
class WithdrawalView(SignBaseView):
    serializer_class = TokenBlacklistSerializer

    def post(self, request, *args, **kwargs):
        authorization = request.META.get(api_settings.AUTH_HEADER_NAME)
        token_str = authorization[len('Bearer '):]
        token =
        return super().post(request, *args, **kwargs)


sign_up = SignUpView.as_view()
sign_in = SignInView.as_view()
sign_out = SignOutView.as_view()
