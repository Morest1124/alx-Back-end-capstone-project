from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from Proposal.views import ProposalListCreateView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    path('projects/<int:project_pk>/proposals/', ProposalListCreateView.as_view({'get': 'list', 'post': 'create'}), name='project-proposals'),
]
