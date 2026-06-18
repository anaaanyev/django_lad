from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from slugify import slugify
from django.urls import reverse_lazy

from blog_app.models import Post, Category
from blog_app.forms import SearchForm, CategoryForm
from mixins import PostFormBase


class MainPageView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return self.model.objects.filter(published=True).select_related("category", "author")

    def get_context_data(self, *, object_list=..., **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchForm(data=self.request.GET)
        posts = context['posts']
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            if query:
                posts = posts.filter(title__icontains=query)
        context['posts'] = posts[:5]
        context['search_form'] = search_form
        return context


# https://www.youtube.com/watch?v=NOX83nszcwI&list=PL4cUxeGkcC9hgO93oEHPBMuLA20y0SBVK&index=5
def query_posts_list(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(title__icontains=query, published=True).select_related("category", "author")
    return render(request, 'blog/partials/posts_list_main_page.html', {'posts': posts})


# def index(request):
#     # Инициализируем форму поиска данными из GET-запроса (URL параметров)
#     search_form = SearchForm(data=request.GET)
#     # Базовый набор опубликованных статей
#     posts = Post.objects.filter(published=True).select_related("category", "author")
#     # Если пользователь ввел поисковый запрос
#     if search_form.is_valid():
#         query = search_form.cleaned_data.get('query')
#         if query:
#             # Фильтруем статьи по совпадению подстроки в заголовке без учета регистра (icontains)
#             posts = posts.filter(title__icontains=query)
#
#     # Выбираем последние 5 статей после фильтрации
#     posts = posts[:5]
#     context = {
#         "posts": posts,
#         "search_form": search_form,  # Передаем форму поиска в шаблон
#     }
#     return render(request, "blog/index.html", context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/category_create.html"
    success_url = reverse_lazy("blog:categories_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('blog:categories_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)


# https://www.youtube.com/watch?v=Ula0c_rZ6gk&list=PL-2EBeDYMIbRByZ8GXhcnQSuv2dog4JxY
def check_title_category(request):
    title = request.POST.get('title')
    slug = slugify(title)
    if len(title) < 5:
        return HttpResponse("<div class='invalid-feedback d-block'>Ошибка! Укажите больше 5 символов</div>")
    elif Category.objects.filter(slug=slug).exists():
        return HttpResponse("<div class='invalid-feedback d-block'>Такая категория уже существует</div>")
    else:
        return HttpResponse("<div class='invalid-feedback d-block success'>Доступно для создания</div>")


# def category_create(request):
#     if not request.user.is_superuser:
#         return redirect('blog:categories_list')
#
#     if request.method == 'POST':
#         form = CategoryForm(data=request.POST)
#         if form.is_valid():
#             category = form.save(commit=False)
#             category.slug = slugify(category.title)
#             category.save()
#             return redirect('blog:categories_list')
#     else:
#         form = CategoryForm()
#     return render(request, 'blog/category_create.html', context={'form': form})


class CategoriesListView(ListView):
    model = Category
    template_name = 'blog/categories_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return self.model.objects.annotate(count_posts=Count(
            'posts', filter=Q(posts__published=True))
        )


# def categories_list(request):
#     # Получаем из БД только те категории в которых есть опубликованные статьи
#     # https://www.youtube.com/watch?v=eSlIF3FDs5s&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=34
#     categories = Category.objects.annotate(count_posts=Count(
#         'posts', filter=Q(posts__published=True))
#     )
#     context = {
#         'categories': categories
#     }
#     return render(request, 'blog/categories_list.html', context)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    pk_url_kwarg = 'category_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=context['category'], published=True).select_related('author')
        return context


# def category_detail(request, category_id):
#     # Безопасно находим категорию
#     category = get_object_or_404(Category, id=category_id)
#     # Выбираем только опубликованные статьи, привязанные к этой категории
#     posts = Post.objects.filter(category=category, published=True).select_related('author')
#     context = {
#         'category': category,
#         'posts': posts
#     }
#     return render(request, 'blog/category_detail.html', context)


class PostCreateView(LoginRequiredMixin, PostFormBase, CreateView):
    """Создание новой статьи."""
    template_name = "blog/posts_create.html"

    def form_valid(self, form):
        """
        Переопределяем form_valid() для автоматической генерации slug.
        form.instance — это объект модели Post, который форма создала
        в памяти, но ещё НЕ сохранила в базу данных.
        Мы можем дополнить его нужными полями перед сохранением.
        """
        # Генерируем slug из заголовка статьи
        form.instance.slug = slugify(form.instance.title)
        # Вызываем родительский form_valid(), который сделает form.save() + redirect
        return super().form_valid(form)


# @login_required
# def post_create(request):
#     # Если пользователь отправил данные формы (нажал кнопку отправить)
#     if request.method == "POST":
#         form = PostForm(data=request.POST)
#
#         if form.is_valid():
#             # Метод save(commit=False) создает объект в памяти, но не пишет его в БД.
#             # Это нужно, так как в форме нет поля slug, а оно уникальное и обязательное в модели!
#             post = form.save(commit=False)
#             # Автоматическая генерация slug на основе заголовка статьи.
#             post.slug = slugify(post.title)
#             # Записываем статью в базу данных
#             post.save()
#             # Перенаправляем пользователя на главную страницу (список постов)
#             return redirect("blog:index_page")
#     # Если пользователь просто открыл страницу создания (GET)
#     else:
#         form = PostForm()
#     # Рендерим шаблон, передавая в него объект формы
#     return render(request, "blog/posts_create.html", context={'form': form})

class PostUpdateView(LoginRequiredMixin, PostFormBase, UpdateView):
    """Редактирование существующей статьи."""
    template_name = 'blog/post_edit.html'
    slug_url_kwarg = 'post_slug'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])
        if request.user != post.author:
            return redirect('blog:post_detail', post_slug=post.slug)
        return super().dispatch(request, *args, **kwargs)


# def post_edit(request, post_slug):
#     post = get_object_or_404(Post, slug=post_slug)
#
#     # Исключаем возможность любому пользователю изменить статью
#     if request.user != post.author:
#         return redirect('blog:post_detail', post_slug=post.slug)
#
#     form = PostForm(data=request.POST or None, instance=post)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return redirect('blog:post_detail', post_slug=post.slug)
#     return render(request, 'blog/post_edit.html', context={'post': post, 'form': form})


class PostListView(ListView):
    """Страница статей — список опубликованных статей."""
    model = Post  # Модель
    template_name = "blog/posts_list.html"  # Шаблон
    context_object_name = "posts"  # Имя переменной (по умолчанию: object_list - для предка ListView)
    paginate_by = 5  # Показываем 5 статей на странице

    def get_queryset(self):
        """Возвращаем только опубликованные посты"""
        # по умолчанию: model.objects.all()
        return self.model.objects.filter(published=True).select_related("category", "author")


# def posts_list(request):
#     posts = Post.objects.filter(published=True).select_related("category", "author")
#     context = {
#         "posts": posts
#     }
#     return render(request, "blog/posts_list.html", context)


class PostDetailView(DetailView):
    """Страница отдельной статьи."""
    model = Post
    template_name = "blog/post_detail.html"
    slug_url_kwarg = "post_slug"  # Говорим Django: "slug в URL называется post_slug"

    # context_object_name по умолчанию = 'post' (имя модели в нижнем регистре)

    # https://proproprogs.ru/django4/django4-klass-detailview
    def get_object(self, queryset=...):
        post = get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])
        post.increase_views_count()
        return post


# def post_detail(request, post_slug):
#     # Безопасно получаем опубликованный пост по слагу или отдаем 404 ошибку
#     post = get_object_or_404(Post, slug=post_slug)
#     post.increase_views_count()
#     context = {
#         "post": post,
#     }
#     return render(request, "blog/post_detail.html", context)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статьи с подтверждением."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    slug_url_kwarg = "post_slug"
    success_url = reverse_lazy('blog:index_page')  # Куда перенаправить после успеха

    # context_object_name по умолчанию = 'post' (имя модели в нижнем регистре)

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])
        if request.user != post.author:
            return redirect('blog:post_detail', post_slug=post.slug)
        return super().dispatch(request, *args, **kwargs)
