from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .Serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .Permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile, Role #, Payment

# from Project.models import Project
# import stripe
# import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

class LoginView(APIView):
    """Simple login endpoint that returns user data and all their roles."""
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response({'detail': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user is None:
            # Fallback to username
            user = User.objects.filter(username=email).first()
        
        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Auto-reactivate deactivated accounts on login
        was_deactivated = False
        if user.deactivated_at:
            user.deactivated_at = None
            user.is_active = True
            user.save()
            was_deactivated = True
        
        # Check if account is scheduled for deletion
        if user.scheduled_deletion_at:
            from django.utils import timezone
            days_remaining = (user.scheduled_deletion_at - timezone.now()).days
            return Response({
                'detail': f'Your account is scheduled for deletion in {days_remaining} days. Cancel deletion from settings to continue using your account.',
                'scheduled_deletion': True,
                'days_remaining': max(0, days_remaining)
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get all user roles
        user_roles = list(user.roles.values_list('name', flat=True))
        if not user_roles:
            return Response({'detail': 'User has no assigned roles'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        refresh['role'] = user_roles[0]  # Add primary role to token
        
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'roles': user_roles
        }
        
        # Add notification if account was reactivated
        if was_deactivated:
            response_data['message'] = 'Your account has been reactivated. Welcome back!'
            response_data['reactivated'] = True
        
        return Response(response_data)

class LoginWithRoleView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        role_name = request.data.get('role')
        
        user = User.objects.filter(email=email).first()
        if user is None:
            # As a fallback, try to authenticate against the username
            user = User.objects.filter(username=email).first()
        
        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Auto-reactivate deactivated accounts on login
        was_deactivated = False
        if user.deactivated_at:
            user.deactivated_at = None
            user.is_active = True
            user.save()
            was_deactivated = True
        
        # Check if account is scheduled for deletion
        if user.scheduled_deletion_at:
            from django.utils import timezone
            days_remaining = (user.scheduled_deletion_at - timezone.now()).days
            return Response({
                'detail': f'Your account is scheduled for deletion in {days_remaining} days. Cancel deletion from settings to continue using your account.',
                'scheduled_deletion': True,
                'days_remaining': max(0, days_remaining)
            }, status=status.HTTP_403_FORBIDDEN)
            
        if role_name not in user.roles.values_list('name', flat=True):
            return Response({'detail': 'Invalid role for this user.'}, status=status.HTTP_400_BAD_REQUEST)
            
        refresh = RefreshToken.for_user(user)
        refresh['role'] = role_name
        
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
            'roles': [role_name]
        }
        
        # Add notification if account was reactivated
        if was_deactivated:
            response_data['message'] = 'Your account has been reactivated. Welcome back!'
            response_data['reactivated'] = True
        
        return Response(response_data)


class RegisterView(APIView):
    """A registration endpoint that accepts username separate from first and last name."""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                
                # Generate tokens for the new user
                refresh = RefreshToken.for_user(user)
                if user.roles.exists():
                    refresh['role'] = user.roles.first().name
                
                response_data = UserSerializer(user).data
                response_data['refresh'] = str(refresh)
                response_data['access'] = str(refresh.access_token)
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            # Return validation errors with details
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Log the full error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            
            # Return a user-friendly error message
            error_message = str(e) if str(e) else "Registration failed. Please try again."
            return Response({
                'detail': error_message
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListView(APIView):
    """
    List all users.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """
    Retrieve or update a user instance.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Retrieve or update a user's profile.
    """
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """Create or update the authenticated user's profile. Uses full PUT semantics per API docs."""
        user = get_object_or_404(User, pk=pk)
        profile = get_object_or_404(Profile, user=user)
        self.check_object_permissions(request, user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFreelancerRoleView(APIView):
    """
    Allows a user to add the 'freelancer' role to their own account.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # Get the freelancer and client roles
        freelancer_role, _ = Role.objects.get_or_create(name='freelancer')
        client_role, _ = Role.objects.get_or_create(name='client')
        
        # Add the roles to the user
        user.roles.add(freelancer_role, client_role)
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.db.models import Q

class UserSearchView(APIView):
    """
    Search for freelancers with filters.
    """
    permission_classes = [AllowAny] # Allow public search or restrict as needed

    def get(self, request, format=None):
        query = request.query_params.get('q', '')
        min_rate = request.query_params.get('min_rate')
        max_rate = request.query_params.get('max_rate')
        level = request.query_params.get('level')
        country = request.query_params.get('country')
        availability = request.query_params.get('availability')

        # Start with all users who have a 'freelancer' role
        users = User.objects.filter(roles__name='freelancer')

        if query:
            # Search in username, names, bio, skills
            users = users.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(profile__bio__icontains=query) |
                Q(profile__skills__icontains=query)
            ).distinct()

        # Apply Filters
        if min_rate:
            users = users.filter(profile__hourly_rate__gte=min_rate)
        if max_rate:
            users = users.filter(profile__hourly_rate__lte=max_rate)
        if level:
            users = users.filter(profile__level=level)
        if country:
            users = users.filter(country_origin=country)
        if availability:
            users = users.filter(profile__availability=availability)

        # Pagination (Simple limit for now, can use standard DRF pagination)
        # users = users[:20] 

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserSuggestionView(APIView):
    """
    Provide autocomplete suggestions for the search bar.
    """
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response([])

        suggestions = []

        # 1. Matches in Roles/Job Titles (if we had a standard title field, we'd use that)
        # For now, let's assume 'skills' contains relevant keywords.
        
        # 2. Matches in Skills (Assuming comma-separated string in Profile.skills or similar structure)
        # A bit complex to filter distinct skills from a CharField efficiently in SQLite/Postgres without normalization.
        # We will do a simple containment search for now.
        
        # 3. Matches in Names
        users = User.objects.filter(roles__name='freelancer').filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )[:5]
        
        for user in users:
            name_str = f"{user.first_name} {user.last_name} (@{user.username})"
            suggestions.append({
                "type": "user",
                "text": name_str.strip(),
                "id": user.id
            })

        # 4. Keyword suggestions (Mocked behavior or derived from skills)
        # Ideally, you'd query a Tag/Skill model. Here we mimic it by looking at profiles.
        profiles = Profile.objects.filter(skills__icontains=query)[:5]
        seen_skills = set()
        for p in profiles:
            # Simple splitter, might be messy if skills aren't standardized
            user_skills = [s.strip() for s in p.skills.split(',')] 
            for s in user_skills:
                if query.lower() in s.lower() and s.lower() not in seen_skills:
                    suggestions.append({
                        "type": "skill",
                        "text": s,
                        "id": s # use text as ID for skill search
                    })
                    seen_skills.add(s.lower())
                    if len(suggestions) >= 10: break
            if len(suggestions) >= 10: break

        return Response(suggestions)


# --- Stripe Payment Views ---
# stripe.api_key = settings.STRIPE_SECRET_KEY

# class StripeCheckoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         project_id = request.data.get('project_id')
#         try:
#             project = Project.objects.get(id=project_id)
#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
# line_items=[
#                     {
#                         'price_data': {
#                             'currency': 'usd',
#                             'product_data': {
#                                 'name': project.title,
#                             },
#                             'unit_amount': int(project.price * 100),
#                         },
#                         'quantity': 1,
#                     },
#                 ],
#                 mode='payment',
#                 success_url=settings.SITE_URL + '/success/',
#                 cancel_url=settings.SITE_URL + '/cancel/',
#                 metadata={
#                     'project_id': project.id,
#                     'user_id': request.user.id
#                 }
#             )
#             return Response({'id': checkout_session.id})
#         except Project.DoesNotExist:
#             return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @csrf_exempt
# def stripe_webhook(request):
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return JsonResponse({'status': 'invalid payload'}, status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return JsonResponse({'status': 'invalid signature'}, status=400)

#     # Handle the event
#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         project_id = session.get('metadata', {}).get('project_id')
#         user_id = session.get('metadata', {}).get('user_id')
#         
#         if user_id and project_id:
#             try:
#                 user = User.objects.get(id=user_id)
#                 project = Project.objects.get(id=project_id)
#                 
#                 Payment.objects.create(
#                     user=user,
#                     project=project,
#                     amount=session.get('amount_total') / 100,
#                     transaction_id=session.get('payment_intent'),
#                     payment_method='stripe',
#                     status='succeeded'
#                 )
#             except (User.DoesNotExist, Project.DoesNotExist) as e:
#                 print(f"Error processing webhook: {e}")
#                 return JsonResponse({'status': 'error', 'message': 'User or Project not found'}, status=400)

#     return JsonResponse({'status': 'success'})


# # --- PayPal Payment Views ---

# # PayPal Configuration
# paypalrestsdk.configure({
#     "mode": settings.PAYPAL_MODE,  # sandbox or live
#     "client_id": settings.PAYPAL_CLIENT_ID,
#     "client_secret": settings.PAYPAL_CLIENT_SECRET
# })


# class CreatePayPalPaymentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         project_id = request.data.get('project_id')
#         try:
#             project = Project.objects.get(id=project_id)
#         except Project.DoesNotExist:
#             return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

#         payment = paypalrestsdk.Payment({
#             "intent": "sale",
#             "payer": {
#                 "payment_method": "paypal"
#             },
#             "redirect_urls": {
#                 "return_url": settings.SITE_URL + '/api/users/payment/paypal/execute/?project_id=' + str(project.id),
#                 "cancel_url": settings.SITE_URL + '/cancel/'
#             },
#             "transactions": [{
#                 "item_list": {
#                     "items": [{
#                         "name": project.title,
#                         "sku": "project-" + str(project.id),
#                         "price": str(project.price),
#                         "currency": "USD",
#                         "quantity": 1
#                     }]
#                 },
#                 "amount": {
#                     "total": str(project.price),
#                     "currency": "USD"
#                 },
#                 "description": f"Payment for project: {project.title}"
#             }]
#         })

#         if payment.create():
#             # Find the approval url
#             for link in payment.links:
#                 if link.rel == "approval_url":
#                     approval_url = str(link.href)
#                     return Response({"approval_url": approval_url}, status=status.HTTP_201_CREATED)
#             return Response({"error": "Could not find PayPal approval URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ExecutePayPalPaymentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         payment_id = request.query_params.get('paymentId')
#         payer_id = request.query_params.get('PayerID')
#         project_id = request.query_params.get('project_id')

#         if not all([payment_id, payer_id, project_id]):
#             return Response({"error": "Missing paymentId, PayerID, or project_id"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             project = Project.objects.get(id=project_id)
#         except Project.DoesNotExist:
#             return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

#         payment = paypalrestsdk.Payment.find(payment_id)

#         if payment.execute({"payer_id": payer_id}):
#             Payment.objects.create(
#                 user=request.user,
#                 project=project,
#                 amount=payment.transactions[0].amount.total,
#                 transaction_id=payment.id,
#                 payment_method='paypal',
#                 status='succeeded'
#             )
#             # You should redirect the user to a success page on your frontend
#             return Response({"status": "success", "payment_id": payment.id}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": payment.error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)