# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Announcement, Register


@receiver(post_save, sender=Announcement)
def send_announcement_email(sender, instance, created, **kwargs):

    if not created:
        return

    recipients = list(
        Register.objects.exclude(email="")
        .values_list("email", flat=True)
    )

    if not recipients:
        return

    subject = f"New Announcement: {instance.title}"

    message = f"""
Title: {instance.title}

Date: {instance.date}

Message:
{instance.message}

Issued By:
{instance.issued_by}
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )