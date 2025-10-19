from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Project.models import Project, Category
from Proposal.models import Proposal

User = get_user_model()

class Command(BaseCommand):
    help = 'Deletes all mock data from the database'

    def handle(self, *args, **kwargs):
        # Delete all data in a specific order to avoid foreign key constraints
        Proposal.objects.all().delete()
        Project.objects.all().delete()
        Category.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted mock data.'))