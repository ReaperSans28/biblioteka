from rest_framework import viewsets, status, permissions
from .forms import BookForm
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect

from .models import Item, Book, News
from .serializers import (
    ItemSerializer,
    BookSerializer,
    BookCreateSerializer,
    NewsSerializer,
)


class HomeView(TemplateView):
    """
    Обычный Django TemplateView для отображения главной страницы.
    
    Это не DRF view, потому что мы хотим показывать HTML страницу,
    а не JSON ответ. DRF используется для API endpoints.
    """
    template_name = "landing/index.html"
    
    def get_context_data(self, **kwargs):
        """
        Добавляем данные в контекст шаблона.
        
        Получаем последние книги и новости для отображения на главной странице.
        """
        context = super().get_context_data(**kwargs)
        # Получаем последние 6 книг
        context["books"] = Book.objects.all()[:6]
        # Получаем последние 3 новости
        context["news"] = News.objects.filter(is_published=True)[:3]
        return context


class ItemViewSet(viewsets.ModelViewSet): # Не нужно
    """
    ViewSet для модели Item.
    
    ModelViewSet автоматически создает следующие endpoints:
    - GET /api/items/ - список всех элементов
    - POST /api/items/ - создание нового элемента
    - GET /api/items/{id}/ - получение конкретного элемента
    - PUT /api/items/{id}/ - полное обновление элемента
    - PATCH /api/items/{id}/ - частичное обновление элемента
    - DELETE /api/items/{id}/ - удаление элемента
    
    Атрибуты:
    - queryset - набор объектов для работы (все Item объекты)
    - serializer_class - класс сериализатора для преобразования данных
    - permission_classes - кто может обращаться к этим endpoints
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]  # Только авторизованные пользователи


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Book (книги).
    
    Предоставляет полный CRUD функционал для работы с книгами.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Разрешаем загрузку файлов (для обложек книг)
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        """
        Настраиваем разрешения в зависимости от действия.
        
        - list, retrieve (GET) - могут все (AllowAny)
        - create, update, destroy - только авторизованные (IsAuthenticated)
        """
        if self.action in ["list", "retrieve"]:
            # Просмотр списка и детальной информации доступны всем
            return [permissions.AllowAny()]
        # Создание, обновление и удаление только для авторизованных
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        """
        Выбираем сериализатор в зависимости от действия.
        
        При создании используем BookCreateSerializer (упрощенный),
        в остальных случаях - BookSerializer (полный).
        """
        if self.action == "create":
            return BookCreateSerializer
        return BookSerializer
    
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


class NewsViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели News (новости).
    
    Предоставляет функционал для работы с новостями библиотеки.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    parser_classes = [MultiPartParser, FormParser]  # Для загрузки изображений
    
    def get_queryset(self):
        """
        Фильтруем queryset в зависимости от пользователя.
        
        - Обычные пользователи видят только опубликованные новости
        - Авторизованные пользователи (особенно авторы) видят все свои новости
        """
        queryset = News.objects.all()
        
        # Если пользователь не авторизован, показываем только опубликованные
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        # Если пользователь авторизован, но не staff, показываем опубликованные + свои
        elif not self.request.user.is_staff:
            queryset = queryset.filter(
                is_published=True
            ) | queryset.filter(author=self.request.user)
        
        return queryset.order_by("-created_at")
    
    def get_permissions(self):
        """
        Настраиваем разрешения:
        - Просмотр - все могут
        - Создание - только авторизованные
        - Изменение/удаление - только автор или staff
        """
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        elif self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            # Для update и destroy проверяем, что пользователь - автор или staff
            return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        """
        При создании новости автоматически устанавливаем автора.
        
        Автор берется из request.user (текущий авторизованный пользователь).
        Это делается в сериализаторе, но можно и здесь.
        """
        serializer.save(author=self.request.user)
    
    def get_serializer_context(self):
        """
        Добавляем request в контекст сериализатора.
        
        Это нужно для построения полных URL изображений в сериализаторе.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# Функциональные views для HTML форм (не API)
def book_create_form(request):
    """
    View для отображения HTML формы создания книги.
    
    Это обычная Django view, не DRF, потому что мы показываем HTML форму.
    """
    
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("landing:index")
    else:
        form = BookForm()
    
    return render(request, "landing/book_form.html", {"form": form})


def news_create_form(request):
    """
    View для отображения HTML формы создания новости.
    """
    from .forms import NewsForm
    
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            from django.shortcuts import redirect
            return redirect("landing:index")
    else:
        form = NewsForm()
    
    return render(request, "landing/news_form.html", {"form": form})
