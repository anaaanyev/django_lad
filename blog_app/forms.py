from django import forms
from blog_app.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'category']
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
