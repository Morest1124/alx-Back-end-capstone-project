from rest_framework import serializers
from .models import Project, Category

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        # `client` is a ForeignKey to the User model; Django will manage
        # `client_id` automatically. Keep project_id read-only.
        readOnly_fields = ['id', 'project_id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        readOnly_fields = ['id']
        
class ProjectStatusSerializers(serializers.ModelSerializer):
    class Meta:
        #Default ordering of quiries
        ordering = ['-created_at']
        