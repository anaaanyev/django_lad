from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_app.api import (
    CategoryListCreateAPIView,
    CategoryRetrieveUpdateDestroyAPIView,
    PostViewSet
)

app_name = 'drf'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoryListCreateAPIView.as_view(), name='categories-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]
