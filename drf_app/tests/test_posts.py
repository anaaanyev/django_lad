from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from blog_app.models import Post, Category


class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_api', password='user_api123')
        self.category = Category.objects.create(title='Api Category', slug='api_category')

        Post.objects.create(
            title='API test 1',
            slug='api_test_1',
            content='API test 1',
            author=self.user,
            category=self.category,
        )

        Post.objects.create(
            title='API test 2',
            slug='api_test_2',
            content='API test 2',
            author=self.user,
            category=self.category,
        )

    def test_get_posts_list_success(self):
        response = self.client.get(path='/api/v1/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), 2)

    def test_create_post_authenticated_user_success(self):
        token = self.client.post(path='/api/v1/token/', data={"username": "user_api", "password": "user_api123"})

        response = self.client.post(path='/api/v1/posts/', data={
            "title": "New article",
            "slug": "new_article",
            "content": "something",
            "category": self.category.pk,
            "author": self.user
        }, headers={"Authorization": f'Bearer {token.data["access"]}'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.all().count(), 3)

    def test_create_post_anonymous_user_unauthorized(self):
        response = self.client.post(path='/api/v1/posts/', data={
            "title": "New article",
            "slug": "new_article",
            "content": "something",
            "category": self.category.pk,
            "author": self.user
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.all().count(), 2)
