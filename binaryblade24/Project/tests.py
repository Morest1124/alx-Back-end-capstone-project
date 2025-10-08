from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ProjectAPITests(APITestCase):
    def test_list_projects(self):
        """
        Ensure we can list projects.
        """
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)