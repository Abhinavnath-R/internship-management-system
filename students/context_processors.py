def unread_notifications_count(request):
    """Provide the unread notification count for the topbar bell."""
    if request.user.is_authenticated and request.user.is_student:
        count = request.user.notifications.filter(is_read=False).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
