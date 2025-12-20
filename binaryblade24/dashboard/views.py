from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Avg, Count, Q
from django.shortcuts import render
from django.urls import get_resolver
# Models moved inside methods to avoid circular dependencies

class FreelancerDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        from User.models import User
        from Order.models import OrderItem
        from Project.models import ProjectView
        from Proposal.models import Proposal
        from message.models import Conversation
        
        if user_id:
            # If user_id is provided, check if the requesting user is an admin
            if not request.user.is_staff and not request.user.is_superuser:
                return Response({"detail": "You do not have permission to view other freelancers' dashboards."}, status=status.HTTP_403_FORBIDDEN)
            try:
                freelancer = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({"detail": "Freelancer not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # If no user_id, use the logged-in user
            freelancer = request.user

        # Total Earnings (from completed order items)
        total_earnings = OrderItem.objects.filter(
            freelancer=freelancer,
            order__status='COMPLETED'
        ).aggregate(total=Sum('final_price'))['total'] or 0

        # Estimated Tax Calculation (Simplified South African Tax Brackets)
        # Using progressive tax rates based on annual income
        from decimal import Decimal
        
        def calculate_tax(annual_income):
            """Calculate tax based on simplified SA tax brackets (2024)"""
            income = Decimal(str(annual_income))
            tax = Decimal('0')
            
            # Tax brackets (simplified for demonstration)
            if income <= 237100:
                tax = income * Decimal('0.18')
            elif income <= 370500:
                tax = Decimal('42678') + (income - Decimal('237100')) * Decimal('0.26')
            elif income <= 512800:
                tax = Decimal('77362') + (income - Decimal('370500')) * Decimal('0.31')
            elif income <= 673000:
                tax = Decimal('121475') + (income - Decimal('512800')) * Decimal('0.36')
            elif income <= 857900:
                tax = Decimal('179147') + (income - Decimal('673000')) * Decimal('0.39')
            else:
                tax = Decimal('251258') + (income - Decimal('857900')) * Decimal('0.41')
            
            return float(tax)
        
        estimated_tax = calculate_tax(total_earnings) if total_earnings > 0 else 0

        # Active Projects (Orders in progress)
        active_projects = OrderItem.objects.filter(
            freelancer=freelancer,
            order__status__in=['PENDING', 'PAID']
        ).count()

        # Concluded Projects (Completed orders)
        concluded_projects = OrderItem.objects.filter(
            freelancer=freelancer,
            order__status='COMPLETED'
        ).count()

        # Total Orders (All items)
        total_orders = OrderItem.objects.filter(
            freelancer=freelancer
        ).count()

        # Achievement Rating
        achievement_rating = freelancer.profile.rating or 0

        # Response Rate Calculation
        # Definition: Percentage of conversations where the freelancer has replied
        # 1. Get all conversations where the user is a participant
        conversations = Conversation.objects.filter(
            Q(participant_1=freelancer) | Q(participant_2=freelancer)
        )
        total_conversations = conversations.count()
        
        if total_conversations > 0:
            # 2. significant conversations (where freelancer sent at least one message)
            replied_count = 0
            for convo in conversations:
                if convo.messages.filter(sender=freelancer).exists():
                    replied_count += 1
            
            rate = (replied_count / total_conversations) * 100
            response_rate = f"{int(rate)}%"
        else:
            response_rate = "N/A" # No conversations yet

        # Total Impressions (Real data from ProjectView)
        # Count all views on projects created by this freelancer
        total_impressions = ProjectView.objects.filter(
            project__client=freelancer 
        ).count()
        
        # Format for readability (e.g. 1.2K) if large
        if total_impressions > 1000:
            total_impressions = f"{total_impressions/1000:.1f}K"

        # Recent Proposals (Keeping this for now, though less relevant in Fiverr model)
        recent_proposals = Proposal.objects.filter(freelancer=freelancer).order_by('-created_at')[:3]
        recent_proposals_data = [
            {
                "title": p.project.title,
                "status": p.status,
                "date": p.created_at.strftime("%Y-%m-%d")
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
        from Order.models import Order
        from Project.models import Project
        from Proposal.models import Proposal
        from User.models import User
        
        client = request.user

        # Total Spent
        total_spent = Order.objects.filter(
            client=client,
            status='COMPLETED'
        ).aggregate(total=Sum('total_amount'))['total'] or 0

        # Active Projects (Orders)
        active_projects = Order.objects.filter(
            client=client,
            status__in=['PENDING', 'PAID']
        ).count()

        # Completed Projects (Orders)
        completed_projects = Order.objects.filter(
            client=client,
            status='COMPLETED'
        ).count()

        # Open Projects (Gigs created? Clients don't create gigs usually, but if they posted jobs)
        # In Fiverr model, clients don't have "Open Projects". 
        # But if we support hybrid, we count OPEN projects owned by client.
        open_projects = Project.objects.filter(
            client=client,
            status='OPEN'
        ).count()

        # Total Proposals Received (Legacy)
        total_proposals_received = Proposal.objects.filter(
            project__client=client
        ).count()

        # Number of Freelancers Hired (Distinct freelancers in orders)
        # Using correct related name 'received_orders' from OrderItem model
        freelancers_hired = User.objects.filter(
            received_orders__order__client=client
        ).distinct().count()

        # Recent Transactions
        # Using Orders as transactions for now
        recent_orders = Order.objects.filter(client=client).order_by('-created_at')[:5]
        recent_transactions = [
            {
                "id": o.id,
                "amount": o.total_amount,
                "project": f"Order #{o.order_number}",
                "date": o.created_at.strftime("%Y-%m-%d")
            }
            for o in recent_orders
        ]

        data = {
            'total_spent': total_spent,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'open_projects': open_projects,
            'proposals_received': total_proposals_received, # Fixed key name to match frontend
            'freelancers_hired': freelancers_hired,
            'recent_transactions': recent_transactions,
        }

        return Response(data)

def get_all_urls():
    """
    Scans all registered URL patterns and returns a sorted list of paths,
    excluding admin and internal Django URLs.
    """
    resolver = get_resolver(None)
    all_patterns = []

    def recurse_patterns(patterns, prefix=''):
        for p in patterns:
            if hasattr(p, 'url_patterns'):  # This is a URLResolver
                recurse_patterns(p.url_patterns, prefix + str(p.pattern))
            else:  # This is a URLPattern
                path = prefix + str(p.pattern)
                # Clean up the pattern string
                path = path.replace('^', '').replace('$', '')
                # Exclude unwanted patterns
                if not any(s in path for s in ['admin', 'static', 'media', '<', '(?P<']):
                    all_patterns.append(path)

    recurse_patterns(resolver.url_patterns)
    return sorted(list(set(all_patterns)))


def api_home(request):
    """
    A view that renders an HTML page displaying a list of all
    available API endpoints.
    """
    endpoints = get_all_urls()
    context = {
        'endpoints': endpoints
    }
    return render(request, 'dashboard/api_home.html', context)