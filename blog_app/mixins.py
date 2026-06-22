from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from blog_app.models import Post


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
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        if self.request.user.username != post.author.username:
            raise PermissionDenied("Доступно только автору статьи")
        return super().dispatch(request, *args, **kwargs)
