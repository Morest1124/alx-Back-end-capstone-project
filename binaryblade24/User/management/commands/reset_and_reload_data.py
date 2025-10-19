
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Deletes all mock data and reloads it from the mock_data.json file'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting all mock data...'))
        call_command('delete_mock_data')
        self.stdout.write(self.style.SUCCESS('Successfully deleted mock data.'))

        self.stdout.write(self.style.WARNING('Loading new mock data...'))
        call_command('load_mock_data')
        self.stdout.write(self.style.SUCCESS('Successfully loaded new mock data.'))
