"""
Notification API Views

REST API endpoints for managing user notifications.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and managing notifications.
    
    Provides endpoints for:
    - list: Get user's notifications
    - retrieve: Get specific notification
    - unread_count: Get count of unread notifications
    - mark_read: Mark specific notification as read
    - mark_all_read: Mark all notifications as read
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        """
        Return only the authenticated user's notifications.
        
        Security: Users can only see their own notifications.
        """
        return Notification.objects.filter(recipient=self.request.user)
    
    def create(self, request, *args, **kwargs):
        """
        Disable create endpoint.
        
        Notifications should only be created through the NotificationService,
        not directly via the API.
        """
        return Response(
            {'detail': 'Notifications cannot be created via API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def update(self, request, *args, **kwargs):
        """
        Disable update endpoint.
        
        Use mark_read endpoint instead.
        """
        return Response(
            {'detail': 'Use mark_read endpoint to update notifications'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """Allow users to delete their notifications"""
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications.
        
        Endpoint: GET /api/notifications/notifications/unread_count/
        
        Returns:
            {"unread_count": 5}
        """
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark a specific notification as read.
        
        Endpoint: POST /api/notifications/notifications/{id}/mark_read/
        
        Returns:
            {"status": "marked as read", "notification_id": 123}
        """
        notification = self.get_object()
        notification.mark_as_read()
        
        return Response({
            'status': 'marked as read',
            'notification_id': notification.id
        })
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Mark all user's notifications as read.
        
        Endpoint: POST /api/notifications/notifications/mark_all_read/
        
        Returns:
            {"status": "all notifications marked as read", "count": 10}
        """
        updated_count = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'status': 'all notifications marked as read',
            'count': updated_count
        })
