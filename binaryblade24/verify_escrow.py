import os
import django
import sys
from decimal import Decimal

# Set up Django environment
sys.path.append(os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

from django.contrib.auth import get_user_model
from escrow.models import Contract, Milestone
from User.models import Profile

User = get_user_model()

def verify():
    print("Starting verification...")
    
    # Get or create test users
    client, _ = User.objects.get_or_create(
        username='test_client', 
        email='client@test.com',
        defaults={'identity_number': 'ID12345', 'country_origin': 'US'}
    )
    freelancer, _ = User.objects.get_or_create(
        username='test_freelancer', 
        email='freelancer@test.com',
        defaults={'identity_number': 'ID67890', 'country_origin': 'ZA'}
    )
    
    # Ensure profiles exist and have balance
    client_profile, _ = Profile.objects.get_or_create(user=client)
    freelancer_profile, _ = Profile.objects.get_or_create(user=freelancer)
    
    client_profile.wallet_balance = Decimal('1000.00')
    client_profile.save()
    
    print(f"Client balance: {client_profile.wallet_balance}")
    
    # 1. Create Contract
    contract = Contract.objects.create(
        title="Test Project",
        client=client,
        freelancer=freelancer,
        total_budget=Decimal('500.00'),
        status='pending'
    )
    
    # 2. Create Milestones
    m1 = Milestone.objects.create(
        contract=contract,
        description="Milestone 1",
        amount=Decimal('200.00'),
        status='pending'
    )
    
    print(f"Contract created: {contract.id}, Milestone 1: {m1.id}")
    
    # 3. Test Funding
    from django.test import RequestFactory
    from escrow.views import ContractViewSet
    from rest_framework.test import force_authenticate
    
    factory = RequestFactory()
    view = ContractViewSet.as_view({'post': 'fund_milestone'})
    
    request = factory.post(f'/api/escrow/{contract.id}/fund_milestone/', {'milestone_id': m1.id}, content_type='application/json')
    force_authenticate(request, user=client)
    
    response = view(request, pk=contract.id)
    print(f"Funding Response: {response.status_code}, {response.data}")
    
    client_profile.refresh_from_db()
    m1.refresh_from_db()
    print(f"Client balance after funding: {client_profile.wallet_balance}")
    print(f"Milestone status after funding: {m1.status}")
    
    # 4. Test Submission
    view_submit = ContractViewSet.as_view({'post': 'submit_work'})
    request = factory.post(f'/api/escrow/{contract.id}/submit_work/', {
        'milestone_id': m1.id,
        'delivery_note': 'Work done',
        'delivery_url': 'http://example.com'
    }, content_type='application/json')
    force_authenticate(request, user=freelancer)
    
    response = view_submit(request, pk=contract.id)
    print(f"Submission Response: {response.status_code}, {response.data}")
    m1.refresh_from_db()
    print(f"Milestone status after submission: {m1.status}")
    
    # 5. Test Release
    view_release = ContractViewSet.as_view({'post': 'release_escrow'})
    request = factory.post(f'/api/escrow/{contract.id}/release_escrow/', {'milestone_id': m1.id}, content_type='application/json')
    force_authenticate(request, user=client)
    
    response = view_release(request, pk=contract.id)
    print(f"Release Response: {response.status_code}, {response.data}")
    
    freelancer_profile.refresh_from_db()
    m1.refresh_from_db()
    print(f"Freelancer balance after release: {freelancer_profile.wallet_balance}")
    print(f"Milestone status after release: {m1.status}")
    
    print("Verification complete.")

if __name__ == "__main__":
    verify()
