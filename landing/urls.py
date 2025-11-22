from django.urls import path
from . import views

app_name = "landing"

urlpatterns = [
    # HTML views (веб-интерфейс)
    # В проекте минимально нужны эти функции и класс
    path('', views.HomeView.as_view(), name="index"),
    path('books/create/', views.book_create_form, name="book_create"),
    path('news/create/', views.news_create_form, name="news_create"),
]
