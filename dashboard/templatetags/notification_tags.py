from django import template

from dashboard.models import Notification

register = template.Library()


@register.simple_tag
def get_user_notifications(user, limit=10):
    if user.is_authenticated:
        return (
            Notification.objects.for_user(user)
            .filter(is_read=False)
            .order_by("-created_at")[:limit]
        )

    return []
