from rest_framework import serializers
from .models import Project, Category

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        readOnly_fields = ['id', 'project_id', 'client_id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        readOnly_fields = ['id']