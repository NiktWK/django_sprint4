# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        verbose_name='Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Post(PublishedModel):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        verbose_name='Автор публикации',
        to=User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    location = models.ForeignKey(
        verbose_name='Местоположение',
        to='Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to='Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='posts',
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)


class Location(PublishedModel):
    name = models.CharField(
        verbose_name='Название места',
        max_length=256,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)


class Category(PublishedModel):
    title = models.CharField(
        verbose_name='Заголовок',
        max_length=256,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Comment(models.Model):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
