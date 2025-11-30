from django.urls import path
from .views import ReviewCreateView, UserReviewsView

app_name = 'review_api'

urlpatterns = [
    # Create a review for a project
    path('projects/<int:project_pk>/create/', ReviewCreateView.as_view(), name='review-create'),
    
    # List all reviews for a specific user
    path('users/<int:pk>/', UserReviewsView.as_view(), name='user-reviews'),
]
