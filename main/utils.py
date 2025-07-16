# emailing/utils.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(data):
    msg = MIMEMultipart()
    msg['From'] = data['from_email']
    msg['To'] = ', '.join(data['to_email'])
    msg['Subject'] = data['subject']

    if data.get("cc"):
        msg['Cc'] = ', '.join(data['cc'])

    msg.attach(MIMEText(data['message'], 'plain'))

    smtp_class = smtplib.SMTP_SSL if data.get('use_ssl') else smtplib.SMTP
    server = smtp_class(data['smtp_host'], data['smtp_port'])
    if data.get('use_tls') and not data.get('use_ssl'):
        server.starttls()
    server.login(data['smtp_username'], data['smtp_password'])
    all_recipients = data['to_email'] + data.get('cc', []) + data.get('bcc', [])
    server.sendmail(data['from_email'], all_recipients, msg.as_string())
    server.quit()
