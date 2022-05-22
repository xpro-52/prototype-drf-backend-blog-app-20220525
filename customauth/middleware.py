from config import settings
from django.middleware.csrf import CsrfViewMiddleware

from rest_framework.response import Response


class SameSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: Response = self.get_response(request)

        for key in response.cookies.keys():
            response.cookies[key]["samesite"] = "None"
            response.cookies[key]["secure"] = True
        return response
