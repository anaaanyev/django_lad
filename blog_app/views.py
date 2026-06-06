from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from blog_app.models import Post, Category


def index(request):
    # Получаем 5 последних опубликованных постов
    posts_published = Post.objects.filter(published=Post.Status.PUBLISHED)[:5]
    context = {
        "posts": posts_published,
    }
    return render(request, "blog/index.html", context)


def posts_list(request):
    posts = Post.objects.filter(published=Post.Status.PUBLISHED)
    li_posts = list(map(lambda post:
                        f"\t<li><a href='/posts/{post.slug}/'>{post.title}</a> - {post.created_at:%Y-%m-%d %H:%M}</li>\n",
                        posts))
    content = f'<h1>Опубликованные статьи</h1>\n<ul>\n{"".join(li_posts)}</ul>'
    return HttpResponse(content)


def post_detail(request, post_slug):
    # Безопасно получаем опубликованный пост по слагу или отдаем 404 ошибку
    post = get_object_or_404(Post, slug=post_slug)
    post.increase_views_count()
    context = {
        "post": post,
    }
    return render(request, "blog/post_detail.html", context)


def categories_list(request):
    # Получаем из БД только те категории в которых есть опубликованные статьи
    # https://www.youtube.com/watch?v=eSlIF3FDs5s&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=34
    categories = Category.objects.annotate(count_posts=Count(
        'posts', filter=Q(posts__published=Post.Status.PUBLISHED))
    ).filter(count_posts__gt=0)
    context = {
        'categories': categories
    }
    return render(request, 'blog/categories_list.html', context)


def category_detail(request, category_id):
    # Безопасно находим категорию
    category = get_object_or_404(Category, id=category_id)
    # Выбираем только опубликованные статьи, привязанные к этой категории
    posts = Post.objects.filter(category=category, published=Post.Status.PUBLISHED)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_detail.html', context)
