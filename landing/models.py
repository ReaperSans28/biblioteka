from django.db import models
from django.contrib.auth import get_user_model

# Получаем модель пользователя (кастомную)
User = get_user_model()


class Item(models.Model):
    """Базовая модель элемента (можно использовать для разных целей)"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"


class Book(models.Model):
    """
    Модель книги для библиотеки.
    
    Содержит основную информацию о книге:
    - Название, автор, описание
    - Год издания и количество страниц
    - ISBN для идентификации
    - Обложка книги (изображение)
    - Дата добавления в библиотеку
    """
    title = models.CharField(
        max_length=255,
        verbose_name="Название книги",
        help_text="Введите полное название книги"
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Автор",
        help_text="ФИО автора книги"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Краткое описание содержания книги"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="ISBN",
        help_text="Международный стандартный номер книги (13 цифр)"
    )
    year_published = models.IntegerField(
        verbose_name="Год издания",
        help_text="Год, когда была опубликована книга"
    )
    pages = models.IntegerField(
        verbose_name="Количество страниц",
        help_text="Общее количество страниц в книге"
    )
    cover_image = models.ImageField(
        upload_to="books/covers/",
        blank=True,
        null=True,
        verbose_name="Обложка",
        help_text="Изображение обложки книги"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["-created_at"]  # Сортировка по дате добавления (новые сначала)


class News(models.Model):
    """
    Модель новостей библиотеки.
    
    Используется для публикации новостей, анонсов событий,
    информации о новых поступлениях книг и т.д.
    """
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Заголовок новости"
    )
    content = models.TextField(
        verbose_name="Содержание",
        help_text="Полный текст новости"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="news",
        verbose_name="Автор",
        help_text="Пользователь, создавший новость"
    )
    image = models.ImageField(
        upload_to="news/images/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Иллюстрация к новости"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отметьте, чтобы новость была видна всем пользователям"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]  # Сортировка по дате (новые сначала)
