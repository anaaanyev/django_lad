from django import forms
from feedback_app.models import Feedback

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
        choices=Feedback.SUBJECT_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        )
    )
