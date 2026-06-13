from django.urls import path
from feedback_app import views

app_name = 'feedback'

urlpatterns = [
    path('', views.feedback_view, name='index_page'),
]
