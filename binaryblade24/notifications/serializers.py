"""
Notification Serializers

Serializers for the notification API.
"""

from rest_framework import serializers
from django.utils.timesince import timesince
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    
    Includes a computed 'time_ago' field for human-readable timestamps.
    """
    
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'is_read',
            'link_url',
            'created_at',
            'read_at',
            'time_ago',
        ]
        read_only_fields = ['id', 'created_at', 'read_at', 'time_ago']
    
    def get_time_ago(self, obj):
        """
        Return human-readable time since notification was created.
        Examples: "2 minutes ago", "3 hours ago", "1 day ago"
        """
        return timesince(obj.created_at) + ' ago'
