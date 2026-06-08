from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Announcement, Register


@receiver(post_save, sender=Announcement)
def send_announcement_email(sender, instance, created, **kwargs):

    if not instance.send_notification:
        return

    subject = f"📢 Konkiyazhikam Kudumbayogam - {instance.title}"

    for member in Register.objects.exclude(email=""):

        message = f"""Dear {member.first_name},

Greetings from Konkiyazhikam Kudumbayogam.

A new announcement has been published for all members.

━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 ANNOUNCEMENT
{instance.title}

📅 DATE
{instance.date}

📝 DETAILS

{instance.message}

👤 ISSUED BY
{instance.issued_by}

━━━━━━━━━━━━━━━━━━━━━━━━━━

Website:
https://www.konkiyazhikamkudumbayogam.com/

Thank you for being a valued member of our family community.

Warm Regards,

Konkiyazhikam Kudumbayogam
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [member.email],
            fail_silently=False,
        )

    Announcement.objects.filter(pk=instance.pk).update(
        send_notification=False
    )