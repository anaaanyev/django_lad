from django import forms
from blog_app.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'title': 'Заголовок статьи',
            'content': 'Содержание статьи',
            'author': 'Автор',
            'category': 'Категория',
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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Ошибка! Заголовок должен быть длиннее 5 символов.")
        return title


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        label="Поиска по статьям",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текст запроса',
        })
    )
