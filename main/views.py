# emailing/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendEmailSerializer
from .utils import send_email
from .models import SentEmail
from drf_yasg.utils import swagger_auto_schema

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
