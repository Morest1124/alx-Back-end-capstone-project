from django.urls import path

app_name = 'Proposal'
from .views import ProposalDetailView, ProposalListView

urlpatterns = [
    path('proposals/', ProposalListView.as_view(), name='proposal-list'),
    path('proposals/<int:pk>/', ProposalDetailView.as_view(), name='proposal-detail'),
]