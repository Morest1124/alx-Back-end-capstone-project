
from django.core.management.base import BaseCommand
from User.models import User

class Command(BaseCommand):
    help = 'Counts the number of users in the database'

    def handle(self, *args, **options):
        user_count = User.objects.count()
        self.stdout.write(f'There are {user_count} users in the database.')
