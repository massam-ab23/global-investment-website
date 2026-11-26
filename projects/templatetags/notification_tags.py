from django import template  # Import the template module
from projects.models import Notification  # Import your Notification model

register = template.Library()  # Register the custom template tags or filters

@register.filter
def unread_notifications(user):
    """Filter to get unread notifications for a user."""
    if user.is_authenticated:
        return Notification.objects.filter(user=user, is_read=False)
    return Notification.objects.none()
