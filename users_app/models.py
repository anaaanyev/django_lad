from django.contrib.auth.models import User
from django.db import models
from PIL import Image   # Импортируем Image из Pillow для работы с графикой


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="Пользователь")
    bio = models.TextField(blank=True, verbose_name="Биография")
    social_link = models.URLField(blank=True, verbose_name="Ссылка на соцсеть")
    avatar = models.ImageField(
        upload_to="avatars/",       # Папка внутри MEDIA_ROOT (media/avatars/)
        blank=True,                 # Поле необязательное в формах
        null=True,                  # Допускает пустое значение в базе данных
        verbose_name="Аватар"
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"

    def save(self, *args, **kwargs):
        # 1. Сначала вызываем родительский метод save, чтобы файл записался на диск
        super().save(*args, **kwargs)

        # 2. Если аватар был загружен — сжимаем его
        if self.avatar:
            # Открываем изображение по его физическому пути на диске
            image = Image.open(self.avatar.path)

            # Если ширина или высота картинки превышает 300 пикселей
            if image.width > 300 or image.height > 300:
                output_size = (300, 300)
                # Метод thumbnail бережно сжимает картинку с сохранением пропорций
                image.thumbnail(output_size)
                # Перезаписываем файл на сервере
                image.save(self.avatar.path)
