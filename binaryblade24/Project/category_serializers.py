"""
Category Serializers

Handles serialization of 3-level hierarchical category data for the frontend.
"""

from rest_framework import serializers
from .models import Category


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Serializer for subcategories (Level 2) with items (Level 3).
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'items']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for main categories (Level 1) with nested subcategories.
    
    Response format:
    {
        "id": 1,
        "name": "Core Development",
        "slug": "core-development",
        "description": "Fundamental web development services",
        "subcategories": [
            {
                "id": 2,
                "name": "Frontend Development",
                "slug": "frontend-development",
                "description": "Client-side web development",
                "items": [
                    "SPA Development (React, Vue, Angular)",
                    "Responsive Web Design (HTML/CSS/JS)"
                ]
            }
        ]
    }
    """
    subcategories = SubcategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'subcategories']
