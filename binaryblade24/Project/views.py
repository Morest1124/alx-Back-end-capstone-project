from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from User.Serializers import Profile

from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Project
from Proposal.models import Proposal
from .Serializers import ProjectSerializer
from Proposal.Serializer import ProposalSerializer
from .Permissions import IsClient, IsFreelancer, IsProjectOwner
from User.models import Profile # To access UserRoles



class ProjectViewSet(viewsets.ModelViewSet):
    """
    Handles Project CRUD operations: listing, creating, retriving, 
    updating, and deleting projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        """
        Set permissions based on the action (read, create, update/delete).
        """
        if self.action in ['create']:
            # Only authenticated clients can create a project
            self.permission_classes = [IsAuthenticated, IsClient]
        elif self.action in ['update', 'partial_update', 'destroy']:
            
            # Only the owner can update/delete
            self.permission_classes = [IsAuthenticated, IsProjectOwner]
        else:
            # Listing and retrieving is open to everyone
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    def get_queryset(self): # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Filter queryset:
        - Clients see all their own projects.
        - Public/Freelancers see only 'OPEN' projects.
        """
        if self.request.user.is_authenticated:
            try:
                is_client = self.request.user.profile.role == Profile.UserRoles.CLIENT
            except Profile.DoesNotExist:
                is_client = False

            if is_client:
                return Project.objects.filter(client=self.request.user)
        
        # For anonymous users or freelancers, only show open projects
        return Project.objects.filter(status=Project.ProjectStatus.OPEN)

    def perform_create(self, serializer):
        """
        Set the client and initial status upon creation.
        """
        # CRUCIAL: Set the client and default status ('OPEN') from the server side.(Suggested by Gemini)
        serializer.save(
            client=self.request.user, 
            status=Project.ProjectStatus.OPEN
        )


