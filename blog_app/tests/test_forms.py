from django.test import TestCase
from blog_app.forms import PostForm
from blog_app.models import Category


class PostFormTest(TestCase):
    """Набор тестов для проверки формы добавления статей (PostForm)."""

    def setUp(self):
        """Создаем категорию, так как форма требует ID связанной записи."""
        self.category = Category.objects.create(
            title='Новости',
            slug='news'
        )

    def test_form_with_valid_data(self):
        """Проверяем, что заполненная корректными данными форма валидна."""
        form_data = {
            'title': 'Интересный пост',
            'slug': 'interesting-post',
            'content': 'Текст интересного поста.',
            'category': self.category.pk,  # Передаем первичный ключ категории (ID)
            'published': True
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_empty_title(self):
        """Проверяем, что форма не проходит валидацию, если поле заголовка пустое."""
        form_data = {
            'title': '',  # Обязательное поле пустое
            'slug': 'empty-title-post',
            'content': 'Текст поста.',
            'category': self.category.pk
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Проверяем, что ошибка зафиксирована именно на поле title
        self.assertIn('title', form.errors)

    def test_form_invalid_with_empty_content(self):
        """Проверяем, что форма не проходит валидацию, если отсутствует текст статьи."""
        form_data = {
            'title': 'Заголовок поста',
            'slug': 'empty-content-post',
            'content': '',  # Текст статьи отсутствует
            'category': self.category.pk
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
