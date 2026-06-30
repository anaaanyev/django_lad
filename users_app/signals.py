from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users_app.models import Profile

@receiver(signal=post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создает профиль при создании нового пользователя."""

    # Флаг created равен True только если объект создается впервые
    if created:
        Profile.objects.create(user=instance)


"""
[!WARNING] Всегда проверяйте параметр created.
Сигнал post_save срабатывает как при создании объекта,
так и при его любом изменении (например, при смене пароля).
Если не проверить created, Django попытается создать еще один Profile
для существующего пользователя и выдаст ошибку IntegrityError.
"""
