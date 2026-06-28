from django.db.models import Count, Q

from blog_app.models import Category, Post
from django.contrib.auth.models import User


def categories_processors(request):
    """Добавляет список категорий во все шаблоны для выпадающего меню."""
    return {
        'nav_categories': Category.objects.annotate(count_posts=Count(
            'posts', filter=Q(posts__published=True))
        ).filter(count_posts__gt=0)
    }


def blog_stats_processor(request):
    """Добавляет статистику в футер на всех страницах:
    количество опубликованных статей и
    количество зарегистрированных пользователей в системе"""
    return {
        'total_posts': Post.objects.filter(published=True).count(),
        'total_users': User.objects.all().count()
    }
