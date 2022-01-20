from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status, exceptions
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignUpSerializer
from mwodeola_tokens.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from mwodeola_users.models import MwodeolaUser


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
        except (TokenError, IntegrityError) as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)


class SignUpView(SignBaseView):
    serializer_class = SignUpSerializer


class SignInView(SignBaseView):
    serializer_class = TokenObtainPairSerializer


class SignOutView(SignBaseView):
    serializer_class = TokenBlacklistSerializer


# 회원 탈퇴
# 추후 탈퇴 정책 꼭 보완하기.
class WithdrawalView(SignBaseView):

    def delete(self, request):
        authorization = request.META.get(api_settings.AUTH_HEADER_NAME)
        token_str = authorization[len('Bearer '):]

        try:
            token = RefreshToken(token_str)
            user_id = token.payload['user_id']
        except TokenError as e:
            raise InvalidToken(e.args[0])

        try:
            MwodeolaUser.objects.get(id=user_id).delete()
        except ObjectDoesNotExist as e:
            raise exceptions.ValidationError(e)

        return HttpResponse(status=status.HTTP_200_OK)


sign_up = SignUpView.as_view()
sign_in = SignInView.as_view()
sign_out = SignOutView.as_view()
withdrawal = WithdrawalView.as_view()
