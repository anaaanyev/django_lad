from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_app.api import (
    PostViewSet,
    CategoriesViewSet
)

app_name = 'drf'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoriesViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
