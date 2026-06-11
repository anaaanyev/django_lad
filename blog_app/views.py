from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from slugify import slugify

from blog_app.models import Post, Category
from blog_app.forms import PostForm, SearchForm


def index(request):
    # Инициализируем форму поиска данными из GET-запроса (URL параметров)
    search_form = SearchForm(data=request.GET)
    # Базовый набор опубликованных статей
    posts = Post.objects.filter(published=True).select_related("category", "author")
    # Если пользователь ввел поисковый запрос
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        if query:
            # Фильтруем статьи по совпадению подстроки в заголовке без учета регистра (icontains)
            posts = posts.filter(title__icontains=query)

    # Выбираем последние 5 статей после фильтрации
    posts = posts[:5]
    context = {
        "posts": posts,
        "search_form": search_form,     # Передаем форму поиска в шаблон
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
    # Если пользователь отправил данные формы (нажал кнопку отправить)
    if request.method == "POST":
        form = PostForm(data=request.POST)

        if form.is_valid():
            # Метод save(commit=False) создает объект в памяти, но не пишет его в БД.
            # Это нужно, так как в форме нет поля slug, а оно уникальное и обязательное в модели!
            post = form.save(commit=False)
            # Автоматическая генерация slug на основе заголовка статьи.
            post.slug = slugify(post.title)
            # Записываем статью в базу данных
            post.save()
            # Перенаправляем пользователя на главную страницу (список постов)
            return redirect("blog:index_page")
    # Если пользователь просто открыл страницу создания (GET)
    else:
        form = PostForm()
    # Рендерим шаблон, передавая в него объект формы
    return render(request, "blog/posts_create.html", context={'form': form})
