from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Админ-панель для кастомной модели пользователя.
    
    Наследуется от BaseUserAdmin, чтобы сохранить стандартный функционал
    админ-панели Django для пользователей.
    """
    # Поля, отображаемые в списке пользователей
    list_display = ["email", "username", "first_name", "last_name", "is_staff", "is_active", "date_joined"]
    list_filter = ["is_staff", "is_active", "date_joined"]
    search_fields = ["email", "username", "first_name", "last_name"]
    
    # Группировка полей в форме редактирования
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Персональная информация", {
            "fields": ("first_name", "last_name", "phone_number", "birth_date", "address", "bio", "avatar")
        }),
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Важные даты", {
            "fields": ("last_login", "date_joined")
        }),
    )
    
    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2"),
        }),
    )
    
    ordering = ["-date_joined"]
    readonly_fields = ["last_login", "date_joined"]
