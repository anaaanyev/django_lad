from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, verbose_name="URL")
    content = models.TextField()
    published = models.BooleanField(default=False)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
