from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins, viewsets

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer, FollowSerializer
from posts.models import Group, Post, Follow


class PostViewSet(viewsets.ModelViewSet):
    """Обеспечит операции CRUD с моделью Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = LimitOffsetPagination
    # фильтрация и сортировка по тз не заданы
    # нужно добавить роутер

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Обеспечит операции CRUD с моделью Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))
    

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Обеспечит получение данных из модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ListCreateVievSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(ListCreateVievSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # return Follow.objects.filter(user__exact=self.request.user)
        return self.request.user.follower.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
