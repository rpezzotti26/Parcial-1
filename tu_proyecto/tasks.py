from app import celery, mail
from flask_mail import Message

@celery.task
def send_async_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients, body=body)
    with mail.app.app_context():
        try:
            mail.send(msg)
            print(f"Correo electrónico enviado a {recipients}")
        except Exception as e:
            print(f"Error al enviar el correo electrónico a {recipients}: {e}")