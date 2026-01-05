from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class ProjectAPITests(APITestCase):
    def test_list_projects(self):
        """
        Ensure we can list projects publicly.
        """
        url = reverse('project_api:project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_jobs_anonymous(self):
        """
        Ensure anonymous users get 401 (not 500) for my_jobs.
        """
        url = reverse('project_api:project-my-jobs')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_category_param(self):
        """
        Ensure invalid category param doesn't cause 500 error.
        """
        url = reverse('project_api:project-list')
        response = self.client.get(f"{url}?category=undefined", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)