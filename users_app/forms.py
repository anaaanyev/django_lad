from django import forms
from users_app.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "social_link"]

        widgets = {
            "bio": forms.Textarea(attrs={'class': 'form-control'}),
            "social_link": forms.URLInput(attrs={'class': 'form-control'})
        }

        labels = {
            'bio': 'Расскажите о себе',
            'social_link': 'Ваша ссылка на соцсеть',
        }
