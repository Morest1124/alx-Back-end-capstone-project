from django.urls import path

app_name = 'dashboard'
from .views import FreelancerDashboardAPIView, ClientDashboardAPIView

urlpatterns = [
    path('freelancer/<int:user_id>/', FreelancerDashboardAPIView.as_view(), name='freelancer-dashboard-detail'),
    path('freelancer/', FreelancerDashboardAPIView.as_view(), name='freelancer-dashboard'),
    path('client/', ClientDashboardAPIView.as_view(), name='client-dashboard'),
]
