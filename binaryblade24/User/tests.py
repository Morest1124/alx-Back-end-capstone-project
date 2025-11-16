from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Role

User = get_user_model()

class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            first_name='Test',
            last_name='User',
            country_origin='KE'
        )
        self.role = Role.objects.create(name='testrole')
        self.user.roles.add(self.role)

    def test_login_with_email(self):
        """
        response = self.client.post('/api/auth/login/role/', {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'role': 'testrole'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_with_username(self):
        """
        Ensure user can log in with username.
        """
        response = self.client.post('/api/users/login/role/', {
            'email': 'testuser',  # Using username in the 'email' field
            'password': 'testpassword123',
            'role': 'testrole'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_with_invalid_password(self):
        """
        Ensure login fails with an invalid password.
        """
        response = self.client.post('/api/users/login/role/', {
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'role': 'testrole'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_invalid_role(self):
        """
        Ensure login fails with an invalid role.
        """
        response = self.client.post('/api/users/login/role/', {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'role': 'invalidrole'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
