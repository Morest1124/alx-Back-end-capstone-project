from django.urls import path

app_name = 'User'
from .views import (
    RegisterView, 
    UserListView, 
    UserDetailView, 
    CustomLoginView, 
    LoginWithRoleView,
    UserProfileView,
    # StripeCheckoutView, 
    # stripe_webhook,
    # CreatePayPalPaymentView,
    # ExecutePayPalPaymentView
)
from Proposal.views import UserProposalsView
from Review.views import UserReviewsView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('login/role/', LoginWithRoleView.as_view(), name='login_with_role'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/proposals/', UserProposalsView.as_view(), name='user-proposals'),
    path('users/<int:pk>/reviews/', UserReviewsView.as_view(), name='user-reviews'),
    
    # Stripe URLs
    # path('create-checkout-session/', StripeCheckoutView.as_view(), name='create-checkout-session'),
    # path('stripe-webhook/', stripe_webhook, name='stripe-webhook'),

    # PayPal URLs
    # path('payment/paypal/create/', CreatePayPalPaymentView.as_view(), name='paypal-create-payment'),
    # path('payment/paypal/execute/', ExecutePayPalPaymentView.as_view(), name='paypal-execute-payment'),
]