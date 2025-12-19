from django.db import models
from django.conf import settings
from Project.models import Project

class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.IntegerField(db_index=True)  # Index for filtering high/low rated reviews
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Index for sorting reviews by date

    class Meta:
        indexes = [
            models.Index(fields=['reviewee', 'rating']),  # Calculating user ratings
            models.Index(fields=['project', 'reviewer']),  # Ensuring one review per project per user
        ]

    def __str__(self):
        return f'Review for {self.project} by {self.reviewer.username}'
