# from tinymce.widgets import TinyMCE
from django.urls import reverse_lazy
from slugify import slugify

from django import forms
from blog_app.models import Post, Category


class PostForm(forms.ModelForm):
    class Meta:
        # Связываем форму с моделью
        model = Post
        # Перечисляем поля, которые пользователь заполняет на сайте
        fields = ['title', 'author', 'category', 'content']

        # Переопределяем виджеты для добавления стилей Bootstrap
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            # 'content': TinyMCE(attrs={'class': 'form-control'}),
        }
        # Перевод подписей полей (labels)
        labels = {
            'title': 'Заголовок статьи',
            'author': 'Автор',
            'category': 'Категория',
            'content': 'Содержание статьи',
        }
        # Текст подсказка для полей
        help_texts = {
            'title': "Минимум 5 символов",
        }

    # https://docs.djangoproject.com/en/6.0/ref/forms/fields/#modelchoicefield
    # https://www.reddit.com/r/djangolearning/comments/urnmgr/django_forms_empty_label_attribute_for_select/
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(self.fields)
        # {'title': <django.forms.fields.CharField object at 0x1066f1580>,
        # 'author': <django.forms.models.ModelChoiceField object at 0x1066f14f0>,
        # 'category': <django.forms.models.ModelChoiceField object at 0x1064cf7a0>,
        # 'content': <django.forms.fields.CharField object at 0x1062cd100>}
        self.fields['author'].empty_label = "Выберите автора"
        self.fields['category'].empty_label = "Выберите категорию"

    # Кастомная валидация заголовка
    def clean_title(self):
        # Данные уже очищены базовой проверкой
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Ошибка! Заголовок должен быть длиннее 5 символов.")
        # Важно: всегда возвращайте значение в конце метода!
        return title

    # def clean(self):
    #     # Получаем словарь очищенных данных от родительского класса
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get('title')
    #     content = cleaned_data.get('content')
    #
    #     if title and content and title.lower() in content.lower():
    #         raise forms.ValidationError("Содержимое статьи не должно дублировать её заголовок!")
    #
    #     return cleaned_data


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,  # Поиск может быть пустым
        label="Поиск по статьям",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите слово для поиска...',
            'hx-get': reverse_lazy('blog:query_posts_list'),
            'hx-trigger': 'keyup changed delay:1s',
            'hx-target': '#query_posts_list',
        })
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок категории'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        if len(title) < 5:
            raise forms.ValidationError("Ошибка! Укажите больше 5 символов")
        elif Category.objects.filter(slug=slug).exists():
            raise forms.ValidationError("Такая категория уже существует")
        return title
