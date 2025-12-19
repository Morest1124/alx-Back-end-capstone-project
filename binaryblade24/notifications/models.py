"""
Notification Models

In-app notification system for BinaryBlade24 platform.
Stores notifications for users about various platform events.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    """
    In-app notification model.
    
    Stores notifications for users about proposals, messages, orders, payments, etc.
    Notifications can be marked as read and include optional links to relevant pages.
    """
    
    NOTIFICATION_TYPES = [
        ('PROPOSAL_SUBMITTED', 'Proposal Submitted'),
        ('PROPOSAL_ACCEPTED', 'Proposal Accepted'),
        ('PROPOSAL_REJECTED', 'Proposal Rejected'),
        ('MESSAGE_RECEIVED', 'Message Received'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('PAYMENT_RELEASED', 'Payment Released'),
        ('ORDER_CREATED', 'Order Created'),
        ('ORDER_COMPLETED', 'Order Completed'),
        ('PROJECT_COMPLETED', 'Project Completed'),
        ('REVIEW_RECEIVED', 'Review Received'),
        ('SYSTEM_UPDATE', 'System Update'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives this notification"
    )
    
    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES,
        db_index=True,
        help_text="Type of notification"
    )
    
    title = models.CharField(
        max_length=200,
        help_text="Notification title/heading"
    )
    
    message = models.TextField(
        help_text="Notification message content"
    )
    
    # Optional linked objects for context
    project = models.ForeignKey(
        'Project.Project',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Related project (optional)"
    )
    
    proposal = models.ForeignKey(
        'Proposal.Proposal',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Related proposal (optional)"
    )
    
    order = models.ForeignKey(
        'Order.Order',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="Related order (optional)"
    )
    
    # Behavior fields
    is_read = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether notification has been read"
    )
    
    link_url = models.CharField(
        max_length=500,
        blank=True,
        help_text="URL to navigate to when notification is clicked"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When notification was created"
    )
    
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When notification was marked as read"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),  # Unread notifications query
            models.Index(fields=['recipient', 'created_at']),  # Recent notifications query
            models.Index(fields=['notification_type', 'created_at']),  # Filter by type
        ]
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.notification_type}: {self.title} for {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark this notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
