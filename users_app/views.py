from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

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
