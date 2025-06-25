from django.core.mail import send_mail
from django.db import transaction
from django.conf import settings


def send_email(subject, message, recipient_list, fail_silently=False):
    """
    Sends an email using Django's send_mail function.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        recipient_list (list): A list of recipient email addresses.
        fail_silently (bool): If True, errors during sending will be ignored.
    """
    try:
        with transaction.atomic():
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=fail_silently,
            )
        return True
    except Exception as e:
        if not fail_silently:
            raise e
        # Log the error if fail_silently is True
        # You can use logging here if needed
        print(f"Failed to send email: {e}")
        return False
