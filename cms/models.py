from django.contrib.auth import get_user_model
from django.db import models
from tinymce.models import HTMLField

User = get_user_model()

from django.contrib.auth.models import User
class News(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    content = HTMLField(verbose_name="Содержание")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name="Дата создания")
    updated_at = models.DateTimeField(verbose_name="Дата обновления")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class Genre(models.Model):
    title = models.CharField(verbose_name="Название")


class Book(models.Model):
    class AgeLimit(models.TextChoices):
        ALL_AGES = 0
        CHILDREN = 6
        TEENAGERS = 12
        ADULTS = 18

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    short_description = models.CharField(verbose_name="Краткое описание", max_length=127)
    full_description = models.TextField(verbose_name="Полное описание")
    cover = models.ImageField(verbose_name="Обложка")
    price = models.PositiveIntegerField(verbose_name="Цена")
    created_at = models.DateTimeField(verbose_name="Дата создания")
    updated_at = models.DateTimeField(verbose_name="Дата обновления")
    age_limit = models.CharField(choices=AgeLimit.choices, default=AgeLimit.ALL_AGES, verbose_name="Возрастное ограничение")
    type = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    genre = models.ManyToManyField(
        Genre,
        on_delete=models.CASCADE
    )
    is_free = models.BooleanField(verbose_name="Бесплатно?")
    is_public = models.BooleanField(verbose_name="Доступ")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

