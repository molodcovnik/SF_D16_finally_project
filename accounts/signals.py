import random

from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.dispatch import receiver

from accounts.models import Profile
from .tasks import send_mail_verify_code


def random_code():
    random.seed()
    return random.randint(1000, 9999)


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
        code = random_code()
        username = user.username
        email = user.email
        Profile.objects.create(user=user, code=code)

        send_mail_verify_code.delay(username, code, email)
