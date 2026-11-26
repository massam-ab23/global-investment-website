from django.contrib.auth.decorators import login_required
from .models import Notification
from projects.models import Activity


def languages_processor(request):
    return {
        'available_languages': [
            ('en', 'English'),
            ('ar', 'Arabic'),
            ('ti', 'Eritrean Tigrinya'),
            ('sv', 'Svenska'),
            ('de', 'German'),
            ('ru', 'Russian'),
            ('zh-hans', 'Chinese'),
            ('it', 'Italian'),
            ('fr', 'French'),
        ]
    }


def unread_notifications(request):
    """
    Adds unread notification count to the template context.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}