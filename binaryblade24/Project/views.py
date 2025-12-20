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
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny

from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Project, Category, Milestone
from Proposal.models import Proposal
from .Serializers import ProjectSerializer, MilestoneSerializer
from .category_serializers import CategorySerializer
from Proposal.Serializer import ProposalSerializer
from .Permissions import IsClient, IsFreelancer, IsProjectOwner, IsClientOrFreelancer
from User.models import Profile


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD operations for projects with role-based access control.
    
    Pure Fiverr Model:
        - ONLY Freelancers can create GIGs (service offerings)
        - Clients browse gigs and hire freelancers
        - Clients CANNOT post job requests
    
    This ViewSet provides different views of projects based on user roles:
    - Public/Anon: Can view OPEN gigs (marketplace discovery)
    - Clients: Can browse gigs, hire freelancers, manage hired work
    - Freelancers: Can create GIGS, view opportunities, manage accepted work
    
    Permissions Strategy:
        CREATE: Authenticated + FREELANCER role (gigs only)
        UPDATE/DELETE: Authenticated + Project owner
        LIST/RETRIEVE: Public read access (unauthenticated allowed)
    
    Default Queryset Behavior:
        Returns only OPEN gigs (the marketplace for clients to browse)
        
    Custom Actions:
        - my_projects: Returns all gigs created by the authenticated freelancer
        - my_jobs: Returns projects where freelancer has accepted proposals
    
    Business Rules:
        - New gigs always start with OPEN status
        - Creator is automatically set from authenticated user
        - Only gig creators can modify their gigs
        - Deleted gigs remove all associated proposals (cascade)
    
    Security:
        - Creator assignment is server-side (prevents impersonation)
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
            - CREATE (POST):      IsAuthenticated + IsFreelancer
              * ONLY Freelancers can create GIGs (Pure Fiverr Model)
              * Clients browse and purchase gigs, they don't post jobs
            - UPDATE (PUT/PATCH): IsAuthenticated + IsProjectOwner
            - DELETE:             IsAuthenticated + IsProjectOwner
            - LIST/RETRIEVE:      IsAuthenticatedOrReadOnly (public can read)
        
        Design Rationale:
            - Pure Fiverr model: freelancers offer services, clients hire
            - Public listing enables SEO and project discovery
            - Modification restricted to owners prevents unauthorized changes
        """
        if self.action in ['create']:
            # Both freelancers (GIGs) and clients (JOBs) can create projects
            self.permission_classes = [IsAuthenticated, IsClientOrFreelancer]
            
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only the project creator can modify or delete
            # Prevents clients/freelancers from editing each other's projects
            self.permission_classes = [IsAuthenticated, IsProjectOwner]
            
        elif self.action in ['list', 'retrieve']:
            # Public browsing allowed - no authentication required
            # Allows anonymous users to browse gigs (marketplace discovery)
            self.permission_classes = [AllowAny]
            
        else:
            # Default: authenticated or read-only
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

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsClient, IsProjectOwner])
    def approve_work(self, request, pk=None):
        """
        Approve completed work and release payment.
        """
        project = self.get_object()
        
        if project.status != Project.ProjectStatus.IN_PROGRESS:
            return Response(
                {"detail": "Project must be in progress to approve work."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        with transaction.atomic():
            # Find and release the held payment
            from User.models import Payment
            try:
                payment = Payment.objects.get(
                    project=project,
                    status=Payment.PaymentStatus.HELD
                )
                payment.status = Payment.PaymentStatus.RELEASED
                payment.save()
            except Payment.DoesNotExist:
                return Response(
                    {"detail": "No held payment found for this project."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Mark project as completed
            project.status = Project.ProjectStatus.COMPLETED
            project.save()
            
            # Send email notification
            from notifications.email_service import EmailService
            EmailService.send_payment_released_email(project, payment.amount)
            
            return Response({
                "status": "success", 
                "message": "Work approved, payment released, and project completed."
            })

    def perform_create(self, serializer):
        """
        Handle project creation with server-side field population.
        
        Automatically sets critical fields based on user role:
        - Freelancers create GIGs (service offerings)
        - Clients create JOBS (work requirements)
        
        Server-Set Fields:
            - client: Always set to the authenticated user
            - status: Always initialized as OPEN (accepts proposals/orders)
            - project_type: GIG for freelancers, JOB for clients
        
        Args:
            serializer: Validated ProjectSerializer instance
            
        Side Effects:
            - Creates new Project record
            - Sets client as authenticated user
            - Initializes status as OPEN
            - Sets project_type based on user's role
            
        Security Rationale:
            Preventing client-side control of these fields eliminates:
            - Impersonation attacks (can't set client to another user)
            - Status manipulation (can't create already-completed projects)
            - Project type manipulation (enforces role-based creation)
            - Workflow bypass (all projects start in OPEN state)
        
        Business Logic:
            - Freelancers create GIGs: Service offerings that clients can directly accept
            - Clients create JOBS: Requirements that freelancers bid on via proposals
            
            All projects go through the standard workflow:
            OPEN → (acceptance/proposal) → IN_PROGRESS → COMPLETED
        """
        user = self.request.user
        
        # Determine project type based on user role
        # Freelancers create GIGs (Fiverr-style), Clients create JOBS (Upwork-style)
        user_roles = [role.name.lower() for role in user.roles.all()]
        if 'freelancer' in user_roles:
            project_type = Project.ProjectType.GIG
        else:
            project_type = Project.ProjectType.JOB
        
        # Save project with server-controlled fields
        serializer.save(
            client=user,                                # Owner = authenticated user
            status=Project.ProjectStatus.OPEN,          # Always start accepting proposals/orders
            project_type=project_type                   # GIG or JOB based on role
        )


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for browsing categories and subcategories.
    
    Endpoints:
        GET /api/projects/categories/ - List all main categories with subcategories
        GET /api/projects/categories/{id}/ - Get a specific category
    
    Response Format:
        [
            {
                "id": 1,
                "name": "Web Development",
                "slug": "web-development",
                "description": "Professional services in Web Development",
                "subcategories": [
                    {"id": 2, "name": "Frontend Development", ...},
                    {"id": 3, "name": "Backend Development", ...}
                ]
            },
            ...
        ]
    
    Permissions:
        - Public read access (no authentication required)
        - Users can browse categories when creating projects/gigs
    """
    queryset = Category.objects.filter(parent=None).prefetch_related('subcategories')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MilestoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing project milestones.
    """
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Optionally filter milestones by project.
        """
        queryset = Milestone.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset

    def perform_create(self, serializer):
        """
        Update project milestone status and count on creation.
        """
        milestone = serializer.save()
        project = milestone.project
        project.has_milestones = True
        project.milestone_count = project.milestones.count()
        project.save()


class RecordProjectView(APIView):
    """
    Endpoint to record a view (impression) for a project.
    POST /api/projects/{id}/view/
    """
    permission_classes = [AllowAny] # Public can view projects

    def post(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None
        
        # Create view record
        # Optional: Add logic to prevent duplicate views from same IP/User within X minutes
        from .models import ProjectView
        ProjectView.objects.create(
            project=project,
            ip_address=ip,
            user=user
        )
        
        return Response({"status": "view recorded"}, status=status.HTTP_201_CREATED)
