from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from datetime import datetime
from django.shortcuts import render


def notify_user(user, content, reference=None):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(user.pk),
        {
            "type": "notify",
            "content": {
                "body": "content",
                "reference": reference
            }
        },
    )


def home(request):
    return render(request, 'noti/home.html')


def notification_test_page(request):
    # Django Channels Notifications Test
    current_user = request.user
    channel_layer = get_channel_layer()
    data = "notification at " + \
        str(datetime.now().date()) + ' for user ' + current_user.username
    # Trigger message sent to group
    async_to_sync(channel_layer.group_send)(
        str(current_user.pk),  # Channel Name, Should always be string
        {
            "type": "notify",   # Custom Function written in the consumers.py
            "text": data,
        },
    )
    return render(request, 'noti/notifications_test_page.html')
