import base64
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.core.files.base import ContentFile

from posts.models import Comment, Group, Post, Follow, User


# оптимизировать, может есть способ из коробки
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            file_format, imgstr = data.split(';base64,')
            extension = file_format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name='temp.' + extension)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()  # Возможно не нужно
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Сериализвтор для модели Comment."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()  # Возможно не нужно
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализвтор для модели Group."""

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    
    def validate(self, data):
        if self.context['request'].user == data['following']:  # разобраться и переписать
            raise serializers.ValidationError('Подписка на себя запрещена') # сообщение об ошибке вынести в константу
        return data
        
    class Meta:
        model = Follow
        fields = '__all__'
        # не уверен, что нужен
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=['user', 'following'])]

