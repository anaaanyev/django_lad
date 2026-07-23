# from tinymce import models as tinymce_models
from PIL import Image
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.postgres.indexes import GinIndex


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
    published = models.BooleanField(default=False, verbose_name="Опубликовать статью")

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

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
        verbose_name="Обложка"
    )

    class Meta:
        ordering = ("-created_at", )
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"
        indexes = [
            GinIndex(
                fields=["title", "content"],
                name="post_title_content_gin",
                opclasses=["gin_trgm_ops", "gin_trgm_ops"]
            )
        ]


    def increase_views_count(self):
        """Увеличивает число просмотров статьи"""
        self.views_count += 1
        self.save()

    # https://www.youtube.com/watch?v=QFYIEwDkepM&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl&index=23
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_slug": self.slug})

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.width > 1200 or image.height > 1200:
                output_size = (1200, 1200)
                image.thumbnail(output_size)
                image.save(self.image.path)
