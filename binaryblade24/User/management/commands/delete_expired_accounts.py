from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Delete user accounts that have passed their scheduled deletion date'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()
        
        # Find users scheduled for deletion whose deletion date has passed
        users_to_delete = User.objects.filter(
            scheduled_deletion_at__isnull=False,
            scheduled_deletion_at__lte=now
        )
        
        count = users_to_delete.count()
        
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No accounts scheduled for deletion.'))
            return
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} account(s):'
                )
            )
            for user in users_to_delete:
                self.stdout.write(
                    f'  - {user.email} (scheduled: {user.scheduled_deletion_at})'
                )
        else:
            self.stdout.write(
                self.style.WARNING(f'Deleting {count} expired account(s)...')
            )
            
            deleted_emails = []
            for user in users_to_delete:
                email = user.email
                deleted_emails.append(email)
                self.stdout.write(f'  Deleting user: {email}')
                user.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {len(deleted_emails)} account(s).'
                )
            )
            
            # Log deleted accounts
            for email in deleted_emails:
                self.stdout.write(f'  - {email}')
