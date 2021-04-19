"""Notify."""
from django.core.mail import send_mail


def notify(email_to):
    """Notify Method."""
    email_send(email_to)
    # telegram_notify(email_to)


def email_send(email_to):
    """Notify Email."""
    send_mail(
        'Notifying from Blog Django',
        'We notify you!',
        'blogadmin@gmail.com',
        [email_to],
        fail_silently=False
    )


def telegram_notify(email_to):
    """Notify Telegram."""
    pass
