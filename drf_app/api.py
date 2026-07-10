from rest_framework import generics, permissions, viewsets
from slugify import slugify

from blog_app.models import Post, Category
from drf_app.serializers import PostSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с постами блога.
    Предоставляет все CRUD-операции:
    list, create, retrieve, update, partial_update, destroy.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # --- Фильтрация, поиск и сортировка ---
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Точная фильтрация по значению поля: ?category=1 или ?published=true
    filterset_fields = ['category', 'published']

    # Полнотекстовый поиск (ищет вхождение подстроки): ?search=django
    search_fields = ['title', 'content']

    # Сортировка результатов: ?ordering=-created_at или ?ordering=title
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        """
        Переопределяем сохранение нового поста:
        1. Автор берётся из JWT-токена (request.user).
        2. Slug генерируется автоматически из заголовка (title).
        """
        # Получаем заголовок из провалидированных данных
        title = serializer.validated_data.get('title')
        # Генерируем URL-безопасный slug из заголовка
        generated_slug = slugify(title, allow_unicode=True)
        # Сохраняем пост, принудительно передавая автора и slug
        serializer.save(
            author=self.request.user,
            slug=generated_slug,
        )


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
