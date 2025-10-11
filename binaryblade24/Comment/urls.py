from django.urls import path
from .views import CommentListCreateView

urlpatterns = [
    path('projects/<int:project_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
]
