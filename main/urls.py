# emailing/urls.py
from django.urls import path
from .views import SendEmailAPI, UploadAttachmentView

urlpatterns = [
    path('send-email/', SendEmailAPI.as_view()),
    path('upload-email-attachment/', UploadAttachmentView.as_view()),
]
