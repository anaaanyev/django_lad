from django.core.exceptions import PermissionDenied


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        # Вызываем get_context_data() следующего класса в цепочке MRO
        context = super().get_context_data(**kwargs)
        # Добавляем свои данные
        if self.title:
            context['title'] = self.title
        return context


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # Проверяем: пользователь авторизован И является сотрудником?
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied("Доступ только для сотрудников")
        # Проверка пройдена — передаём управление дальше по цепочке MRO
        return super().dispatch(request, *args, **kwargs)


class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user.username != post.author.username:
            raise PermissionDenied("Доступно только автору статьи")
        return super().dispatch(request, *args, **kwargs)


class AuthorOrStaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if not request.user.is_authenticated or not request.user.is_staff or self.request.user.username != post.author.username:
            raise PermissionDenied("Доступно только модератору и автору статьи")
        return super().dispatch(request, *args, **kwargs)
