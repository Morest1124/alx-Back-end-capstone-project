from rest_framework import serializers
from .models import Order, OrderItem
from Project.Serializers import ProjectSerializer
from User.Serializers import UserSerializer, FreelancerDetailSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    project_details = ProjectSerializer(source='project', read_only=True)
    freelancer_details = FreelancerDetailSerializer(source='freelancer', read_only=True)
    tier_features = serializers.ListField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'project', 'project_details', 'tier', 
            'base_price', 'tier_multiplier', 'final_price',
            'freelancer', 'freelancer_details', 'created_at',
            'tier_features'
        ]
        read_only_fields = ['base_price', 'tier_multiplier', 'final_price', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    client_details = UserSerializer(source='client', read_only=True)
    
    # Write-only field to accept items during creation
    # Expected format: [{"project_id": 1, "tier": "SIMPLE"}]
    items_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'client', 'client_details',
            'status', 'total_amount', 'payment', 
            'created_at', 'updated_at', 'paid_at',
            'items', 'items_data'
        ]
        read_only_fields = [
            'id', 'order_number', 'client', 'status', 
            'total_amount', 'created_at', 'updated_at', 'paid_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items_data')
        client = self.context['request'].user
        
        # Create the order
        order = Order.objects.create(client=client, **validated_data)
        
        # Create order items
        for item_data in items_data:
            project_id = item_data.get('project_id')
            tier = item_data.get('tier')
            
            # Fetch project to get base price and freelancer
            from Project.models import Project
            project = Project.objects.get(id=project_id)
            
            OrderItem.objects.create(
                order=order,
                project=project,
                tier=tier,
                base_price=project.budget, # Use project budget as base price
                freelancer=project.client # Project owner is the freelancer
            )
            
        # Calculate total
        order.calculate_total()
        return order
