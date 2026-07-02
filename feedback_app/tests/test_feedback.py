from django.test import TestCase
from django.urls import reverse

from feedback_app.models import Feedback
from feedback_app.forms import FeedbackForm

class FeedbackTest(TestCase):
    def test_create_feedback_post_via_post_request(self):
        response = self.client.post(reverse('feedback:index_page'), data={
            'name': 'Sergey',
            'email': 'django@gmail.com',
            'message': 'Contact with me',
            'subject': 'collaboration',
        })

        self.assertEqual(response.status_code, 302)

        feedback_exists = Feedback.objects.filter(
            name='Sergey',
            email='django@gmail.com',
            message='Contact with me',
            subject='collaboration'
        ).exists()
        self.assertTrue(feedback_exists)

    def test_form_invalid_email_address(self):
        form = FeedbackForm(data={
            'name': 'Sergey',
            'email': 'django@gmail',
            'message': 'Contact with me',
            'subject': 'collaboration',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

        self.assertEqual(Feedback.objects.all().count(), 0)
