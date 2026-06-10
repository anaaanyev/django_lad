from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.text import slugify

from blog_app.models import Post, Category
from blog_app.forms import PostForm, SearchForm
from transliterate import translit


def index(request):
    search_form = SearchForm(data=request.GET)
    # Получаем 5 последних опубликованных постов
    posts = Post.objects.filter(published=True).select_related("category", "author")
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        posts = posts.filter(title__icontains=query)
    posts = posts[:5]
    context = {
        "posts": posts,
        "search_form": search_form,
    }
    return render(request, "blog/index.html", context)


def posts_list(request):
    posts = Post.objects.filter(published=True).select_related("category", "author")
    context = {
        "posts": posts
    }
    return render(request, "blog/posts_list.html", context)

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
        'posts', filter=Q(posts__published=True))
    ).filter(count_posts__gt=0)
    context = {
        'categories': categories
    }
    return render(request, 'blog/categories_list.html', context)


def category_detail(request, category_id):
    # Безопасно находим категорию
    category = get_object_or_404(Category, id=category_id)
    # Выбираем только опубликованные статьи, привязанные к этой категории
    posts = Post.objects.filter(category=category, published=True).select_related('author')
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/category_detail.html', context)


def post_create(request):
    if request.method == "POST":
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(translit(post.title, 'ru', reversed=True))
            post.save()
            return redirect("blog:index_page")
    else:
        form = PostForm()
    return render(request, "blog/posts_create.html", context={'form': form})
