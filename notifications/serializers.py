from asyncio import tasks
from django.utils.timezone import now
from rest_framework import serializers

from .models import Notification


def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('year',        60*60*24*365),
        ('month',       60*60*24*30),
        ('day',         60*60*24),
        ('hour',        60*60),
        ('minute',      60),
        ('second',      1)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = 's' if period_value > 1 else ''
            strings.append("%s %s%s" % (period_value, period_name, has_s))

    return ", ".join(strings)


class UniModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UniModelSerializer, self).get_field_names(
            declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class NotificationSerializer(UniModelSerializer):
    since = serializers.SerializerMethodField()

    def get_since(self, obj):
        return td_format(now() - obj.timestamp) + ' ago'

    class Meta:
        model = Notification
        exclude = ['timestamp', 'user', 'reference']


class NotificationDetailSerializer(UniModelSerializer):
    since = serializers.SerializerMethodField()

    def get_since(self, obj):
        return td_format(now() - obj.timestamp) + ' ago'

    class Meta:
        model = Notification
        exclude = ['timestamp', 'user', 'content']
