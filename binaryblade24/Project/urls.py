from django.urls import path, include

app_name = 'Project'
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, CategoryViewSet, MilestoneViewSet, RecordProjectView
from Proposal.views import ProposalListCreateView, ProposalDetailView
from Review.views import ReviewCreateView

# Separate routers to avoid conflicts
project_router = DefaultRouter()
project_router.register(r'', ProjectViewSet, basename='project')

category_router = DefaultRouter()
category_router.register(r'', CategoryViewSet, basename='category')

milestone_router = DefaultRouter()
milestone_router.register(r'', MilestoneViewSet, basename='milestone')

urlpatterns = [
    # Category routes (must come first to avoid conflicts)
    path('categories/', include(category_router.urls)),
    path('milestones/', include(milestone_router.urls)),
    
    # Proposal routes
    path('<int:project_pk>/proposals/', ProposalListCreateView.as_view({'get': 'list', 'post': 'create'}), name='project-proposals'),
    path('<int:project_pk>/proposals/<int:pk>/', ProposalDetailView.as_view(), name='proposal-detail'),
    path('<int:project_pk>/proposals/<int:pk>/status/', ProposalListCreateView.as_view({'patch': 'update_status'}), name='proposal-update-status'),
    
    # Review routes
    path('<int:project_pk>/reviews/', ReviewCreateView.as_view(), name='create-review'),
    
    # Analytics routes
    path('<int:pk>/view/', RecordProjectView.as_view(), name='record-project-view'),

    # Project routes (must come last)
    path('', include(project_router.urls)),
]