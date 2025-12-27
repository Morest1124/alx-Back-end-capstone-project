from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Contract, Milestone
from .serializers import ContractSerializer, MilestoneSerializer
from decimal import Decimal

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    
    @action(detail=True, methods=['post'])
    def fund_milestone(self, request, pk=None):
        milestone_id = request.data.get('milestone_id')
        try:
            milestone = Milestone.objects.get(id=milestone_id, contract_id=pk)
        except Milestone.DoesNotExist:
            return Response({'error': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
            
        client_profile = request.user.profile

        if client_profile.wallet_balance < milestone.amount:
            return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            client_profile.wallet_balance -= milestone.amount
            client_profile.save()
            milestone.status = 'funded'
            milestone.save()
            
            # Update contract status if first funding
            if milestone.contract.status == 'pending':
                milestone.contract.status = 'active'
                milestone.contract.save()

        return Response({'status': 'Milestone funded into escrow'})

    @action(detail=True, methods=['post'])
    def request_revision(self, request, pk=None):
        milestone_id = request.data.get('milestone_id')
        feedback = request.data.get('feedback', '')
        try:
            milestone = Milestone.objects.get(id=milestone_id, contract_id=pk)
        except Milestone.DoesNotExist:
            return Response({'error': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)

        if milestone.status != 'submitted':
            return Response({'error': 'Can only request revision on submitted work'}, status=status.HTTP_400_BAD_REQUEST)

        milestone.status = 'funded' # Revert status
        milestone.last_feedback = feedback
        milestone.revision_count += 1
        milestone.save()

        return Response({
            'status': 'Revision requested',
            'revision_count': milestone.revision_count
        })

    @action(detail=True, methods=['post'])
    def release_escrow(self, request, pk=None):
        milestone_id = request.data.get('milestone_id')
        try:
            milestone = Milestone.objects.get(id=milestone_id, contract_id=pk)
        except Milestone.DoesNotExist:
            return Response({'error': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if milestone.status != 'submitted':
            return Response({'error': 'Work must be submitted before release'}, status=status.HTTP_400_BAD_REQUEST)

        fee_percent = Decimal('0.10')
        gross = milestone.amount
        platform_fee = gross * fee_percent
        net_amount = gross - platform_fee

        with transaction.atomic():
            freelancer_profile = milestone.contract.freelancer.profile
            freelancer_profile.wallet_balance += net_amount
            freelancer_profile.save()
            
            milestone.status = 'released'
            milestone.save()
            
            # Check if all milestones are released to complete contract
            if not milestone.contract.milestones.exclude(status='released').exists():
                milestone.contract.status = 'completed'
                milestone.contract.save()

        return Response({'status': 'Funds released', 'net_paid': net_amount})

    @action(detail=True, methods=['post'])
    def submit_work(self, request, pk=None):
        milestone_id = request.data.get('milestone_id')
        delivery_note = request.data.get('delivery_note', '')
        delivery_url = request.data.get('delivery_url', '')
        
        try:
            milestone = Milestone.objects.get(id=milestone_id, contract_id=pk)
        except Milestone.DoesNotExist:
            return Response({'error': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if milestone.status != 'funded':
            return Response({'error': 'Milestone must be funded before submission'}, status=status.HTTP_400_BAD_REQUEST)
            
        milestone.status = 'submitted'
        milestone.delivery_note = delivery_note
        milestone.delivery_url = delivery_url
        milestone.save()
        
        return Response({'status': 'Work submitted'})
