import os
import django
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

from Proposal.models import Proposal
from Comment.models import Comment
from message.models import Message
from Review.models import Review
from Project.models import Project

# Check current state
print("=== Current Database State ===")
print(f"Projects: {Project.objects.count()}")
print(f"Proposals: {Proposal.objects.count()}")
print(f"Comments: {Comment.objects.count()}")
print(f"Messages: {Message.objects.count()}")
print(f"Reviews: {Review.objects.count()}")

# Check proposals with default title
default_title_count = Proposal.objects.filter(title="Proposal").count()
print(f"\nProposals with default 'Proposal' title: {default_title_count}")

# Update proposals with default titles
if default_title_count > 0:
    print("\nUpdating proposal titles...")
    proposal_title_templates = [
        "I can deliver {} with excellence",
        "Expert {} services available",
        "Professional {} at competitive rates",
        "Quality {} guaranteed",
        "Experienced in {}",
        "Specialized in {}",
        "Ready to handle {}",
        "Offering premium {}",
    ]
    
    for proposal in Proposal.objects.filter(title="Proposal"):
        job_keywords = proposal.project.title.split()[:3]
        template = random.choice(proposal_title_templates)
        proposal.title = template.format(" ".join(job_keywords))
        proposal.save()
    
    print(f"Updated {default_title_count} proposals with new titles")

print("\n=== Update Complete ===")
