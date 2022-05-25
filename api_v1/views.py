from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.decorators import (
    api_view, permission_classes
)

from .serializers import PostSerializer, AuthorSerializer
from blog.models import Author, Post


class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([])
def author_from_user_view(request: HttpRequest):
    response = Response(data={"author": None})
    if (request.user.is_authenticated):
        try:
            response.data["author"] = request.user.author.id
        except ObjectDoesNotExist:
            pass
    return response
