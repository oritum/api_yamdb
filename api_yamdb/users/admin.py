from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Регистрация кастомной модели пользователя в админке."""
