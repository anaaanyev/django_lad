from django.urls import path
from blog_app import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index_page"),    # blog:index_page   будет доступно в шаблонах
    path("posts/", views.posts_list, name="posts_published"),    # blog:index_page   будет доступно в шаблонах
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),    # blog:index_page   будет доступно в шаблонах
]
