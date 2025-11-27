"""
Project Views Module

This module manages all project-related API endpoints in the BinaryBlade24 platform,
including project creation, browsing, and role-specific project listings.

Core Functionality:
- Clients can create and manage their posted projects
- Freelancers can browse available work and view active assignments
- Public users can view available projects (discovery/SEO)
- Role-based project filtering (my projects vs. my jobs)

API Endpoints:
- GET    /api/projects/                    - List all OPEN projects (find work)
- POST   /api/projects/                    - Create new project (clients only)
- GET    /api/projects/{id}/               - Retrieve project details
- PUT    /api/projects/{id}/               - Update project (owner only)
- DELETE /api/projects/{id}/               - Delete project (owner only)
- GET    /api/projects/my_projects/        - Client's created projects
- GET    /api/projects/my_jobs/            - Freelancer's active assignments

Author: BinaryBlade24 Team
Last Modified: 2025-11-27
"""

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Project
from Proposal.models import Proposal
from .Serializers import ProjectSerializer
from Proposal.Serializer import ProposalSerializer
from .Permissions import IsClient, IsFreelancer, IsProjectOwner
from User.models import Profile


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD operations for projects with role-based access control.
    
    This ViewSet provides different views of projects based on user roles:
    - Public/Anon: Can view OPEN projects (job board/discovery)
    - Clients: Can create, manage, and view their own projects
    - Freelancers: Can view OPEN projects and their accepted assignments
    
    Permissions Strategy:
        CREATE: Authenticated + CLIENT role
        UPDATE/DELETE: Authenticated + Project owner
        LIST/RETRIEVE: Public read access (unauthenticated allowed)
    
    Default Queryset Behavior:
        Returns only OPEN projects (the "Find Work" feed for freelancers)
        
    Custom Actions:
        - my_projects: Returns all projects created by the authenticated client
        - my_jobs: Returns projects where freelancer has accepted proposals
    
    Business Rules:
        - New projects always start with OPEN status
        - Client is automatically set from authenticated user
        - Only project creators can modify their projects
        - Deleted projects remove all associated proposals (cascade)
    
    Security:
        - Client assignment is server-side (prevents impersonation)
        - Status changes through proposal acceptance (prevents manual manipulation)
        - Role-based permissions prevent cross-role actions
    """
    
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_permissions(self):
        """
        Dynamically assign permissions based on the HTTP method/action.
        
        Returns:
            list: Permission classes for the current request
            
        Permission Matrix:
            - CREATE (POST):      IsAuthenticated + IsClient
            - UPDATE (PUT/PATCH): IsAuthenticated + IsProjectOwner
            - DELETE:             IsAuthenticated + IsProjectOwner
            - LIST/RETRIEVE:      IsAuthenticatedOrReadOnly (public can read)
        
        Design Rationale:
            - Public listing enables SEO and project discovery
            - Creation restricted to clients prevents spam/fraud
            - Modification restricted to owners prevents unauthorized changes
        """
        if self.action in ['create']:
            # Only authenticated clients can create projects
            # Freelancers cannot post work (business rule)
            self.permission_classes = [IsAuthenticated, IsClient]
            
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only the project creator can modify or delete
            # Prevents clients from editing each other's projects
            self.permission_classes = [IsAuthenticated, IsProjectOwner]
            
        else:
            # Listing and retrieving projects is open to everyone
            # Allows non-authenticated users to browse (SEO, discovery)
            # Authenticated users see additional fields (via serializer context)
            self.permission_classes = [IsAuthenticatedOrReadOnly]
            
        return super().get_permissions()

    def get_queryset(self):
        """
        Filter projects to show only OPEN opportunities.
        
        This is the default queryset for the "Find Work" page where freelancers
        browse available projects. It intentionally excludes:
        - IN_PROGRESS projects (already assigned)
        - COMPLETED projects (finished work)
        - CANCELED projects (no longer active)
        
        Returns:
            QuerySet: Only projects with status=OPEN
            
        Note:
            Clients and freelancers use custom actions (my_projects, my_jobs)
            to view their specific projects. This default view is for discovery.
        
        Alternative Views:
            - Use my_projects() for client's created projects
            - Use my_jobs() for freelancer's active work
        """
        # Show only open projects (the "job board" for freelancers)
        return Project.objects.filter(status=Project.ProjectStatus.OPEN)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsClient])
    def my_projects(self, request):
        """
        Retrieve all projects created by the authenticated client.
        
        This endpoint provides clients with a complete view of their posted
        projects regardless of status (OPEN, IN_PROGRESS, COMPLETED, CANCELED).
        Essential for the client dashboard and project management interface.
        
        Endpoint: GET /api/projects/my_projects/
        
        Permissions:
            - Must be authenticated
            - Must have CLIENT role
            
        Returns:
            Response: List of client's projects with full details
            
        Response Format:
            [
                {
                    "id": 1,
                    "title": "Build React Dashboard",
                    "status": "IN_PROGRESS",
                    "budget": 5000.00,
                    "client_details": {...},
                    ...
                }
            ]
        
        Use Cases:
            - Client dashboard showing project portfolio
            - Project management page with filters
            - Analytics on client's posting activity
        
        Security:
            Filtered to current user's projects only (prevents viewing others)
        """
        user = request.user
        
        # Get all projects where this user is the client
        projects = Project.objects.filter(client=user)
        
        # Serialize with full context (may expose additional fields)
        serializer = self.get_serializer(projects, many=True)
        
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsFreelancer])
    def my_jobs(self, request):
        """
        Retrieve projects where freelancer has accepted proposals.
        
        This endpoint shows freelancers their active work - projects where
        they've been hired (proposal status = ACCEPTED). This is distinct
        from the default queryset which shows available work to apply for.
        
        Endpoint: GET /api/projects/my_jobs/
        
        Permissions:
            - Must be authenticated
            - Must have FREELANCER role
            
        Query Logic:
            Returns projects where:
            1. A proposal exists by this freelancer
            2. That proposal's status is ACCEPTED
        
        Returns:
            Response: List of freelancer's active assignments
            
        Response Format:
            [
                {
                    "id": 1,
                    "title": "Build React Dashboard",
                    "status": "IN_PROGRESS",
                    "budget": 5000.00,
                    "client_details": {
                        "email": "client@example.com",  // Exposed after acceptance
                        "phone_number": "+1234567890"
                    },
                    ...
                }
            ]
        
        Use Cases:
            - Freelancer dashboard showing active work
            - "My Jobs" or "My Projects" page
            - Time tracking integration (show current assignments)
        
        Note:
            Client contact details are exposed in the response because
            the proposal is ACCEPTED. See ProjectSerializer conditional logic.
        
        Performance:
            Uses efficient JOIN via proposals__freelancer and proposals__status
            Index on (freelancer_id, status) recommended for scale
        """
        user = request.user
        
        # Filter projects where:
        # 1. There exists a proposal by this user
        # 2. That proposal's status is ACCEPTED
        # Uses Django's double-underscore notation for related model filtering
        projects = Project.objects.filter(
            proposals__freelancer=user,
            proposals__status='ACCEPTED'
        )
        
        # Serialize with request context (enables conditional field exposure)
        serializer = self.get_serializer(projects, many=True)
        
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Handle project creation with server-side field population.
        
        Automatically sets critical fields that should never be controlled
        by client input to maintain data integrity and security.
        
        Server-Set Fields:
            - client: Always set to the authenticated user
            - status: Always initialized as OPEN (accepts proposals)
        
        Args:
            serializer: Validated ProjectSerializer instance
            
        Side Effects:
            - Creates new Project record
            - Sets client as authenticated user
            - Initializes status as OPEN
            
        Security Rationale:
            Preventing client-side control of these fields eliminates:
            - Impersonation attacks (can't set client to another user)
            - Status manipulation (can't create already-completed projects)
            - Workflow bypass (all projects start in OPEN state)
        
        Business Logic:
            All new projects must go through the standard workflow:
            OPEN → (proposal acceptance) → IN_PROGRESS → COMPLETED
        
        Note:
            Project details (title, description, budget, etc.) come from
            the validated request data. Only relationship fields and
            workflow state are server-controlled.
        """
        # Save project with server-controlled fields
        # This prevents malicious clients from:
        # - Setting themselves as owner of project they shouldn't control
        # - Creating projects in IN_PROGRESS or COMPLETED state
        # - Bypassing the normal project workflow
        serializer.save(
            client=self.request.user,              # Owner = authenticated user
            status=Project.ProjectStatus.OPEN       # Always start accepting proposals
        )
