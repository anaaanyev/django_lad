from django.shortcuts import render, redirect
from feedback_app.forms import FeedbackForm
from feedback_app.models import Feedback

def feedback_view(request):
    form = FeedbackForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        # У обычной формы forms.Form НЕТ метода .save()!
        # Извлекаем очищенные и приведенные к типам данные из cleaned_data
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')
        subject = form.cleaned_data.get('subject')

        # Вручную создаем запись в таблице базы данных через ORM
        Feedback.objects.create(name=name, email=email, message=message, subject=subject)

        # https://developer.mozilla.org/ru/docs/Learn_web_development/Extensions/Server-side/Django/Sessions
        # Создаем для пользователя ключ в сессии, чтобы он получил доступ к странице feedback/success/
        request.session['feedback_success'] = True

        return redirect('feedback:feedback_success')

    return render(request, 'feedback/feedback_page.html', context={'form': form})


def feedback_success(request):
    # Исключаем возможность любому пользователю попасть на страницу feedback/success/
    if not request.session.get('feedback_success', False):
        # Редирект на страницу обратная связь
        return redirect('feedback:index_page')

    # Удаляем из сессии ключ 'feedback_success' для пользователя который заполнил форму и нажал на кнопку отправить
    del request.session['feedback_success']

    # Отображаем страницу разово для тех кто заполнил форму и отправил ее
    return render(request, 'feedback/success.html')
