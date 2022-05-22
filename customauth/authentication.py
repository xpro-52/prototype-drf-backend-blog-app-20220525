from django.http import HttpRequest
from django.middleware.csrf import CsrfViewMiddleware

from rest_framework import exceptions
from rest_framework.authentication import SessionAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationWithCookie(JWTAuthentication, SessionAuthentication):
    def authenticate(self, request: HttpRequest):
        self.enforce_csrf(request)
        raw_token = request.COOKIES.get("access")
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
