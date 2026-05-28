from django.contrib import admin
from .models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Какие колонки отображать в общем списке статей
    list_display = ('id', 'title', 'category', 'published', 'created_at', 'views_count')

    # По каким полям можно фильтровать список сбоку
    list_filter = ('author__username', 'published', 'created_at')

    # По каким полям будет работать строка текстового поиска
    search_fields = ('title', 'content')

    # Магия: при вводе title, поле slug будет заполняться автоматически транслитом!
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}
