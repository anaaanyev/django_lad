from django.test import TestCase
from django.contrib.auth.models import User
from blog_app.models import Category, Post


class PostModelTest(TestCase):
    """Набор тестов для модели статей (Post)."""

    def setUp(self):
        """Подготовка общих данных перед запуском каждого теста."""
        self.user = User.objects.create_user(
            username='writer',
            password='securepassword123'
        )
        self.category = Category.objects.create(
            title=' Django Разработка',
            slug='django-dev'
        )
        # Создаем статью для последующих проверок
        self.post = Post.objects.create(
            title='Тестовый пост',
            slug='test-post',
            content='Содержимое для проверки автотестов.',
            category=self.category,
            author=self.user,
            published=True
        )

    def test_post_fields_creation(self):
        """Проверяем корректность сохранения всех переданных полей модели."""
        self.assertEqual(self.post.title, 'Тестовый пост')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.content, 'Содержимое для проверки автотестов.')
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.author, self.user)
        self.assertTrue(self.post.published)

    def test_post_string_representation(self):
        """Проверяем, что метод __str__ возвращает заголовок статьи."""
        self.assertEqual(str(self.post), 'Тестовый пост')

    def test_post_published_default_value(self):
        """Убеждаемся, что по умолчанию статья создается неопубликованной (черновиком)."""
        draft_post = Post.objects.create(
            title='Черновик статьи',
            slug='draft-post',
            content='Этот пост не должен быть опубликован сразу.',
            category=self.category,
            author=self.user
            # Поле published не передаем — проверяем значение по умолчанию
        )
        self.assertFalse(draft_post.published)
