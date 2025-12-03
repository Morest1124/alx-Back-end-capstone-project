import logging
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User, Profile, NotificationPreferences, UserPreferences


logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Logs when a user successfully logs in.
    """
    logger.info(f"User '{user.username}' (ID: {user.id}) logged in from IP: {request.META.get('REMOTE_ADDR')}")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile for a new User.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """
    Create NotificationPreferences and UserPreferences for a new User.
    """
    if created:
        NotificationPreferences.objects.create(user=instance)
        UserPreferences.objects.create(user=instance)
