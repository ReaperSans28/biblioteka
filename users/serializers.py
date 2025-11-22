from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    
    При регистрации нужно:
    1. Проверить, что пароль и подтверждение пароля совпадают
    2. Валидировать пароль (длина, сложность и т.д.)
    3. Хешировать пароль перед сохранением
    4. Создать токен для пользователя (для API аутентификации)
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
        help_text="Пароль должен быть не менее 8 символов"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Повторите пароль для подтверждения"
    )
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password_confirm",
            "birth_date",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
        }
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "Пароли не совпадают"
            })
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует")
        return value
    
    def create(self, validated_data):
        """
        Создание нового пользователя.
        
        1. Удаляем password_confirm (он не нужен в модели)
        2. Извлекаем пароль
        3. Создаем пользователя БЕЗ пароля
        4. Устанавливаем пароль через set_password (автоматически хеширует)
        5. Сохраняем пользователя
        6. Создаем токен для API аутентификации
        """
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения и обновления информации о пользователе.
    
    Используется для:
    - Просмотра профиля пользователя
    - Обновления профиля
    - НЕ используется для регистрации (для этого UserRegistrationSerializer)
    """
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "birth_date",
            "avatar",
            "avatar_url",
            "date_joined",
            "last_login",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "date_joined",
            "last_login",
            "is_active",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    
    def get_avatar_url(self, obj):
        """Получение полного URL аватара пользователя"""
        if obj.avatar:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserLoginSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя.
    
    Это не ModelSerializer, потому что мы не создаем объект модели,
    а только проверяем учетные данные.
    
    Поля:
    - email - для входа (так как USERNAME_FIELD = 'email')
    - password - пароль пользователя
    """
    email = serializers.EmailField(
        required=True,
        help_text="Email пользователя для входа"
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        help_text="Пароль пользователя"
    )

