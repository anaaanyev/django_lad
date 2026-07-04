from django.urls import path
from drf_app.api import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView

app_name = 'drf'

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
]
