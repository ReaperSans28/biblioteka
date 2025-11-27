from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from landing.forms import ItemsForm
from landing.models import Item, Book
from landing.serializers import BookSerializer


class HomeView(TemplateView):
    template_name = "landing/index.html"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)


class ItemsCreateView(CreateView):
    model = Item
    form_class = ItemsForm
    success_url = reverse_lazy("landing:home")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        """
       Настраиваем разрешения в зависимости от действия.

       - list, retrieve (GET) - могут все (AllowAny)
       - create, update, destroy - только авторизованные (IsAuthenticated)
       """
        if self.action in permissions.SAFE_METHODS:
            # Просмотр списка и детальной информации доступны всем
            return [permissions.AllowAny()]
        # Создание, обновление и удаление только для авторизованных
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Дополнительные действия при создании книги.

        Здесь можно добавить логику, которая выполняется перед сохранением:
        - Логирование
        - Отправка уведомлений
        - Валидация бизнес-логики
        """
        # Просто сохраняем объект
        serializer.save()

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """
        Кастомное действие для получения последних книг.

        @action декоратор создает дополнительный endpoint:
        GET /api/books/recent/ - возвращает последние 5 книг

        detail=False означает, что это действие на коллекции (не на конкретном объекте)
        methods=["get"] - разрешенные HTTP методы
        """
        recent_books = self.queryset.order_by("-created_at")[:5]
        serializer = self.get_serializer(recent_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        """
        Пример кастомного действия для добавления книги в избранное.

        detail=True означает, что это действие на конкретном объекте
        GET /api/books/{id}/favorite/ - добавить книгу в избранное

        Это пример - в реальном проекте нужно создать модель FavoriteBook.
        """
        book = self.get_object()
        # Здесь можно добавить логику добавления в избранное
        return Response({
            "message": f"Книга '{book.title}' добавлена в избранное",
            "book_id": book.id
        })
