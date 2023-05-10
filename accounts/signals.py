import random

from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.dispatch import receiver

from accounts.models import Profile


def random_code():
    random.seed()
    return random.randint(1000, 9999)


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
        code = random_code()
        Profile.objects.create(user=user, code=code)

        send_mail(
                subject='Код подтверждения',
                message=f'{user.username} для завершения регистрации на сайте введите код подтверждения\n'
                        f'{code}',
                from_email=None,
                recipient_list=[user.email],
        )