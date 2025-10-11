from rest_framework import serializers
from .models import Proposal
from Project.models import Project 
from django.contrib.auth import get_user_model

User = get_user_model()

class FreelancerDetailSerializer(serializers.ModelSerializer):
    """
    Minimal serializer to represent the Freelancer (User) details 
    when viewing a proposal.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Helper Serializers for Nesting
class ProjectNestedSerializer(serializers.ModelSerializer):
    """
    Minimal serializer to show the associated project title.
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'budget']


# Main Proposal Serializer
class ProposalSerializer(serializers.ModelSerializer):
    freelancer_details = FreelancerDetailSerializer(source='freelancer', read_only=True)
    project_details = ProjectNestedSerializer(source='project', read_only=True)

    class Meta:
        model = Proposal
        # List all fields you want to expose or allow input for(Implemented by Gemini for security purposes to prevent data leaks)
        fields = [
            'id', 
            'project',
            'freelancer',
            'bid_amount', 
            'cover_letter', 
            'status', 
            'created_at',
            'freelancer_details',
            'project_details',
        ]
        
        #for  Security 
        read_only_fields = [
            'status',
            'freelancer',
            'project',
            'created_at',
        ]
        
    def validate_bid_amount(self, value):
        """
        Example validation: Ensure the bid amount is positive.
        """
        if value <= 5:
            raise serializers.ValidationError("Bid amount must be greater than 5.")
        return value

class ProposalStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = ['status']