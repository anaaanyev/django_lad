from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from blog_app.models import Category, Post


class AuthorizationTest(TestCase):
    """Набор тестов для проверки прав доступа и POST-запросов создания контента."""

    def setUp(self):
        """Создаем общие записи для тестов авторизации."""
        self.user = User.objects.create_user(
            username='editor',
            password='securepassword123'
        )
        self.category = Category.objects.create(
            title='Базы данных',
            slug='database'
        )

    def test_create_post_anonymous_redirect(self):
        """Проверяем, что неавторизованного пользователя перенаправляет на страницу входа."""
        response = self.client.get(reverse('blog:posts_create'))
        # Ожидаем редирект (код ответа 302)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что адрес перенаправления содержит путь страницы входа
        self.assertIn('/users/login/', response.url)

    def test_create_post_page_accessible_for_authenticated_users(self):
        """Проверяем, что авторизованный пользователь успешно открывает страницу создания статьи."""
        # Авторизуем пользователя в нашем виртуальном браузере
        self.client.login(username='editor', password='securepassword123')
        response = self.client.get(reverse('blog:posts_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_post_via_post_request(self):
        """Проверяем, что авторизованный пользователь может успешно создать статью через POST."""
        self.client.login(username='editor', password='securepassword123')

        # Отправляем POST-запрос с данными формы
        response = self.client.post(reverse('blog:posts_create'), data={
            'title': 'Пост созданный в тесте',
            'slug': 'post-sozdannyi-v-teste',
            'content': 'Контент созданный с помощью автотеста.',
            'category': self.category.pk,
            'published': True
        })

        # 1. Проверяем редирект (после успешного сохранения Django перенаправляет)
        self.assertEqual(response.status_code, 302)

        # 2. Проверяем, что запись действительно сохранилась в базе данных
        post_exists = Post.objects.filter(slug='post-sozdannyi-v-teste').exists()
        self.assertTrue(post_exists)
