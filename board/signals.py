import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives

from django.conf import settings
from .models import Reply, Item
from .tasks import send_mail_new_item, send_mail_reply_created, send_mail_reply_accepted

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

        customer = instance.user.username
        cus_mail = instance.user.email
        seller = instance.item.user.username
        sel_mail = instance.item.user.email

        send_mail_reply_accepted.delay(customer, cus_mail, seller, sel_mail, instance.text,
                                       instance.item.get_absolute_url(), instance.item.header)
