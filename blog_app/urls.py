from django.urls import path
from blog_app import views

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index_page"),    # blog:index_page
    path("posts/", views.PostListView.as_view(), name="posts_list"),    # blog:posts_list
    path("posts/create/", views.PostUpdateView.as_view(), name="posts_create"),  # blog:posts_create
    path("posts/<slug:post_slug>/", views.PostDetailView.as_view(), name="post_detail"),    # blog:post_detail
    path('posts/<slug:post_slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),    # blog:post_edit
    path('posts/<slug:post_slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),    # blog:post_edit
    path("categories/", views.categories_list, name="categories_list"),    # blog:categories_list
    path("categories/create/", views.category_create, name="category_create"),    # blog:category_create
    path("categories/<int:category_id>/", views.category_detail, name="category_detail"),    # blog:category_detail
]
