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
    print("Starting verification (Final v3)...")
    
    # Get or create test users
    client, _ = User.objects.get_or_create(
        username='test_client_final', 
        defaults={
            'email': 'client_final@test.com',
            'identity_number': 'ID_FINAL_123',
            'country_origin': 'US'
        }
    )
    freelancer, _ = User.objects.get_or_create(
        username='test_freelancer_final', 
        defaults={
            'email': 'freelancer_final@test.com',
            'identity_number': 'ID_FINAL_456',
            'country_origin': 'ZA'
        }
    )
    
    # Ensure profile has balance
    client_profile, _ = Profile.objects.get_or_create(user=client)
    client_profile.wallet_balance = Decimal('2000.00')
    client_profile.save()
    
    # REFRESH CLIENT TO CLEAR CACHED PROFILE
    client.refresh_from_db()
    print(f"Client Balance in memory (after refresh): {client.profile.wallet_balance}")
    
    # 1. Create Contract
    contract = Contract.objects.create(
        title="Final Test Project",
        client=client,
        freelancer=freelancer,
        total_budget=Decimal('500.00'),
        status='pending'
    )
    
    # 2. Create Milestone
    m1 = Milestone.objects.create(
        contract=contract,
        description="Milestone 1 Final",
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
    print(f"Funding Response Status: {response.status_code}")
    print(f"Funding Response Data: {response.data}")
    
    m1.refresh_from_db()
    if m1.status == 'funded':
        print("SUCCESS: Milestone funded.")
    else:
        print(f"FAILURE: Milestone status is {m1.status}")
        
    print("Verification complete.")

if __name__ == "__main__":
    verify()
