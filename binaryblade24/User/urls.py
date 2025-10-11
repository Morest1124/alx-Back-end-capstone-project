from django.urls import path
from .views import RegisterView, UserListView, UserDetailView, LoginView, UserProfileView
from Proposal.views import UserProposalsView
from Review.views import UserReviewsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/proposals/', UserProposalsView.as_view(), name='user-proposals'),
    path('users/<int:pk>/reviews/', UserReviewsView.as_view(), name='user-reviews'),
]