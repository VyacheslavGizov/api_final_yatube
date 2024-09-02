"""Модуль содержит классы пользовательских разрешений."""

from rest_framework.permissions import BasePermission, SAFE_METHODS


NOT_AUTHOR_ERROR = 'У вас недостаточно прав для выполнения данного действия.'


class IsAuthorOrReadOnly(BasePermission):
    """Предоставит доступ к изменению контента лишь автору этого контента."""

    message = NOT_AUTHOR_ERROR

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
