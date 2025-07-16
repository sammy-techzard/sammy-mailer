# emailing/urls.py
from django.urls import path
from .views import SendEmailAPI

urlpatterns = [
    path('send-email/', SendEmailAPI.as_view()),
]
