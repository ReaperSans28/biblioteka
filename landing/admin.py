from django.contrib import admin
from .models import Item, Book, News


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Админ-панель для модели Item"""
    list_display = ["name", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "description"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Админ-панель для модели Book"""
    list_display = ["title", "author", "year_published", "isbn", "created_at"]
    list_filter = ["year_published", "created_at"]
    search_fields = ["title", "author", "isbn", "description"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "author", "description")
        }),
        ("Детали", {
            "fields": ("isbn", "year_published", "pages", "cover_image")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Админ-панель для модели News"""
    list_display = ["title", "author", "is_published", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "content", "author__username"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Содержание", {
            "fields": ("title", "content", "image")
        }),
        ("Автор и публикация", {
            "fields": ("author", "is_published")
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )
