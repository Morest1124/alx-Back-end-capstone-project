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
    print("Starting verification (Post-Monkeypatch-Removal)...")
    
    # Get or create test users
    client, _ = User.objects.get_or_create(
        username='test_client_new', 
        email='client_new@test.com',
        defaults={'identity_number': 'ID_NEW_123', 'country_origin': 'US'}
    )
    freelancer, _ = User.objects.get_or_create(
        username='test_freelancer_new', 
        email='freelancer_new@test.com',
        defaults={'identity_number': 'ID_NEW_456', 'country_origin': 'ZA'}
    )
    
    # Ensure profiles exist and have balance
    client_profile, _ = Profile.objects.get_or_create(user=client)
    freelancer_profile, _ = Profile.objects.get_or_create(user=freelancer)
    
    client_profile.wallet_balance = Decimal('1000.00')
    client_profile.save()
    
    # 1. Create Contract
    contract = Contract.objects.create(
        title="Test Project New",
        client=client,
        freelancer=freelancer,
        total_budget=Decimal('500.00'),
        status='pending'
    )
    
    # 2. Create Milestones
    m1 = Milestone.objects.create(
        contract=contract,
        description="Milestone 1 New",
        amount=Decimal('200.00'),
        status='pending'
    )
    
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
    
    m1.refresh_from_db()
    if m1.status == 'funded':
        print("SUCCESS: Milestone funded.")
    else:
        print(f"FAILURE: Milestone status is {m1.status}")
        
    print("Verification complete.")

if __name__ == "__main__":
    verify()
