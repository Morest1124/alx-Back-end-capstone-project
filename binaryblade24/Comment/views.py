from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .Serializer import CommentSerializer
from django.shortcuts import get_object_or_404
from Project.models import Project

class CommentListCreateView(generics.ListCreateAPIView):
    """
    List all comments for a project or create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        return Comment.objects.filter(project=project)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        serializer.save(user=self.request.user, project=project)