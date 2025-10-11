from rest_framework import viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.serializers import ValidationError

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction

from Proposal.models import Proposal
from Project.models import Project
from Proposal.Serializer import ProposalSerializer, ProposalStatusUpdateSerializer
from Project.Permissions import IsClient, IsFreelancer
from .Permissions import IsProposalProjectOwner
from User.models import Profile, User # To access UserRoles


class ProposalListCreateView(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Handles: 
    - POST /projects/{project_id}/proposals (Freelancer submits a bid)
    - GET /projects/{project_id}/proposals (Client views bids for their project)
    """
    serializer_class = ProposalSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            # Only authenticated freelancers can submit proposals
            self.permission_classes = [IsAuthenticated, IsFreelancer]
        else:
            # Listing proposals requires authentication and custom ownership check
            # We defer object-level checks to the list method
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self): # pyright: ignore[reportIncompatibleMethodOverride]
        """
        Filters proposals by the project ID in the URL.
        """
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)
        
        # Security Check for GET
        # Only the client can see the list of proposals
        if self.request.method == 'GET' and project.client != self.request.user:
            # Freelancers can list their own proposals, but not via the project endpoint
            
            # (A separate /users/{id}/proposals endpoint handles freelancer lists)
            return Proposal.objects.none() 

        return Proposal.objects.filter(project=project)

    def perform_create(self, serializer):
        """
        Set freelancer, project, and initial status upon submission.
        """
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)

        # 1. Check if the project is OPEN
        if project.status != Project.ProjectStatus.OPEN:
            raise ValidationError({"detail": "Cannot submit proposal: Project is not open."})

        # 2. CRUCIAL: Set the required Foreign Keys and sttus
        serializer.save(
            freelancer=self.request.user,
            project=project,
            status=Proposal.ProposalStatus.PENDING
        )
    
    @action(detail=True, methods=['patch'], url_path='status', 
            permission_classes=[IsAuthenticated, IsClient, IsProposalProjectOwner])
    def update_status(self, request, pk=None, project_pk=None):
        """
        Endpoint: PATCH /proposals/{id}/status 
        Allow the Client to accept or reject a proposal.
        """
        proposal = get_object_or_404(Proposal, pk=pk)
        
        # Use a serializer for validation (only accept status field)
        serializer = ProposalStatusUpdateSerializer(proposal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        new_status = serializer.validated_data.get('status')

        if new_status not in [Proposal.ProposalStatus.ACCEPTED, Proposal.ProposalStatus.REJECTED]:
            return Response({"detail": "Invalid status update. Only ACCEPTED or REJECTED are allowed."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            #Update the proposal status
            proposal.status = new_status
            proposal.save()

            if new_status == Proposal.ProposalStatus.ACCEPTED:
                
                # Update the related project status
                project = proposal.project
                if project.status == Project.ProjectStatus.OPEN:
                    project.status = Project.ProjectStatus.IN_PROGRESS
                    project.save()
                    
                # Reject all other proposals for this project
                Proposal.objects.filter(project=project, status=Proposal.ProposalStatus.PENDING).exclude(pk=proposal.pk).update(status=Proposal.ProposalStatus.REJECTED)
        
        return Response(ProposalSerializer(proposal).data)


class ProposalDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single proposal by its ID.
    """
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]


class UserProposalsView(generics.ListAPIView):
    """
    Retrieves all proposals submitted by a specific freelancer.
    """
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        return Proposal.objects.filter(freelancer=user)