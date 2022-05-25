from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

from rest_framework.decorators import (
    api_view, authentication_classes
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt import views
from rest_framework_simplejwt.exceptions import (
    InvalidToken, TokenError
)
from rest_framework_simplejwt.tokens import Token, AccessToken, RefreshToken


@method_decorator(csrf_protect, name="post")
class CustomTokenObtainPairView(views.TokenObtainPairView):
    """use cookie"""

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response(data={"message": "set tokens"})
        response.set_cookie(key="access",
                            value=serializer.validated_data["access"],
                            httponly=True,)

        response.set_cookie(key="refresh",
                            value=serializer.validated_data["refresh"],
                            httponly=True,)
        return response


@method_decorator(csrf_protect, name="post")
class CustomTokenRefreshView(views.TokenRefreshView):
    """use cookie"""

    def post(self, request: HttpRequest, *args, **kwargs):
        access = request.COOKIES.get("access")
        if access:
            try:
                AccessToken(access)
                response = Response({"message": "This is a suspicious access. Deleted the tokens."},
                                    status=status.HTTP_400_BAD_REQUEST)
                response.delete_cookie("access")
                response.delete_cookie("refresh")
                return response
            except TokenError:
                pass
        else:
            raise InvalidToken()
        serializer = self.get_serializer(data={"refresh": request.COOKIES.get("refresh")})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response({"message": "reset access"})
        response.set_cookie(key="access", 
                            value=serializer.validated_data["access"],
                            httponly=True)
        return response


@api_view(["GET"])
@authentication_classes([])
def has_access_token(request: HttpRequest):
    response = Response(data={"has_access_token": False})
    access = request.COOKIES.get("access")
    if access:
        try:
            AccessToken(access)
        except TokenError:
            return response

        response.data["has_access_token"] = True
    return response


@api_view(["GET"])
@authentication_classes([])
def has_refresh_token(request: HttpRequest):
    response = Response(data={"has_refresh_token": False})
    refresh = request.COOKIES.get("refresh")
    if refresh:
        try:
            RefreshToken(refresh)
        except TokenError:
            return response

        response.data["has_refresh_token"] = True
    return response


@api_view(["GET"])
@authentication_classes([])
def csrf_token_view(request: HttpRequest):
    response = Response({"csrftoken": get_token(request)})
    return response


@api_view(["GET"])
@authentication_classes([])
def logout(request: HttpRequest):
    response = Response({"message": "logout succeeded"})
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response
