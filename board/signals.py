from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives

from django.conf import settings
from .models import Reply, Item


@receiver(post_save, sender=Item)
def item_created(instance, created, **kwargs):
    if created:
        send_mail(
            subject='Ваше объявление успешно размещено на сайте!',
            message=(f'{instance.user}, Ваше объявление успешно размещено на сайте!\n' 
                     f'Ссылка на него http://127.0.0.1:8000{instance.get_absolute_url()}'),
            from_email=None,
            recipient_list=[instance.user.email],
            )



@receiver(post_save, sender=Reply)
def reply_created(instance, created, **kwargs):
    if not created:
        return

    subject = f'Вы получили отклик на свое объявление {instance.item.header}'

    text_content = (
        f'{instance.item.user}, Ваше объявление пользуется спросом, получен отклик!\n'
        f'{instance.user} ждет Вашего решения. Емаил покупателя: {instance.user.email}\n'
        f'Лот: {instance.item.header}\n'
        f'Предложение {instance.user}: "{instance.text}"\n\n'
        f'Ссылка на лот: http://127.0.0.1{instance.item.get_absolute_url()}'
    )

    html_content = (
        f'{instance.item.user}, Ваше объявление пользуется спросом, получен отклик!<br>'
        f'{instance.user} ждет Вашего решения. Емаил покупателя: {instance.user.email}<br>'
        f'Лот: {instance.item.header}<br>'
        f'Предложение {instance.user}: "{instance.text}"<br><br>'
        f'<a href="http://127.0.0.1:8000{instance.item.get_absolute_url()}">'
        f'Ссылка на лот</a>'
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to = instance.item.user.email

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Reply)
def reply_accepted(instance, **kwargs):
    if instance.accepted:

        subject = f'{instance.user}, Ваш отклик был принят!'

        text_content = (
            f'Хорошие новости, Ваше предложение было принято!\n'
            f'{instance.item.user} ждет от Вас письма для продолжения сделки, его почта: {instance.item.user.email}\n'
            f'Лот: {instance.item.header}\n'
            f'Ваше предложение: "{instance.text}"\n\n'
            f'Ссылка на лот: http://127.0.0.1{instance.item.get_absolute_url()}'
        )

        html_content = (
            f'Хорошие новости, Ваше предложение было принято!<br>'
            f'{instance.item.user} ждет от Вас письма для продолжения сделки, его почта: {instance.item.user.email}<br>'
            f'Лот: {instance.item.header}<br>'
            f'Ваше предложение: "{instance.text}"<br><br>'
            f'<a href="http://127.0.0.1:8000{instance.item.get_absolute_url()}">'
            f'Ссылка на лот</a>'
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        to = instance.user.email

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
