from django import template  
from projects.models import Notification  

register = template.Library()  

@register.filter
def unread_notifications(user):
    """Filter to get unread notifications for a user."""
    if user.is_authenticated:
        return Notification.objects.filter(user=user, is_read=False)
    return Notification.objects.none()
