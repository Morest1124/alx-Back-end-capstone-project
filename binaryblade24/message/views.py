from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class InboxAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-timestamp')

class SentMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user).order_by('-timestamp')

class MessageDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def get_object(self):
        obj = super().get_object()
        if self.request.user == obj.recipient:
            obj.is_read = True
            obj.save()
        return obj

class SendMessageAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
