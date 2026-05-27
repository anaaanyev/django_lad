from django.contrib import admin
from blog_app.models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'published', 'created_at')
    list_filter = ('author', 'published', 'created_at')
    search_fields = ('title', 'author', 'content')
    prepopulated_fields = {'slug': ('title',)}
