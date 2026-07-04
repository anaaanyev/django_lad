from django.test import TestCase
from blog_app.models import Category
from django.db import IntegrityError


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Первая', slug='same-slug')

    def test_category_fields_creation(self):
        self.assertEqual(self.category.title, 'Первая')
        self.assertEqual(self.category.slug, 'same-slug')

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), 'Первая')

    def test_category_slug_unique(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(title='Вторая', slug='same-slug')
