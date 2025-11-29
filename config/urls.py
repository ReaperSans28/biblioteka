"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

# Импортируем ViewSets для регистрации в router
from landing.views import BookViewSet
from users.views import UserViewSet, register, login, logout

# Создаем router для автоматической регистрации ViewSet endpoints
# Router автоматически создает стандартные CRUD endpoints для каждого ViewSet
router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Админ-панель Django
    path("admin/", admin.site.urls),

    # API endpoints через DRF router
    # Все ViewSet автоматически получают стандартные CRUD endpoints:
    # - GET /api/items/ - список
    # - POST /api/items/ - создание
    # - GET /api/items/{id}/ - детали
    # - PUT/PATCH /api/items/{id}/ - обновление
    # - DELETE /api/items/{id}/ - удаление
    path('api/', include(router.urls)),

    # Кастомные API endpoints (не через router)
    path('api/register/', register, name='api-register'),
    path('api/login/', login, name='api-login'),
    path('api/logout/', logout, name='api-logout'),

    # HTML views (веб-интерфейс)
    path('', include('landing.urls')),
    path('users/', include('users.urls')),

    # Browsable API (красивый веб-интерфейс для API)
    # Доступен по адресу /api/ - показывает все доступные endpoints
    path('api-auth/', include('rest_framework.urls')),
]

# В режиме разработки добавляем статические файлы и медиа файлы
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Добавляем поддержку медиа файлов (загруженные изображения)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)