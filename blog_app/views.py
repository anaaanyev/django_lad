from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from blog_app.models import Post


def index(request):
    return HttpResponse("<h1>Hello World!</h1>")

def posts_list(request):
    posts = Post.objects.filter(published=True)

    content = "<h1>Опубликованные статьи</h1><br><br>"
    for post in posts:
        content += f"<a href='/posts/{post.pk}'>{post.title}</a> ({post.created_at:%Y-%m-%d})<br>"

    return HttpResponse(content)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = f"""
        <h1>{post.title}</h1>
        <p>Автор: {post.author}</p>
        <div>{post.content}</div>
        <hr>
        <a href="/posts/">Назад к статьям</a>
    """
    return HttpResponse(content)
