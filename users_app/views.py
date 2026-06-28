from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, CreateView
from users_app.forms import CustomUserCreationForm

from users_app.forms import ProfileForm
from users_app.models import Profile
from users_app.mixins import ProfileGetOrCreateMixin


class ProfileDetailView(LoginRequiredMixin, ProfileGetOrCreateMixin, DetailView):
    model = Profile
    template_name = "users/profile_detail.html"


class ProfileUpdateView(LoginRequiredMixin, ProfileGetOrCreateMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")


# В функциональных представлениях (FBV) при обработке формы с файлами нужно обязательно передавать request.FILES:
# form = ProfileForm(request.POST, request.FILES, instance=profile)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("blog:index_page")
