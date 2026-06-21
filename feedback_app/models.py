from django.db import models

# Create your models here.
class Feedback(models.Model):
    SUBJECT_CHOICES = [
        ('default', 'Выберите тему обращения'),
        ('tech', 'Технический вопрос'),
        ('collaboration', 'Сотрудничество'),
        ('complaint', 'Жалоба'),
        ('other', 'Другое'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя отправителя')
    email = models.EmailField(verbose_name='Почта отправителя')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    subject = models.CharField(max_length=150, choices=SUBJECT_CHOICES, verbose_name='Тема обращения')

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Обратную связь"
        verbose_name_plural = "Сообщения обратной связи"

    def __str__(self):
        return f"Сообщение от {self.name} ({self.email})"
