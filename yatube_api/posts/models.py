from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

DESCRIPTION_LENGTH_LIMIT = 20

# осознанно подправить методы __str__

class Group(models.Model):
    title = models.CharField(
        'Заголовок',
        max_length=200,
    )
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        max_length=80,
    )
    description = models.TextField('Описание',)

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title[:DESCRIPTION_LENGTH_LIMIT]


class Post(models.Model):
    text = models.TextField('Текст публикации')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts/',
        null=True,
        blank=True
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Сообщество',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self):
        return self.text[:DESCRIPTION_LENGTH_LIMIT]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация',
    )
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return (
            f'{self.text[:DESCRIPTION_LENGTH_LIMIT]} | '
            f'{self.post} | '
            f'{self.author} | '
        )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан на',
    )

    class Meta:
        # Здесь будет валидация на уникальность полей: нельзя быть подписанным на себя
        pass

    def __str__(self):
        return (
            f'{self.user} | '
            f'{self.following} | '
        )
