from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from ninja import Router
from ninja.errors import HttpError

from ninja_app.utils import send_email, create_access_token
from ninja_app.schemas import (
    RegisterOutSchema, RegisterInSchema, ActivationOutSchema, LoginOutSchema, LoginInSchema, ResendActivationSchema
)

auth_router = Router(tags=["Authentication"])


@auth_router.post(path="/register", response={201: RegisterOutSchema},
                  summary="Регистрация нового пользователя с подтверждением по Email")
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

    send_email(user=user)

    return 201, RegisterOutSchema(
        message="Регистрация успешна",
        username=user.username,
        email=user.email
    )


@auth_router.get(path="/activate/{uid}/{token}", response={200: ActivationOutSchema, 400: ActivationOutSchema},
                 summary="Активация учётной записи по ссылке из письма")
def activate_account(request, uid: str, token: str):
    try:
        user_pk = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_pk)
    except (TypeError, ValueError, User.DoesNotExist):
        return 400, ActivationOutSchema(
            message="Ссылка активации не действительна",
            activated=False
        )

    # Проверяем токен: он должен соответствовать пользователю и быть непросроченным
    if not default_token_generator.check_token(user=user, token=token):
        return 400, ActivationOutSchema(
            message="Ссылка активации устарела",
            activated=False
        )

    user.is_active = True
    user.save()

    return 200, ActivationOutSchema(
        message=f"Аккаунт {user.username} успешно активирован",
        activated=True
    )

@auth_router.post(path="/login", response={200: LoginOutSchema, 401: LoginOutSchema},
                  summary="Проверка логина и пароля пользователя")
def login_check(request, payload: LoginInSchema):
    # authenticate проверяет логин, сверяет хеш пароля и проверяет is_active=True
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

    access_token = create_access_token(
        user_id=user.pk,
        username=user.username
    )

    return 200, LoginOutSchema(
        success=True,
        message="Добро пожаловать",
        username=user.username,
        email=user.email,
        is_staff=user.is_staff,
        access_token=access_token
    )

@auth_router.post(path="/resend-activation", response={201: RegisterOutSchema},
                  summary="Запросить повторную активацию аккаунта (для не активированных учётных записей)")
def resend_activation(request, payload: ResendActivationSchema):
    if not User.objects.filter(email=payload.email).exists():
        raise HttpError(status_code=401, message="Почта не найдена в базе данных")

    user = User.objects.get(email=payload.email)

    if user.is_active:
        raise HttpError(status_code=401, message="Аккаунт уже активирован")

    send_email(user=user)

    return 201, RegisterOutSchema(
        message="Новая ссылка с подтверждением аккаунта отправлена на почту",
        username=user.username,
        email=user.email
    )
