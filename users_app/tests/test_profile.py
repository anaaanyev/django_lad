from django.test import TestCase
from django.urls import reverse

from users_app.models import Profile
from django.contrib.auth.models import User


class ProfileTest(TestCase):
    def test_creating_user_automatically_creates_profile(self):
        User.objects.create_user(username='user01', password='test_user_01')
        self.assertTrue(Profile.objects.filter(user__username='user01').exists())

    def test_anonymous_user_redirected_to_login_on_profile_edit(self):
        response = self.client.get(reverse('users:profile_edit'))
        self.assertTrue(response.status_code, 302)
