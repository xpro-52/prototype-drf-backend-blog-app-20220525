from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('posts', views.PostViewset)
router.register('authors', views.AuthorViewset)

app_name = 'blog'
urlpatterns = [
    path('', include(router.urls)),
    path('author_from_user/', views.author_from_user_view),
]

