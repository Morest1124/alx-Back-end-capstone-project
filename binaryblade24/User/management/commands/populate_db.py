
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from User.models import Role, Profile
from Project.models import Project, Category
from Proposal.models import Proposal
from Review.models import Review
from Comment.models import Comment
from message.models import Conversation, Message
from faker import Faker
import random
from decimal import Decimal
from django.utils import timezone
import itertools

User = get_user_model()
fake = Faker()

CATEGORIES = {
    "Development": ["Web Development", "Mobile Apps", "Game Dev", "DevOps"],
    "Design": ["Logo Design", "UI/UX", "Illustration", "3D Models"],
    "Writing": ["Content Writing", "Copywriting", "Technical Writing"],
    "Marketing": ["SEO", "Social Media", "Email Marketing"]
}

SKILLS = ["Python", "React", "Django", "Node.js", "Figma", "Photoshop", "SEO", "AWS", "Docker", "Java", "C++", "Writing"]

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database population...')
        
        with transaction.atomic():
            self.create_roles()
            self.create_categories()
            users = self.create_users(30)
            projects = self.create_projects(60, users)
            self.create_proposals(60, users, projects)
            self.create_reviews(60, users, projects)
            self.create_comments(60, users, projects)
            self.create_conversations_and_messages(60, users, projects) # Creates 60 messages approx

        self.stdout.write(self.style.SUCCESS('Database successfully populated!'))

    def create_roles(self):
        Role.objects.get_or_create(name='freelancer')
        Role.objects.get_or_create(name='client')
        self.stdout.write('Roles created/verified.')

    def create_categories(self):
        for main, subs in CATEGORIES.items():
            parent, _ = Category.objects.get_or_create(name=main, slug=fake.slug(main))
            for sub in subs:
                Category.objects.get_or_create(name=sub, slug=fake.slug(sub), parent=parent)
        self.stdout.write('Categories created.')

    def create_users(self, count):
        users = []
        freelancer_role = Role.objects.get(name='freelancer')
        client_role = Role.objects.get(name='client')
        
        for _ in range(count):
            email = fake.unique.email()
            username = email.split('@')[0]
            # Ensure unique username
            while User.objects.filter(username=username).exists():
                username = username + str(random.randint(1, 999))
                
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                country_origin=random.choice(['US', 'GB', 'CA', 'AU', 'IN', 'DE', 'FR', 'ZA', 'ZW']),
                phone_number=fake.unique.phone_number()[:15], # Truncate to max len
                identity_number=fake.unique.ssn(),
            )
            
            # Add roles (randomly both or one)
            if random.random() > 0.5:
                user.roles.add(freelancer_role)
            if random.random() > 0.5:
                user.roles.add(client_role)
            if not user.roles.exists():
                user.roles.add(freelancer_role) # Default to at least one

            # Profile (Created by signal, so we update it)
            profile = user.profile
            profile.bio = fake.paragraph()
            profile.address = fake.address()
            profile.skills = ",".join(random.sample(SKILLS, k=random.randint(1, 5)))
            profile.hourly_rate = Decimal(random.randint(10, 150))
            profile.level = random.choice(Profile.SkillLevel.choices)[0]
            profile.availability = random.choice(Profile.Availability.choices)[0]
            profile.save()

            users.append(user)
            
        self.stdout.write(f'{count} Users created.')
        return users

    def create_projects(self, count, users):
        projects = []
        categories = list(Category.objects.filter(parent__isnull=False)) # Use subcategories
        
        for _ in range(count):
            client = random.choice(users)
            cat = random.choice(categories)
            
            # Ensure unique title using random suffix
            title = fake.catch_phrase() + f" {random.randint(1000, 9999)}"
            
            project = Project.objects.create(
                title=title,
                description=fake.text(max_nb_chars=1000),
                price=Decimal(random.randint(50, 5000)),
                budget=Decimal(random.randint(50, 5000)),
                category=cat,
                client=client,
                status=random.choice(Project.ProjectStatus.choices)[0],
                project_type=random.choice(Project.ProjectType.choices)[0],
                delivery_days=timezone.now() + timezone.timedelta(days=random.randint(1, 30))
            )
            projects.append(project)
            
        self.stdout.write(f'{count} Projects created.')
        return projects

    def create_proposals(self, count, users, projects):
        created_count = 0
        
        # Shuffle to randomize
        random.shuffle(users)
        random.shuffle(projects)
        
        # Try to generate proposals avoiding duplicates
        combinations = set()
        
        attempts = 0
        while created_count < count and attempts < count * 5:
            attempts += 1
            user = random.choice(users)
            project = random.choice(projects)
            
            # Freelancer can't propose to own project
            if project.client == user:
                continue
                
            # Check unique constraint
            if (project.id, user.id) in combinations:
                continue
            
            # Check DB (if running cumulatively)
            if Proposal.objects.filter(project=project, freelancer=user).exists():
                combinations.add((project.id, user.id))
                continue

            Proposal.objects.create(
                project=project,
                freelancer=user,
                bid_amount=Decimal(random.randint(int(project.budget * Decimal('0.8')), int(project.budget * Decimal('1.2')))),
                cover_letter=fake.paragraph(),
                status=random.choice(Proposal.ProposalStatus.choices)[0]
            )
            combinations.add((project.id, user.id))
            created_count += 1
            
        self.stdout.write(f'{created_count} Proposals created.')

    def create_reviews(self, count, users, projects):
        # Only for completed projects preferably, but for dummy data we can mix
        completed_projects = [p for p in projects if p.status == 'COMPLETED'] or projects[:10]
        
        count = min(count, len(completed_projects))
        
        for project in completed_projects[:count]:
            # Review from client to freelancer (Need to find who worked on it... 
            # for dummy data we'll just pick a random user as the "freelancer" who did the work)
            reviewer = project.client
            reviewee = random.choice([u for u in users if u != reviewer])
            
            Review.objects.create(
                project=project,
                reviewer=reviewer,
                reviewee=reviewee,
                rating=random.randint(1, 5),
                comment=fake.sentence()
            )
        self.stdout.write(f'{count} Reviews created.')

    def create_comments(self, count, users, projects):
        for _ in range(count):
            Comment.objects.create(
                project=random.choice(projects),
                user=random.choice(users),
                text=fake.sentence()
            )
        self.stdout.write(f'{count} Comments created.')

    def create_conversations_and_messages(self, message_count, users, projects):
        # Create a few conversations
        convs = []
        for _ in range(10): # 10 conversations
            p1 = random.choice(users)
            p2 = random.choice([u for u in users if u != p1])
            proj = random.choice(projects)
            
            if not Conversation.objects.filter(project=proj, participant_1=p1, participant_2=p2).exists():
                c = Conversation.objects.create(project=proj, participant_1=p1, participant_2=p2)
                convs.append(c)
        
        if not convs:
            # Fallback if creation failed
            return

        for _ in range(message_count):
            conv = random.choice(convs)
            sender = random.choice([conv.participant_1, conv.participant_2])
            Message.objects.create(
                conversation=conv,
                sender=sender,
                body=fake.sentence(),
                is_read=random.choice([True, False])
            )
        self.stdout.write(f'{message_count} Messages created.')
