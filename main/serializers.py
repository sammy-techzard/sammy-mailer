from rest_framework import serializers

class SendEmailSerializer(serializers.Serializer):
    smtp_host = serializers.CharField()
    smtp_port = serializers.IntegerField()
    smtp_username = serializers.CharField()
    smtp_password = serializers.CharField()
    use_tls = serializers.BooleanField(default=True)
    use_ssl = serializers.BooleanField(default=False)

    from_email = serializers.EmailField()
    to_email = serializers.ListField(child=serializers.EmailField())
    cc = serializers.ListField(child=serializers.EmailField(), required=False)
    bcc = serializers.ListField(child=serializers.EmailField(), required=False)

    subject = serializers.CharField()
    message = serializers.CharField()

    attachments = serializers.ListField(child=serializers.CharField(), required=False)
class UploadEmailAttachmentSerializer(serializers.Serializer):
    """
    Serializer to handle uploading a single email attachment file.
    """
    file = serializers.FileField()