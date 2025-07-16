from django.db import models

class SentEmail(models.Model):
    to_email = models.TextField()
    from_email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    smtp_host = models.CharField(max_length=255)
    smtp_username = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    response = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} -> {self.to_email}"
