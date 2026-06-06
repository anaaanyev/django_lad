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

    # Пагинатор (кол-во отображаемых статей в админке на странице)
    list_per_page = 30


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_count_posts')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    # https://www.youtube.com/watch?v=eb-Oesr4Zbk&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=40
    @admin.display(description="Кол-во опубликованных статей")
    def show_count_posts(self, category: Category):
        return category.posts.filter(published=Post.Status.PUBLISHED).count()
