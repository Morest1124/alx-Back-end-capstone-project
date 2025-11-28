from django.urls import path
from .views import PublicProposalsView

app_name = 'Proposal'

urlpatterns = [
    path('public/', PublicProposalsView.as_view(), name='public-proposals'),
]