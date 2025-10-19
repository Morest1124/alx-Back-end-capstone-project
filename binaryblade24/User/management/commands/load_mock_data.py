
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Loads mock user data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('mock_data.json') as f:
            mock_data = json.load(f)

        # Load Users
        for user_data in mock_data.get('users', []):
            user, created = User.objects.get_or_create(**user_data)
            if created:
                user.set_password(user_data['password'])
                user.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded mock user data.'))
