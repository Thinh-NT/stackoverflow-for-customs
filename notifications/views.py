from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import NotificationDetailSerializer, NotificationSerializer
from .models import Notification


def notify_user(user, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(user.pk),  # Channel Name, Should always be string
        {
            "type": "notify",   # Custom Function written in the consumers.py
            "text": data,
        },
    )


def home(request):
    return render(request, 'noti/home.html')


def notification_test_page(request):
    # Django Channels Notifications Test
    current_user = request.user
    data = "Hey, check notifications plz."
    # Trigger message sent to group
    notify_user(current_user, data)
    return render(request, 'noti/notifications_test_page.html')


class NotificationView(viewsets.ModelViewSet):
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NotificationDetailSerializer
        return NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        return queryset.order_by('-timestamp')

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_read = True
        obj.save()
        return super().retrieve(request, *args, **kwargs)
