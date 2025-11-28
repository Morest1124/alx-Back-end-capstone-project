from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    Lists all conversations for the authenticated user.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return conversations where user is a participant"""
        user = self.request.user
        return Conversation.objects.filter(
            Q(participant_1=user) | Q(participant_2=user)
        ).select_related('project', 'participant_1', 'participant_2').prefetch_related('messages')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark all messages in conversation as read"""
        conversation = self.get_object()
        Message.objects.filter(
            conversation=conversation
        ).exclude(
            sender=request.user
        ).update(is_read=True)
        return Response({'status': 'messages marked as read'})


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages within conversations.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return messages from conversations where user is a participant"""
        user = self.request.user
        conversation_id = self.request.query_params.get('conversation')
        
        queryset = Message.objects.filter(
            Q(conversation__participant_1=user) | Q(conversation__participant_2=user)
        ).select_related('sender', 'conversation')
        
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set sender to current user when creating message"""
        message = serializer.save(sender=self.request.user)
        
        # Send email notification
        from notifications.email_service import EmailService
        EmailService.send_new_message_email(message)
    
    def create(self, request, *args, **kwargs):
        """Override create to mark message as read and update conversation timestamp"""
        response = super().create(request, *args, **kwargs)
        
        # Update conversation's updated_at timestamp
        conversation_id = request.data.get('conversation')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                conversation.save()  # This triggers auto_now on updated_at
            except Conversation.DoesNotExist:
                pass
        
        return response
