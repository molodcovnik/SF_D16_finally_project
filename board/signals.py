import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives

from django.conf import settings
from .models import Reply, Item
from .tasks import send_mail_new_item, send_mail_reply_created

@receiver(post_save, sender=Item)
def item_created(instance, created, **kwargs):
    if created:
        email = instance.user.email
        send_mail_new_item.delay(
            instance.get_absolute_url(), instance.user.username, email
        )



@receiver(post_save, sender=Reply)
def reply_created(instance, created, **kwargs):
    if not created:
        return

    customer = instance.user.username
    cus_mail = instance.user.email
    seller = instance.item.user.username
    sel_mail = instance.item.user.email

    send_mail_reply_created.delay(
        instance.item.header, instance.text, instance.item.get_absolute_url(), customer, seller, sel_mail, cus_mail)


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
