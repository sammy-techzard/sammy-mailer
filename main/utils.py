# emailing/utils.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.conf import settings

def send_email(data):
    msg = MIMEMultipart()
    msg['From'] = data['from_email']
    msg['To'] = ', '.join(data['to_email'])
    msg['Subject'] = data['subject']

    if data.get("cc"):
        msg['Cc'] = ', '.join(data['cc'])

    msg.attach(MIMEText(data['message'], 'html'))

    # Attach files by filename
    for filename in data.get('attachments', []):
        abs_path = os.path.join(settings.MEDIA_ROOT, filename)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Attachment file not found: {filename}")

        with open(abs_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(filename)}"')
            msg.attach(part)

    smtp_class = smtplib.SMTP_SSL if data.get('use_ssl') else smtplib.SMTP
    server = smtp_class(data['smtp_host'], data['smtp_port'])
    if data.get('use_tls') and not data.get('use_ssl'):
        server.starttls()
    server.login(data['smtp_username'], data['smtp_password'])
    all_recipients = data['to_email'] + data.get('cc', []) + data.get('bcc', [])
    server.sendmail(data['from_email'], all_recipients, msg.as_string())
    server.quit()
