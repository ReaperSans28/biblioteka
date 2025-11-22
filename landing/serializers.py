"""
Сериализаторы для приложения landing.

Сериализаторы в DRF - это классы, которые преобразуют:
1. Модели Django (Python объекты) → JSON (для отправки клиенту)
2. JSON (от клиента) → Модели Django (Python объекты)

Это позволяет легко работать с данными через API.
"""

from rest_framework import serializers
from .models import Item, Book, News
from django.contrib.auth import get_user_model

User = get_user_model()


class ItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Item.
    
    ModelSerializer автоматически создает поля на основе модели.
    Это самый простой способ создания сериализатора.
    
    Поля:
    - id - автоматически добавляется
    - name - название элемента
    - description - описание
    - created_at - дата создания (read_only - только для чтения)
    """
    class Meta:
        model = Item
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]  # Эти поля нельзя изменять через API


class BookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Book (книги).
    
    Используется для:
    - Создания новых книг (POST запрос)
    - Получения списка книг (GET запрос)
    - Обновления информации о книге (PUT/PATCH запрос)
    - Удаления книги (DELETE запрос)
    
    Все поля модели автоматически сериализуются.
    """
    # Переопределяем поле cover_image, чтобы возвращать полный URL
    # Вместо просто пути к файлу возвращаем полный URL для доступа через браузер
    cover_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "description",
            "isbn",
            "year_published",
            "pages",
            "cover_image",
            "cover_image_url",  # Дополнительное поле с URL
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def get_cover_image_url(self, obj):
        """
        Метод для получения полного URL изображения обложки.
        
        obj - это экземпляр модели Book
        
        Если изображение есть, возвращаем полный URL.
        Если нет - возвращаем None.
        """
        if obj.cover_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class BookCreateSerializer(serializers.ModelSerializer):
    """
    Упрощенный сериализатор для создания книги.
    
    Иногда полезно иметь отдельный сериализатор для создания,
    чтобы не показывать лишние поля при создании.
    """
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "description",
            "isbn",
            "year_published",
            "pages",
            "cover_image",
        ]
    
    def validate_isbn(self, value):
        """
        Валидация ISBN.
        
        Проверяем, что ISBN состоит только из цифр и имеет правильную длину.
        Это пример кастомной валидации поля.
        """
        if not value.isdigit():
            raise serializers.ValidationError("ISBN должен содержать только цифры")
        if len(value) != 13:
            raise serializers.ValidationError("ISBN должен содержать 13 цифр")
        return value


class NewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели News (новости).
    
    Включает информацию об авторе новости.
    """
    # Вместо просто ID автора показываем его username и email
    author_username = serializers.CharField(source="author.username", read_only=True)
    author_email = serializers.CharField(source="author.email", read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "content",
            "author",
            "author_username",
            "author_email",
            "image",
            "image_url",
            "is_published",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "author_username", "author_email"]
    
    def get_image_url(self, obj):
        """Получение полного URL изображения новости"""
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def create(self, validated_data):
        """
        Переопределяем метод create, чтобы автоматически установить автора.
        
        Когда пользователь создает новость, мы автоматически устанавливаем
        его как автора, используя request.user из контекста.
        """
        # Получаем пользователя из контекста (передается из view)
        user = self.context["request"].user
        validated_data["author"] = user
        return super().create(validated_data)

