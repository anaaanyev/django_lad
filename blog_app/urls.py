from django.urls import path
from blog_app import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index_page"),    # blog:index_page
    path("posts/", views.posts_list, name="posts_list"),    # blog:posts_list
    path("posts/create/", views.post_create, name="posts_create"),
    path("posts/<slug:post_slug>/", views.post_detail, name="post_detail"),    # blog:post_detail
    path("categories/", views.categories_list, name="categories_list"),    # blog:categories_list
    path("categories/<int:category_id>/", views.category_detail, name="category_detail"),    # blog:category_detail
]
