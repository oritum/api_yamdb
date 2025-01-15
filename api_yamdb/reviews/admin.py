from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Регистрация модели Review в админке."""

    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    list_filter = (
        'author',
        'pub_date',
    )
    search_fields = (
        'text',
        'author__username',
    )
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели Comment в админке."""

    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_filter = (
        'author',
        'pub_date',
    )
    search_fields = (
        'text',
        'author__username',
    )
    ordering = ('-pub_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Регистрация модели Category в админке."""

    list_display = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Регистрация модели Genre в админке."""

    list_display = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Регистрация модели Title в админке."""

    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    list_filter = (
        'name',
        'year',
        'category',
    )
    search_fields = ('name',)
    ordering = ('name',)
