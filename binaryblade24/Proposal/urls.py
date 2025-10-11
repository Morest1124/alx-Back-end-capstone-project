from django.urls import path
from .views import ProposalDetailView

urlpatterns = [
    path('proposals/<int:pk>/', ProposalDetailView.as_view(), name='proposal-detail'),
]
