from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Review
from .Serializer import ReviewSerializer
from django.shortcuts import get_object_or_404
from Project.models import Project
from User.models import User

class ReviewCreateView(generics.CreateAPIView):
    """
    Create a review for a freelancer on a project.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs.get('project_pk'))
        # Add logic to check if the reviewer is the client of the project
        serializer.save(reviewer=self.request.user, project=project)

class UserReviewsView(generics.ListAPIView):
    """
    List all reviews for a specific user.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Review.objects.filter(reviewee=user)