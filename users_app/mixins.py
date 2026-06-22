from users_app.models import Profile

class ProfileGetOrCreateMixin:
    def get_object(self, queryset=None):
        # get_or_create вернёт кортеж (объект, создан_ли)
        # Если профиля ещё нет — он будет создан автоматически
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile
