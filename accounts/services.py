"""Notifications persistantes et e-mails applicatifs."""
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Notifications


def notify(user, title, message, *, email_subject=None, email_message=None):
    """Enregistre la notification et envoie un e-mail sans bloquer le parcours."""
    Notifications.objects.create(user=user, title=title, message=message, is_read=0, created_at=timezone.now())
    if user.email:
        try:
            send_mail(email_subject or title, email_message or message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)
        except Exception:
            pass
