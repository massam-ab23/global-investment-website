from users.models import CustomUser
from projects.models import Activity

def unread_notifications(request):
    if request.user.is_authenticated:
        count = Activity.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
