from django.contrib import admin
from reviews.models import Review, Comment


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
        'author__username'
    )
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели Comment в админке."""
    list_display = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_filter = (
        'author',
        'pub_date'
    )
    search_fields = (
        'text',
        'author__username'
    )
    ordering = ('-pub_date',)
