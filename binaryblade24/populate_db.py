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

    # 2.5 Clean up old projects with numbers in titles
    print("Cleaning up old projects with numbers in titles...")
    old_projects = Project.objects.filter(title__regex=r'\(\d+\)$')
    deleted_count = old_projects.count()
    old_projects.delete()
    print(f"Deleted {deleted_count} old projects with numbered titles")

    # 3. Create Projects (Gigs and Jobs)
    
    # Create Gigs (by Freelancers) - More natural titles
    gig_titles = [
        "Build a modern React e-commerce website",
        "Design a professional business logo and brand identity",
        "Complete SEO optimization for your online store",
        "Write 10 engaging tech blog posts",
        "Edit and enhance your wedding videos professionally",
        "Develop a custom Python automation script",
        "Create a stunning mobile app UI design",
        "Translate legal documents from English to Spanish",
        "Compose original background music for your game",
        "Provide virtual assistant services for data entry",
        "Build a responsive landing page with HTML/CSS",
        "Design a minimalist logo for your startup",
        "Optimize your website for search engines",
        "Write compelling product descriptions for e-commerce",
        "Edit your YouTube videos with professional transitions",
        "Develop a Django REST API for your application",
        "Create a modern Figma design for mobile app",
        "Translate your website content to French",
        "Compose a catchy jingle for your brand",
        "Manage your social media accounts professionally",
        "Build a full-stack web application with React and Node",
        "Design eye-catching social media graphics",
        "Implement advanced SEO strategies for your blog",
        "Write engaging email marketing campaigns",
        "Create stunning motion graphics for your videos"
    ]

    print("Creating 25 Gigs...")
    for i, title in enumerate(gig_titles):
        freelancer = freelancers[i % len(freelancers)]
        category = random.choice(categories)
        
        project, created = Project.objects.get_or_create(
            title=title,
            defaults={
                'description': f"I will {title.lower()} with high quality and fast delivery. I have years of experience and a proven track record. Contact me to discuss your project requirements.",
                'price': Decimal(random.randint(50, 500) * 10),
                'budget': Decimal(random.randint(50, 500) * 10),
                'delivery_days': timezone.now() + timedelta(days=random.randint(3, 14)),
                'category': category,
                'client': freelancer,
                'project_type': 'GIG',
                'status': 'OPEN'
            }
        )

    # Create Jobs (by Clients) - More natural titles
    job_titles = [
        "Need an experienced developer for SaaS platform development",
        "Looking for a creative logo designer for tech startup",
        "SEO expert needed for long-term e-commerce project",
        "Professional copywriter for landing page content",
        "Skilled video editor for wedding footage editing",
        "Python expert to fix bugs in existing application",
        "Talented UI/UX designer for mobile app redesign",
        "Urgent: Translator needed for legal documents",
        "Music composer for indie game soundtrack",
        "Data entry specialist for large-scale project",
        "Full-stack developer for custom CRM system",
        "Graphic designer for complete brand identity package",
        "Digital marketing expert for social media campaigns",
        "Content writer for technology blog articles",
        "Video production specialist for corporate videos",
        "Backend developer for API integration project",
        "Web designer for portfolio website creation",
        "Multilingual translator for international expansion",
        "Audio engineer for podcast editing and mastering",
        "Administrative assistant for ongoing virtual support",
        "React developer for single-page application",
        "Brand designer for complete visual identity",
        "SEO consultant for website traffic improvement",
        "Technical writer for software documentation",
        "Motion graphics artist for explainer videos"
    ]

    print("Creating 25 Jobs...")
    jobs = []
    for i, title in enumerate(job_titles):
        client = clients[i % len(clients)]
        category = random.choice(categories)
        
        project, created = Project.objects.get_or_create(
            title=title,
            defaults={
                'description': f"We are looking for a professional to {title.lower()}. Must have relevant experience and a strong portfolio. Please include your previous work samples when applying.",
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
    proposal_title_templates = [
        "I can deliver {} with excellence",
        "Expert {} services available",
        "Professional {} at competitive rates",
        "Quality {} guaranteed",
        "Experienced in {}",
    ]
    
    for job in jobs:
        # Randomly assign 1-3 proposals per job
        num_proposals = random.randint(1, 3)
        selected_freelancers = random.sample(freelancers, num_proposals)
        
        for freelancer in selected_freelancers:
            # Generate a title based on the job
            template = random.choice(proposal_title_templates)
            # Extract key words from job title for proposal title
            job_keywords = job.title.split()[:3]  # First 3 words
            proposal_title = template.format(" ".join(job_keywords))
            
            proposal, created = Proposal.objects.get_or_create(
                project=job,
                freelancer=freelancer,
                defaults={
                    'title': proposal_title,
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
