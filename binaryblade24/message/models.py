from django.db import models
from django.conf import settings
from Project.models import Project

class Conversation(models.Model):
    """
    Represents a conversation thread between two users about a specific project.
    Automatically created when a proposal is accepted.
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='conversations')
    participant_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_p1')
    participant_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations_as_p2')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['project', 'participant_1', 'participant_2']
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation: {self.participant_1.username} & {self.participant_2.username} - {self.project.title}"

    def get_other_participant(self, user):
        """Get the other participant in the conversation"""
        return self.participant_2 if self.participant_1 == user else self.participant_1


class Message(models.Model):
    """
    Individual message within a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Message from {self.sender.username} at {self.timestamp}'
