import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Logs when a user successfully logs in.
    """
    logger.info(f"User '{user.username}' (ID: {user.id}) logged in from IP: {request.META.get('REMOTE_ADDR')}")
