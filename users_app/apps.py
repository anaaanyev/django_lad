from django.apps import AppConfig


class UsersAppConfig(AppConfig):
    name = "users_app"
    verbose_name = "Профили пользователей"

    def ready(self):
        # Регистрируем сигналы при старте приложения
        import users_app.signals # noqa: F401


"""
[!IMPORTANT] Никогда не импортируйте модели и сигналы на самом верху файла apps.py.
На этапе сборки приложений Django еще не готов к работе с базой данных,
и такой импорт вызовет критическую ошибку AppRegistryNotReady
"""
