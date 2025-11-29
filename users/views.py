from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserLoginSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.

    Предоставляет endpoints для:
    - Просмотра списка пользователей (только для staff)
    - Просмотра своего профиля
    - Обновления своего профиля
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]  # Для загрузки аватаров

    def get_permissions(self):
        """
        Настраиваем разрешения:
        - list - только staff может видеть список всех пользователей
        - retrieve - можно посмотреть свой профиль или любой (если staff)
        - update - можно обновить только свой профиль
        - destroy - только staff может удалять пользователей
        """
        if self.action == "list":
            return [permissions.IsAdminUser()]  # Только админы видят список
        elif self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        elif self.action == "destroy":
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Фильтруем queryset в зависимости от пользователя.

        - Обычные пользователи видят только свой профиль
        - Staff видит всех пользователей
        """
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        # Обычные пользователи видят только себя
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        """
        Переопределяем, чтобы пользователь мог получить свой профиль по /me/.

        Если запрашивается 'me', возвращаем текущего пользователя.
        """
        if self.kwargs.get("pk") == "me":
            return self.request.user
        return super().get_object()

    def get_serializer_context(self):
        """Добавляем request в контекст для построения URL аватара"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    API endpoint для регистрации нового пользователя.

    @api_view декоратор указывает, что это API view (возвращает JSON).
    @permission_classes([permissions.AllowAny]) - доступно всем (не требуется авторизация).

    Принимает:
    - email, username, password, password_confirm
    - first_name, last_name (опционально)
    - phone_number, birth_date, address, bio (опционально)

    Возвращает:
    - Информацию о созданном пользователе
    - Токен для API аутентификации
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        # Создаем пользователя (в сериализаторе уже создается токен)
        user = serializer.save()

        # Получаем токен для нового пользователя
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "Пользователь успешно зарегистрирован",
            "user": UserSerializer(user, context={"request": request}).data,
            "token": token.key,  # Токен для API запросов
        }, status=status.HTTP_201_CREATED)

    # Если данные невалидны, возвращаем ошибки
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    API endpoint для входа пользователя.

    Принимает email и password, проверяет учетные данные.
    Если все верно, возвращает токен для API аутентификации.

    Также выполняет Django login для сессионной аутентификации (для веб-интерфейса).
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # Аутентифицируем пользователя
        # authenticate проверяет email и password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Пользователь найден и пароль верный
            # Выполняем Django login для сессионной аутентификации
            django_login(request, user)

            # Получаем или создаем токен для API
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Успешный вход",
                "user": UserSerializer(user, context={"request": request}).data,
                "token": token.key,
            }, status=status.HTTP_200_OK)
        else:
            # Неверные учетные данные
            return Response({
                "error": "Неверный email или пароль"
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """
    API endpoint для выхода пользователя.

    Удаляет токен пользователя и выполняет Django logout.
    """
    try:
        # Удаляем токен пользователя
        request.user.auth_token.delete()
    except:
        pass  # Если токена нет, ничего страшного

    # Выполняем Django logout
    django_logout(request)

    return Response({
        "message": "Успешный выход"
    }, status=status.HTTP_200_OK)


# HTML views для веб-интерфейса
def register_view(request):
    """
    HTML view для страницы регистрации.

    Показывает форму регистрации. При POST запросе создает пользователя.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Автоматически входим после регистрации
            django_login(request, user)
            return redirect("landing:index")
        # Если есть ошибки, показываем форму с ошибками
        return render(request, "users/register.html", {
            "form": form
        })

    # GET запрос - показываем пустую форму
    form = UserRegistrationForm()
    return render(request, "users/register.html", {
        "form": form
    })


def login_view(request):
    """
    HTML view для страницы входа.

    Показывает форму входа. При POST запросе аутентифицирует пользователя.
    """
    if request.user.is_authenticated:
        # Если уже авторизован, перенаправляем на главную
        return redirect("landing:index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            django_login(request, user)
            # Перенаправляем на страницу, с которой пришли, или на главную
            next_url = request.GET.get("next", "landing:index")
            return redirect(next_url)
        else:
            return render(request, "users/login.html", {
                "error": "Неверный email или пароль"
            })

    return render(request, "users/login.html")


@login_required
def profile_view(request):
    """
    HTML view для страницы профиля пользователя.

    @login_required декоратор требует, чтобы пользователь был авторизован.
    """
    if request.method == "POST":
        # Обновление профиля
        serializer = UserSerializer(
            request.user,
            data=request.POST,
            files=request.FILES,
            partial=True  # partial=True позволяет обновлять только часть полей
        )
        if serializer.is_valid():
            serializer.save()
            return redirect("users:profile")
        return render(request, "users/profile.html", {
            "user": request.user,
            "errors": serializer.errors
        })

    return render(request, "users/profile.html", {
        "user": request.user
    })


def logout_view(request):
    """
    HTML view для выхода.

    Выполняет logout и перенаправляет на главную страницу.
    """
    django_logout(request)
    return redirect("landing:index")
