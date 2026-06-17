from blog_app.models import Post
from blog_app.forms import PostForm
from django.urls import reverse_lazy

class PostFormBase:
    model = Post
    form_class = PostForm           # Используем нашу ModelForm
    success_url = reverse_lazy("blog:index_page")       # После создания — на главную
