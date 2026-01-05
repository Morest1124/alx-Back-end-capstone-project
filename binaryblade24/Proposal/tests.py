from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Project.models import Project, Category
from Proposal.models import Proposal

User = get_user_model()

class ProposalAPITests(APITestCase):
    def setUp(self):
        # Create roles (if needed by your logic)
        from User.models import Role
        self.freelancer_role, _ = Role.objects.get_or_create(name='FREELANCER')
        self.client_role, _ = Role.objects.get_or_create(name='CLIENT')

        # Create users
        self.client_user = User.objects.create_user(
            username='client_user', 
            email='client@example.com', 
            password='password123',
            country_origin='US',
            identity_number='12345'
        )
        self.client_user.roles.add(self.client_role)

        self.freelancer = User.objects.create_user(
            username='freelancer_user', 
            email='freelancer@example.com', 
            password='password123',
            country_origin='US',
            identity_number='67890'
        )
        self.freelancer.roles.add(self.freelancer_role)

        # Create category
        self.category = Category.objects.create(name='Test Category', slug='test-category')

        # Create project
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            budget=100.00,
            price=100.00,
            category=self.category,
            client=self.client_user,
            status=Project.ProjectStatus.OPEN,
            project_type=Project.ProjectType.JOB
        )

        self.url = reverse('project_api:project-proposals', kwargs={'project_pk': self.project.pk})

    def test_submit_proposal_success(self):
        self.client.force_authenticate(user=self.freelancer)
        data = {
            'cover_letter': 'I want this job!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proposal.objects.count(), 1)
        self.assertEqual(Proposal.objects.first().freelancer, self.freelancer)
        self.assertEqual(Proposal.objects.first().bid_amount, self.project.budget)

    def test_submit_duplicate_proposal_fails(self):
        self.client.force_authenticate(user=self.freelancer)
        data = {
            'cover_letter': 'First attempt',
        }
        # First submission
        self.client.post(self.url, data)
        
        # Second submission
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already submitted', response.data['detail'])
        self.assertEqual(Proposal.objects.count(), 1)

    def test_submit_proposal_to_own_project_fails(self):
        # Give client the freelancer role too so they pass the IsFreelancer permission check
        self.client_user.roles.add(self.freelancer_role)
        self.client.force_authenticate(user=self.client_user)
        data = {
            'cover_letter': 'I want my own job!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot submit a proposal to your own project', response.data['detail'])

    def test_submit_proposal_unauthenticated_fails(self):
        data = {
            'cover_letter': 'Anon request',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)