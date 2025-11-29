from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",

    "landing",
    # "cms",
    "users",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = (BASE_DIR / 'static',)

# Настройки для медиа файлов (загруженные пользователями)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustomUser"

# Настройки Django REST Framework
REST_FRAMEWORK = {
    # Класс аутентификации по умолчанию
    # SessionAuthentication - для веб-интерфейса (браузер)
    # TokenAuthentication - для API запросов (мобильные приложения, фронтенд)
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # Для работы в браузере
        "rest_framework.authentication.TokenAuthentication",  # Для API токенов
    ],

    # Класс разрешений по умолчанию
    # IsAuthenticated - только авторизованные пользователи могут обращаться к API
    # AllowAny - все могут обращаться (для публичных endpoints)
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # По умолчанию требуется авторизация
    ],

    # Пагинация - разбиение больших списков на страницы
    # Это помогает не загружать все данные сразу, а показывать по частям
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,  # Количество элементов на странице

    # Формат дат и времени
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%H:%M:%S",

    # Парсеры - форматы данных, которые API может принимать
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",  # JSON формат
        "rest_framework.parsers.FormParser",  # HTML формы
        "rest_framework.parsers.MultiPartParser",  # Для загрузки файлов
    ],

    # Рендереры - форматы данных, которые API может возвращать
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",  # JSON ответы
        "rest_framework.renderers.BrowsableAPIRenderer",  # Красивый веб-интерфейс для API
    ],
}