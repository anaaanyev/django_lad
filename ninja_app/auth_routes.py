from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from ninja import Router
from ninja.errors import HttpError

from ninja_app.schemas import RegisterOutSchema, RegisterInSchema, ActivationOutSchema, LoginOutSchema, LoginInSchema

auth_router = Router(tags=["Authentication"])


@auth_router.post(path="/register", response={201: RegisterOutSchema})
def register(request, payload: RegisterInSchema):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(status_code=400, message="Пользователь с таким логином уже существует")

    if User.objects.filter(email=payload.email).exists():
        raise HttpError(status_code=400, message="Пользователь с такой почтой уже существует")

    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        is_active=False
    )

    uid = urlsafe_base64_encode(force_bytes(user.pk))

    token = default_token_generator.make_token(user=user)

    activation_url = f"http://127.0.0.1:8000/api/v2/auth/activate/{uid}/{token}"

    send_mail(
        subject="Подтверждение регистрации в блоге",
        message=(
            f"Привет, {user.username}!\n\n"
            f"Для активации вашего аккаунта перейдите по ссылке:\n"
            f"{activation_url}\n\n"
            f"Ссылка будет действительна в течении 3 дней."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )

    return 201, RegisterOutSchema(
        message="Регистрация успешна",
        username=user.username,
        email=user.email
    )


@auth_router.get(path="/activate/{uid}/{token}", response={200: ActivationOutSchema, 400: ActivationOutSchema})
def activate_account(request, uid: str, token: str):
    try:
        user_pk = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_pk)
    except (TypeError, ValueError, User.DoesNotExist):
        return 400, ActivationOutSchema(
            message="Ссылка активации не действительна",
            is_activated=False
        )

    if not default_token_generator.check_token(user=user, token=token):
        return 400, ActivationOutSchema(
            message="Ссылка активации устарела",
            is_activated=False
        )

    user.is_active = True
    user.save()

    return 200, ActivationOutSchema(
        message=f"Аккаунт {user.username} успешно активирован",
        is_activated=True
    )

@auth_router.post(path="/login", response={200: LoginOutSchema, 401: LoginOutSchema})
def login_check(request, payload: LoginInSchema):
    user = authenticate(
        request=request,
        username=payload.username,
        password=payload.password
    )

    if user is None:
        return 401, LoginOutSchema(
            success=False,
            message="Неверный логин или пароль"
        )

    return 201, LoginOutSchema(
        success=True,
        message="Доброе пожаловать",
        username=user.username,
        email=user.email,
        is_staff=user.is_staff
    )
