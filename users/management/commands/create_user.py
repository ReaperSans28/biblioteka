"""
Django management команда для создания обычного пользователя.

Использование:
    python manage.py create_user

Команда запросит необходимые данные для создания обычного пользователя.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает обычного пользователя'

    def add_arguments(self, parser):
        """Добавляем опциональные аргументы командной строки"""
        parser.add_argument(
            '--email',
            type=str,
            help='Email пользователя',
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
            '--first-name',
            type=str,
            help='Имя',
        )
        parser.add_argument(
            '--last-name',
            type=str,
            help='Фамилия',
        )
        parser.add_argument(
            '--phone',
            type=str,
            help='Номер телефона',
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
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        phone = options.get('phone')
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
            if not first_name:
                first_name = input('Имя (опционально): ') or None
            if not last_name:
                last_name = input('Фамилия (опционально): ') or None
            if not phone:
                phone = input('Номер телефона (опционально): ') or None

        # Проверяем обязательные поля
        if not email or not username or not password:
            self.stdout.write(
                self.style.ERROR('Email, username и password обязательны!')
            )
            return

        try:
            # Проверяем, существует ли пользователь
            if User.objects.filter(email=email).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Пользователь с email {email} уже существует!'
                    )
                )
                return

            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(
                        f'Пользователь с username {username} уже существует!'
                    )
                )
                return

            # Создаем нового пользователя
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                first_name=first_name or '',
                last_name=last_name or '',
                phone_number=phone or '',
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Пользователь {email} успешно создан!'
                )
            )
            
            # Создаем токен для API
            from rest_framework.authtoken.models import Token
            token, created = Token.objects.get_or_create(user=user)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'API токен создан: {token.key}')
                )

        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при создании пользователя: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Неожиданная ошибка: {e}')
            )

