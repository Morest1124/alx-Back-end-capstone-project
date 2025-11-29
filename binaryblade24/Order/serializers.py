from rest_framework import serializers
from .models import Order, OrderItem, Escrow
from Project.Serializers import ProjectSerializer
from User.Serializers import UserSerializer, FreelancerDetailSerializer

class EscrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escrow
        fields = ['id', 'amount', 'status', 'held_at', 'released_at', 'refunded_at']
        read_only_fields = ['id', 'held_at', 'released_at', 'refunded_at']

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
    escrow = EscrowSerializer(read_only=True)
    
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
            'items', 'items_data', 'escrow'
        ]
        read_only_fields = [
            'id', 'order_number', 'client', 'status', 
            'total_amount', 'created_at', 'updated_at', 'paid_at'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items_data')
        # Client is passed via context from the view, not in validated_data
        client = self.context['request'].user
        
        # Create the order with initial total_amount of 0
        # Don't pass client in validated_data since it's already provided
        order = Order.objects.create(client=client, total_amount=0)
        
        # Create order items
        for item_data in items_data:
            project_id = item_data.get('project_id')
            tier = item_data.get('tier')
            
            # Fetch project to get base price and freelancer
            from Project.models import Project
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                order.delete()  # Clean up the order if project doesn't exist
                raise serializers.ValidationError(f"Project with id {project_id} does not exist")
            
            OrderItem.objects.create(
                order=order,
                project=project,
                tier=tier,
                base_price=project.budget, # Use project budget as base price
                freelancer=project.client # Project owner is the freelancer
            )
            
        # Calculate total (this will update the order's total_amount)
        order.calculate_total()
        return order
