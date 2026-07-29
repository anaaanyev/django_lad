import datetime
from django.conf import settings
import jwt

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_email(user: User):
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    token = default_token_generator.make_token(user=user)

    activation_url = f"http://127.0.0.1:8000/api/v2/auth/activate/{uid}/{token}"

    html_content = render_to_string(
        'emails/activation.html',
        context={
            'username': user.username,
            'activation_url': activation_url
        }
    )

    msg = EmailMessage(
        subject="Подтверждение регистрации в блоге",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.content_subtype = 'html'
    msg.send()

    return

def create_access_token(user_id: int, username: str) -> str:
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(payload=payload, key=settings.JWT_SECRET_KEY, algorithm="HS256")

    return token
