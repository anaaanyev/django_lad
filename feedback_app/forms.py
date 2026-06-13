from django import forms

SUBJECT_CHOICES = [
    ('default', 'Выберите тему обращения'),
    ('tech', 'Технический вопрос'),
    ('collaboration', 'Сотрудничество'),
    ('complaint', 'Жалоба'),
    ('other', 'Другое'),
]


class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше имя',
            }
        )
    )

    email = forms.EmailField(
        label='Ваша эл.почта',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу почту',
            }
        )
    )

    message = forms.CharField(
        label='Ваше обращение',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите ваше обращение',
                'rows': 5,
            }
        )
    )

    subject = forms.ChoiceField(
        label='Тема обращения',
        choices=SUBJECT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
