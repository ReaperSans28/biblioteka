"""
Django management команда для создания суперпользователя.

Использование:
    python manage.py create_superuser

Команда запросит необходимые данные для создания суперпользователя.
Если пользователь с таким email уже существует, будет предложено обновить его до суперпользователя.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает суперпользователя для доступа к админ-панели'

    def add_arguments(self, parser):
        """Добавляем опциональные аргументы командной строки"""
        parser.add_argument(
            '--email',
            type=str,
            help='Email суперпользователя',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Имя пользователя',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Пароль (если не указан, будет запрошен)',
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Не запрашивать данные интерактивно (только с аргументами)',
        )

    def handle(self, *args, **options):
        """Основная логика команды"""
        email = options.get('email')
        username = options.get('username')
        password = options.get('password')
        noinput = options.get('noinput', False)

        # Если данные не переданы через аргументы, запрашиваем интерактивно
        if not noinput:
            if not email:
                email = input('Email: ')
            if not username:
                username = input('Имя пользователя: ')
            if not password:
                password = input('Пароль: ')
                password_confirm = input('Подтверждение пароля: ')
                if password != password_confirm:
                    self.stdout.write(
                        self.style.ERROR('Пароли не совпадают!')
                    )
                    return

        # Проверяем обязательные поля
        if not email or not username or not password:
            self.stdout.write(
                self.style.ERROR('Email, username и password обязательны!')
            )
            return

        try:
            # Пытаемся найти существующего пользователя
            user = User.objects.filter(email=email).first()
            
            if user:
                # Если пользователь существует, обновляем его до суперпользователя
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                if username and user.username != username:
                    user.username = username
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Пользователь {email} обновлен до суперпользователя!'
                    )
                )
            else:
                # Создаем нового суперпользователя
                user = User.objects.create_superuser(
                    email=email,
                    username=username,
                    password=password,
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Суперпользователь {email} успешно создан!'
                    )
                )
            
            # Создаем токен для API (если еще нет)
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'API токен создан: {token.key}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'API токен уже существует: {token.key}')
                )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании пользователя: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Неожиданная ошибка: {e}')
            )

