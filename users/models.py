from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель Django.
    
    Наследуется от AbstractUser, что дает нам все стандартные поля:
    - username, email, password
    - first_name, last_name
    - is_active, is_staff, is_superuser
    - date_joined, last_login
    
    Дополнительно добавляем поля специфичные для библиотеки:
    - phone_number - для связи с пользователем
    - birth_date - дата рождения (может использоваться для возрастных ограничений)
    - address - адрес пользователя (для доставки книг)
    - avatar - фото профиля
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text="Электронная почта пользователя (используется для входа)"
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Дата рождения пользователя"
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Фото профиля пользователя"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.username})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]
