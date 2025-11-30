import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

from User.models import User, Role, Profile
from Project.models import Project, Category
from Proposal.models import Proposal
from Review.models import Review

def populate():
    print("Populating database...")

    # 0. Ensure Roles Exist
    freelancer_role, _ = Role.objects.get_or_create(name='FREELANCER')
    client_role, _ = Role.objects.get_or_create(name='CLIENT')

    # 1. Create Users (Freelancers and Clients)
    freelancers = []
    clients = []

    # Create Freelancers
    freelancer_data = [
        ("alex_dev", "Alex", "Developer", "alex@example.com", "Full Stack Developer with 5 years experience", "React, Python, Django"),
        ("sarah_design", "Sarah", "Designer", "sarah@example.com", "Creative UI/UX Designer", "Figma, Adobe XD, CSS"),
        ("mike_seo", "Mike", "SEO", "mike@example.com", "SEO Specialist and Content Strategist", "SEO, SEM, Google Analytics"),
        ("emily_writer", "Emily", "Writer", "emily@example.com", "Professional Copywriter and Editor", "Copywriting, Editing, Blogging"),
        ("david_video", "David", "Video", "david@example.com", "Video Editor and Motion Graphics Artist", "Premiere Pro, After Effects"),
    ]

    for username, first, last, email, bio, skills in freelancer_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first,
                'last_name': last,
                'is_active': True,
                'country_origin': 'South Africa', # Required field
                'identity_number': f"ID_{username}" # Required field
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created freelancer: {username}")
        
        user.roles.add(freelancer_role)
        
        # Create or Update Profile
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'bio': bio,
                'skills': skills,
                'rating': random.uniform(3.5, 5.0),
                'hourly_rate': Decimal(random.randint(20, 100))
            }
        )
            
        freelancers.append(user)

    # Create Clients
    client_data = [
        ("john_corp", "John", "Doe", "john@corp.com"),
        ("jane_startup", "Jane", "Smith", "jane@startup.com"),
        ("tech_solutions", "Tech", "Solutions", "contact@techsolutions.com"),
        ("creative_agency", "Creative", "Agency", "hello@creative.com"),
        ("global_ent", "Global", "Enterprise", "info@global.com"),
    ]

    for username, first, last, email in client_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first,
                'last_name': last,
                'is_active': True,
                'country_origin': 'USA',
                'identity_number': f"ID_{username}"
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created client: {username}")
        
        user.roles.add(client_role)
        
        # Create or Update Profile
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'bio': "Client looking for talent.",
                'rating': 5.0
            }
        )
            
        clients.append(user)

    # 2. Get Categories
    categories = list(Category.objects.filter(parent__isnull=False)) # Get subcategories
    if not categories:
        print("No subcategories found! Please load categories first.")
        return

    # 3. Create Projects (Gigs and Jobs)
    
    # Create Gigs (by Freelancers)
    gig_templates = [
        "Build a modern {} website",
        "Design a stunning {} logo",
        "SEO optimization for {}",
        "Write engaging {} blog posts",
        "Edit your {} videos",
        "Develop a custom {} script",
        "Create a {} mobile app design",
        "Translate {} documents",
        "Compose {} background music",
        "Virtual Assistant for {}"
    ]
    
    gig_topics = ["React", "Business", "E-commerce", "Tech", "Wedding", "Python", "Fitness", "Legal", "Game", "Data Entry", "Real Estate", "Crypto", "Fashion", "Food", "Travel"]

    print("Creating 25 Gigs...")
    for i in range(25):
        freelancer = freelancers[i % len(freelancers)]
        category = random.choice(categories)
        template = random.choice(gig_templates)
        topic = random.choice(gig_topics)
        title = template.format(topic) + f" ({random.randint(100,999)})" # Add random number to ensure uniqueness
        
        project, created = Project.objects.get_or_create(
            title=title,
            defaults={
                'description': f"I will {title.lower()} with high quality and fast delivery. Contact me for more details.",
                'price': Decimal(random.randint(50, 500) * 10),
                'budget': Decimal(random.randint(50, 500) * 10),
                'delivery_days': timezone.now() + timedelta(days=random.randint(3, 14)),
                'category': category,
                'client': freelancer,
                'project_type': 'GIG',
                'status': 'OPEN'
            }
        )

    # Create Jobs (by Clients)
    job_templates = [
        "Need a developer for {}",
        "Looking for a {} designer",
        "{} expert needed",
        "Copywriter for {}",
        "Video editor for {}",
        "{} expert to fix bugs",
        "UI/UX designer for {}",
        "Translator needed for {}",
        "{} composer needed",
        "{} specialist needed"
    ]

    print("Creating 25 Jobs...")
    jobs = []
    for i in range(25):
        client = clients[i % len(clients)]
        category = random.choice(categories)
        template = random.choice(job_templates)
        topic = random.choice(gig_topics)
        title = template.format(topic) + f" ({random.randint(100,999)})"
        
        project, created = Project.objects.get_or_create(
            title=title,
            defaults={
                'description': f"We are looking for someone to {title.lower()}. Must have experience and good portfolio.",
                'price': Decimal(random.randint(100, 1000) * 10),
                'budget': Decimal(random.randint(100, 1000) * 10),
                'delivery_days': timezone.now() + timedelta(days=random.randint(7, 30)),
                'category': category,
                'client': client,
                'project_type': 'JOB',
                'status': 'OPEN'
            }
        )
        jobs.append(project)

    # 4. Create Proposals (Freelancers applying to Jobs)
    for job in jobs:
        # Randomly assign 1-3 proposals per job
        num_proposals = random.randint(1, 3)
        selected_freelancers = random.sample(freelancers, num_proposals)
        
        for freelancer in selected_freelancers:
            proposal, created = Proposal.objects.get_or_create(
                project=job,
                freelancer=freelancer,
                defaults={
                    'bid_amount': job.budget * Decimal(random.uniform(0.8, 1.2)),
                    'cover_letter': f"Hi, I am interested in your project '{job.title}'. I have the skills to complete it.",
                    'status': 'PENDING'
                }
            )

    # 5. Create Reviews (For some completed projects)
    # Let's mark some jobs as completed and add reviews
    completed_jobs = jobs[:5] # First 5 jobs
    for job in completed_jobs:
        job.status = 'COMPLETED'
        job.save()
        
        # Assume the first freelancer who proposed got the job
        proposals = job.proposals.all()
        if proposals.exists():
            proposal = proposals.first()
            proposal.status = 'ACCEPTED'
            proposal.save()
            
            freelancer = proposal.freelancer
            client = job.client
            
            # Client reviews Freelancer
            Review.objects.get_or_create(
                project=job,
                reviewer=client,
                reviewee=freelancer,
                defaults={
                    'rating': random.randint(4, 5),
                    'comment': f"Great work by {freelancer.username}! Highly recommended."
                }
            )
            
            # Freelancer reviews Client
            Review.objects.get_or_create(
                project=job,
                reviewer=freelancer,
                reviewee=client,
                defaults={
                    'rating': random.randint(4, 5),
                    'comment': f"Excellent client {client.username}. Clear requirements and fast payment."
                }
            )

    print("Database population completed successfully!")

if __name__ == '__main__':
    populate()
