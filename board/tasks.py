from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives


@shared_task
def send_mail_new_item(get_absolute_url, user, email):

    send_mail(
        subject='Ваше объявление успешно размещено на сайте!',
        message=(f'{user}, Ваше объявление успешно размещено на сайте!\n'
                 f'Ссылка на него http://127.0.0.1:8000{get_absolute_url}'),
        from_email=None,
        recipient_list=[email],
    )

@shared_task
def send_mail_reply_created(header, text, get_absolute_url, customer, seller, sel_mail, cus_mail):

    subject = f'Вы получили отклик на свое объявление {header}'

    text_content = (
        f'{seller}, Ваше объявление пользуется спросом, получен отклик!\n'
        f'{customer} ждет Вашего решения. Емаил покупателя: {cus_mail}\n'
        f'Лот: {header}\n'
        f'Предложение {customer}: "{text}"\n\n'
        f'Ссылка на лот: http://127.0.0.1{get_absolute_url}'
    )

    html_content = (
        f'{seller}, Ваше объявление пользуется спросом, получен отклик!<br>'
        f'{customer} ждет Вашего решения. Емаил покупателя: {cus_mail}<br>'
        f'Лот: {header}<br>'
        f'Предложение {customer}: "{text}"<br><br>'
        f'<a href="http://127.0.0.1:8000{get_absolute_url}">'
        f'Ссылка на лот</a>'
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to = sel_mail

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def send_mail_reply_accepted(customer, cus_mail, seller, sel_mail, text, get_absolute_url, header):

    subject = f'{customer}, Ваш отклик был принят!'

    text_content = (
        f'Хорошие новости, Ваше предложение было принято!\n'
        f'{seller} ждет от Вас письма для продолжения сделки, его почта: {sel_mail}\n'
        f'Лот: {header}\n'
        f'Ваше предложение: "{text}"\n\n'
        f'Ссылка на лот: http://127.0.0.1:8000{get_absolute_url}'
    )

    html_content = (
        f'Хорошие новости, Ваше предложение было принято!<br>'
        f'{seller} ждет от Вас письма для продолжения сделки, его почта: {sel_mail}<br>'
        f'Лот: {header}<br>'
        f'Ваше предложение: "{text}"<br><br>'
        f'<a href="http://127.0.0.1:8000{get_absolute_url}">'
        f'Ссылка на лот</a>'
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to = cus_mail

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def send_mail_verify_code_from_view(username, code, email):

    send_mail(
        subject='Код подтверждения',
        message=f'{username} для завершения регистрации на сайте введите код подтверждения\n'
                f'{code}',
        from_email=None,
        recipient_list=[email],
    )
