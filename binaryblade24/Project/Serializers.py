from rest_framework import serializers
from .models import Project, Category 
from django.contrib.auth import get_user_model
from User.Serializers import FreelancerDetailSerializer

User = get_user_model()




# Project Management Serializers
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Project Categories."""
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'slug']

class ProjectSerializer(serializers.ModelSerializer):
    """Main serializer for Project CRUD operations."""
    # Nested field to display the client's public username
    client_details = FreelancerDetailSerializer(source='client', read_only=True)
    
    # Nested field to display the category name
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Project
        # Explicitly listing fields for security and output control
        fields = [
            'id', 
            'title', 
            'description', 
            'budget',
            'price',
            'category', 
            'status', 
            'client', 
            'created_at', 
            'updated_at',
            'client_details',
            'category_details',
            'thumbnail',
            'delivery_days',
            'verbose_name',
            'help_text',
            
        ]
        
        # Security: Fields set by the server/view, not allowed in client input
        read_only_fields = [
            'id', 
            'client',
            'status',
            'created_at',
            'updated_at',
        ]

# Proposal System Serializers

class ProjectNestedSerializer(serializers.ModelSerializer):
    """
    Minimal serializer to show the associated project title for Proposal output.
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'budget']



