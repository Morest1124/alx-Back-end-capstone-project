from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Count, Q
from Project.models import Project
from Proposal.models import Proposal
from Review.models import Review
from User.models import User

class FreelancerDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        freelancer = request.user

        # Total Earnings
        total_earnings = Project.objects.filter(
            proposals__freelancer=freelancer,
            proposals__status='ACCEPTED',
            status='COMPLETED'
        ).aggregate(total_earnings=Sum('price'))['total_earnings'] or 0

        # Estimated Monthly Tax (18%)
        estimated_tax = total_earnings * 0.18

        # Active Projects
        active_projects = Project.objects.filter(
            proposals__freelancer=freelancer,
            proposals__status='ACCEPTED',
            status='IN_PROGRESS'
        ).count()

        # Concluded Projects
        concluded_projects = Project.objects.filter(
            proposals__freelancer=freelancer,
            proposals__status='ACCEPTED',
            status='COMPLETED'
        ).count()

        # Total Orders (accepted proposals)
        total_orders = Proposal.objects.filter(
            freelancer=freelancer,
            status='ACCEPTED'
        ).count()

        # Achievement Rating
        achievement_rating = freelancer.profile.rating or 0

        # Response Rate 
        response_rate = "95%"

        # Total Impressions (hardcoded as no tracking for this)
        total_impressions = "18.5K"

        # Recent Proposals
        recent_proposals = Proposal.objects.filter(freelancer=freelancer).order_by('-created_at')[:3]
        recent_proposals_data = [
            {
                "project_title": p.project.title,
                "status": p.status,
                "created_at": p.created_at.strftime("%Y-%m-%d")
            }
            for p in recent_proposals
        ]

        data = {
            'total_earnings': total_earnings,
            'estimated_monthly_tax': estimated_tax,
            'active_projects': active_projects,
            'concluded_projects': concluded_projects,
            'total_orders': total_orders,
            'achievement_rating': achievement_rating,
            'response_rate': response_rate,
            'total_impressions': total_impressions,
            'recent_proposals': recent_proposals_data,
        }

        return Response(data)

class ClientDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = request.user

        # Total Spent
        total_spent = Project.objects.filter(
            client=client,
            status='COMPLETED'
        ).aggregate(total_spent=Sum('price'))['total_spent'] or 0

        # Active Projects
        active_projects = Project.objects.filter(
            client=client,
            status='IN_PROGRESS'
        ).count()

        # Completed Projects
        completed_projects = Project.objects.filter(
            client=client,
            status='COMPLETED'
        ).count()

        # Open Projects
        open_projects = Project.objects.filter(
            client=client,
            status='OPEN'
        ).count()

        # Total Proposals Received
        total_proposals_received = Proposal.objects.filter(
            project__client=client
        ).count()

        # Number of Freelancers Hired
        freelancers_hired = User.objects.filter(
            submitted_proposals__project__client=client,
            submitted_proposals__status='ACCEPTED'
        ).distinct().count()

        data = {
            'total_spent': total_spent,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'open_projects': open_projects,
            'total_proposals_received': total_proposals_received,
            'freelancers_hired': freelancers_hired,
        }

        return Response(data)