from django.shortcuts import render, redirect
from feedback_app.forms import FeedbackForm
from feedback_app.models import Feedback

def feedback_view(request):
    form = FeedbackForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            Feedback.objects.create(name=name, email=email, message=message)
            return redirect('blog:index_page')
    return render(request, 'feedback/feedback_page.html', context={'form': form})
