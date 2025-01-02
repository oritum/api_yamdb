from django.contrib import admin
from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для Review."""
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
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
    """Админка для Comment."""
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
