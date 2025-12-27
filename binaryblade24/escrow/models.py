from django.db import models
from django.conf import settings
from Project.models import Project

class Contract(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=255)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts_as_client')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts_as_freelancer')
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.id})"

class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('funded', 'Funded'),
        ('submitted', 'Submitted'),
        ('released', 'Released'),
    ]
    
    contract = models.ForeignKey(Contract, related_name='milestones', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Delivery data
    delivery_note = models.TextField(blank=True, null=True)
    delivery_url = models.URLField(blank=True, null=True)
    
    # Revision logic
    revision_count = models.PositiveIntegerField(default=0)
    last_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.contract.title} - {self.description}"
