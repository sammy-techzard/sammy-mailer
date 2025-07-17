# emailing/views.py
import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendEmailSerializer, UploadEmailAttachmentSerializer
from .utils import send_email
from .models import SentEmail
from drf_yasg.utils import swagger_auto_schema
from django.core.files.storage import default_storage
from rest_framework.parsers import MultiPartParser, FormParser

class SendEmailAPI(APIView):
    """
    Sends an email using the given SMTP credentials and logs the attempt.
    """
    permission_classes = []  # Caution: no auth here
    @swagger_auto_schema(request_body=SendEmailSerializer)
    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                send_email(data)
                SentEmail.objects.create(
                    to_email=', '.join(data['to_email']),
                    from_email=data['from_email'],
                    subject=data['subject'],
                    message=data['message'],
                    smtp_host=data['smtp_host'],
                    smtp_username=data['smtp_username'],
                    status='success'
                )
                return Response({'message': 'Email sent successfully'}, status=200)
            except Exception as e:
                SentEmail.objects.create(
                    to_email=', '.join(data['to_email']),
                    from_email=data['from_email'],
                    subject=data['subject'],
                    message=data['message'],
                    smtp_host=data['smtp_host'],
                    smtp_username=data['smtp_username'],
                    status='error',
                    response=str(e)
                )
                return Response({'error': str(e)}, status=500)
        return Response(serializer.errors, status=400)



class UploadAttachmentView(APIView):
    """
    Uploads an email attachment to the server and returns its unique storage filename.
    """
    permission_classes = []
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload a file to be used as an email attachment.",
        request_body=UploadEmailAttachmentSerializer
    )
    def post(self, request):
        serializer = UploadEmailAttachmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data['file']
        # Create unique filename
        file_extension = os.path.splitext(file.name)[1]
        unique_name = f"{uuid.uuid4().hex}{file_extension}"
        save_path = os.path.join('email_attachments', unique_name)

        file_path = default_storage.save(save_path, file)
        return Response({'filename': file_path}, status=status.HTTP_201_CREATED)