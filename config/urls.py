from django.contrib import admin
from django.urls import path, include
from django.views import generic
# from djoser.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic.TemplateView.as_view(template_name='index.html')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('customauth.urls')),
    path('api/v1/', include('api_v1.urls')),
]
