from django.urls import re_path, path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path("csrftoken/", views.csrf_token_view, name="csrf-token"),
    path("has-access-token/", views.has_access_token, name="has-access-token"),
    path("has-refresh-token/", views.has_refresh_token, name="has-refresh-token"),
    path("logout/", views.logout, name="logout"),
    re_path(r"^jwt/create/?", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    re_path(r"^jwt/refresh/?", views.CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    re_path(r"^jwt/verify/?", TokenVerifyView.as_view(), name="jwt-verify"),
]