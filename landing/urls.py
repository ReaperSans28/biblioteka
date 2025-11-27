from . import views
from django.urls import path
from rest_framework import routers

# Импортируем ViewSets для регистрации в router
from landing.views import BookViewSet

# Создаем router для автоматической регистрации ViewSet endpoints
# Router автоматически создает стандартные CRUD endpoints для каждого ViewSet
router = routers.DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

app_name = "landing"

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('post/', views.ItemsCreateView.as_view(), name="post")
]
urlpatterns += router.urls