from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from dashboard.models import Notification

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        user_name = instance.username or instance.email or "Anonymous"
        Notification.objects.create(
            user=instance,  # jo user notification ka owner hoga
            category="user",
            notification_type="user_registered",
            message=f"New user registered: {user_name}. "
            f"<a href='{instance.get_absolute_url()}'>View Profile</a>",
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(instance),
        )
