from django.urls import path
from django.views.generic import TemplateView

from blog_app import views

app_name = "blog"

urlpatterns = [
    path("", views.MainPageView.as_view(), name="index_page"),    # blog:index_page
    path("posts/", views.PostListView.as_view(), name="posts_list"),    # blog:posts_list
    path("posts/create/", views.PostCreateView.as_view(), name="posts_create"),  # blog:posts_create
    path("posts/<slug:post_slug>/", views.PostDetailView.as_view(), name="post_detail"),    # blog:post_detail
    path('posts/<slug:post_slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),    # blog:post_edit
    path('posts/<slug:post_slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),    # blog:post_edit
    path("categories/", views.CategoriesListView.as_view(), name="categories_list"),    # blog:categories_list
    path("categories/create/", views.CategoryCreateView.as_view(), name="category_create"),    # blog:category_create
    path("categories/<int:category_id>/", views.CategoryDetailView.as_view(), name="category_detail"),    # blog:category_detail
    path('about/', TemplateView.as_view(template_name='blog/about.html'), name='about'),
]

htmx_urlpatterns = [
    path('query_posts_list/', views.query_posts_list, name="query_posts_list"),
    path('check_title_category/', views.check_title_category, name="check_title_category")
]

urlpatterns += htmx_urlpatterns
