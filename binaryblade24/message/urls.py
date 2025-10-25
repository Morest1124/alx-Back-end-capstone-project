from django.urls import path

app_name = 'message'
from .views import (
    InboxAPIView,
    SentMessagesAPIView,
    MessageDetailAPIView,
    SendMessageAPIView,
)

urlpatterns = [
    path('', InboxAPIView.as_view(), name='inbox'),
    path('sent/', SentMessagesAPIView.as_view(), name='sent-messages'),
    path('<int:pk>/', MessageDetailAPIView.as_view(), name='message-detail'),
    path('send/', SendMessageAPIView.as_view(), name='send-message'),
]
