from rest_framework import serializers
from .models import Proposal
from Project.models import Project

class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
        readOnly_fields = ['id', 'Project']
        
class ProposalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'
        readOnly_fields = ['status']
        
        
