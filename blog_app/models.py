from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    # Название категории (например: "Технологии", "Дизайн")
    title = models.CharField(max_length=100)

    # Идентификатор для URL (например: "tehnologii")
    # unique=True гарантирует, что в базе не будет двух категорий с одинаковым slug.
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ("id",)


    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    # Флаг "Черновик" или "Опубликовано". По умолчанию - черновик.
    published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Счетчик просмотров
    views_count = models.PositiveIntegerField(default=0)

    # Отношение "Многие-к-Одному". Каждая статья должна принадлежать какой-то категории
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="posts"
    )


    def increase_views_count(self):
        self.views_count += 1
        self.save()

    def __str__(self):
        return self.title
