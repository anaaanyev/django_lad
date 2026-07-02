from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog_app.models import Category, Post


class PostViewTest(TestCase):
    """Набор тестов для проверки GET-представлений блога."""

    def setUp(self):
        """Создаем общие записи для проверки отображения страниц."""
        self.user = User.objects.create_user(
            username='editor',
            password='password123'
        )
        self.category = Category.objects.create(
            title='Веб-дизайн',
            slug='design'
        )
        self.post = Post.objects.create(
            title='Пост про дизайн',
            slug='design-post',
            content='Текст про дизайн интерфейсов.',
            category=self.category,
            author=self.user,
            published=True
        )

    def test_homepage_status_code(self):
        """Убеждаемся, что главная страница доступна для любого гостя."""
        response = self.client.get(reverse('blog:posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_correct_template(self):
        """Проверяем, что главная страница рендерится через правильный шаблон."""
        response = self.client.get(reverse('blog:index_page'))
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_homepage_shows_published_posts(self):
        """Проверяем, что опубликованный пост выводится в HTML-коде главной страницы."""
        response = self.client.get(reverse('blog:posts_list'))
        self.assertContains(response, 'Пост про дизайн')

    def test_homepage_hides_draft_posts(self):
        """Убеждаемся, что неопубликованные статьи (черновики) не выводятся на главной."""
        Post.objects.create(
            title='Черновик статьи',
            slug='draft-article',
            content='Секретные наброски.',
            category=self.category,
            author=self.user,
            published=False  # Пост скрыт от публикации
        )
        response = self.client.get(reverse('blog:posts_list'))
        # Опубликованный пост должен быть виден
        self.assertContains(response, 'Пост про дизайн')
        # Скрытый черновик должен отсутствовать на странице
        self.assertNotContains(response, 'Черновик статьи')

    def test_post_detail_page_status_code(self):
        """Убеждаемся, что страница детального просмотра статьи доступна по её slug."""
        response = self.client.get(reverse('blog:post_detail', kwargs={'post_slug': self.post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_template(self):
        """Проверяем использование верного шаблона для детальной страницы."""
        response = self.client.get(reverse('blog:post_detail', kwargs={'post_slug': self.post.slug}))
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_page_context(self):
        """Убеждаемся, что в контекст шаблона передается именно наш объект статьи."""
        response = self.client.get(reverse('blog:post_detail', kwargs={'post_slug': self.post.slug}))
        self.assertEqual(response.context['post'], self.post)

    def test_post_detail_returns_404(self):
        """Проверяем, что обращение по несуществующему slug возвращает ошибку 404."""
        response = self.client.get(reverse('blog:post_detail', kwargs={'post_slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)
