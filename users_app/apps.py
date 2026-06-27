from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = "users_app"
    verbose_name = "Профили пользователей"

    def ready(self):
        import users_app.signals # noqa: F401
