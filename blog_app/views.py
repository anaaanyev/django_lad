from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from blog_app.models import Post, Category


def index(request):
    posts_published = Post.objects.filter(published=Post.Status.PUBLISHED)[:5]
    contex = {
        "posts": posts_published,
    }
    return render(request, "blog/index.html", contex)


def posts_list(request):
    posts = Post.objects.filter(published=Post.Status.PUBLISHED)
    li_posts = list(map(lambda post:
                        f"\t<li><a href='/posts/{post.slug}/'>{post.title}</a> - {post.created_at:%Y-%m-%d %H:%M}</li>\n",
                        posts))
    content = f'<h1>Опубликованные статьи</h1>\n<ul>\n{"".join(li_posts)}</ul>'
    return HttpResponse(content)


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    contex = {
        "post": post,
    }
    return render(request, "blog/post_detail.html", contex)


def categories_list(request):
    categories = Category.objects.all()
    li_categories = list(map(lambda cat: f"\t<li><a href='/categories/{cat.id}/'>{cat.title}</a></li>\n", categories))
    content = f"<h1>Категории</h1>\n<ul>\n{''.join(li_categories)}</ul>"
    return HttpResponse(content)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts_in_cat = Post.objects.filter(category=category, published=Post.Status.PUBLISHED)
    li_posts = list(map(lambda post: f"\t<li><a href='/posts/{post.slug}/'>{post.title}</a></li>\n", posts_in_cat))
    content = (f"<h1>Все посты категории '{category.title}'</h1>\n"
               f"<ul>\n{''.join(li_posts)}</ul>\n"
               f"<hr>\n"
               f"<a href='/categories/'>Назад к категориям</a>")
    return HttpResponse(content)
