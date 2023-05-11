from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_mail_verify_code(username, code, email):

    send_mail(
        subject='Код подтверждения',
        message=f'{username} для завершения регистрации на сайте введите код подтверждения\n'
                f'{code}',
        from_email=None,
        recipient_list=[email],
    )