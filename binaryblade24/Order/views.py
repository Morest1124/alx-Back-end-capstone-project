from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Clients see their own orders
        # Freelancers see orders they are fulfilling (via items)
        user = self.request.user
        
        # Use Q objects to combine queries instead of queryset union
        from django.db.models import Q
        
        # Return orders where user is either the client OR a freelancer for any item
        return Order.objects.filter(
            Q(client=user) | Q(items__freelancer=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """
        Custom action to simulate payment (for now).
        In production, this would be a webhook from Stripe/PayPal.
        """
        order = self.get_object()
        if order.status == Order.OrderStatus.PENDING:
            order.status = Order.OrderStatus.PAID
            from django.utils import timezone
            order.paid_at = timezone.now()
            order.save()
            return Response({'status': 'Order marked as paid'})
        return Response({'error': 'Order is not pending'}, status=status.HTTP_400_BAD_REQUEST)
