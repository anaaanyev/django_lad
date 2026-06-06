from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    # Название категории (например: "Технологии", "Дизайн")
    title = models.CharField(max_length=100, verbose_name="Название")

    # unique=True гарантирует, что в базе не будет двух категорий с одинаковым slug.
    slug = models.SlugField(unique=True, verbose_name="URL")

    class Meta:
        ordering = ("id",)
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def get_absolute_url(self):
        return reverse("blog:category_detail", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL")
    # content = tinymce_models.HTMLField(verbose_name="Содержимое")
    content = models.TextField(verbose_name="Содержимое")
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )

    # Флаг "Черновик" или "Опубликовано". По умолчанию - черновик.
    published = models.BooleanField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    # Счетчик просмотров
    views_count = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")

    # Отношение "Многие-к-Одному". Каждая статья должна принадлежать какой-то категории
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Категория"
    )

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"


    def increase_views_count(self):
        self.views_count += 1
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_slug": self.slug})

    def __str__(self):
        return self.title
