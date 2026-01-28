import smtplib
from email.message import EmailMessage
from config import ALERT_EMAIL_FROM, ALERT_EMAIL_TO, ALERT_EMAIL_SMTP

def send_alert(subject, body, recipients=None):
    if recipients is None:
        recipients = ALERT_EMAIL_TO

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = ALERT_EMAIL_FROM
    msg['To'] = ','.join(recipients)

    with smtplib.SMTP(ALERT_EMAIL_SMTP) as s:
        s.send_message(msg)
