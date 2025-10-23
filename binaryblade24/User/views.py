from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .Serializers import UserSerializer, ProfileSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.roles.count() > 1:
            roles = [role.name for role in self.user.roles.all()]
            raise serializers.ValidationError({
                'detail': 'Multiple roles found. Please select a role.',
                'roles': roles
            })
        if self.user.roles.exists():
            data['role'] = self.user.roles.first().name
        else:
            data['role'] = None
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LoginWithRoleView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        role_name = request.data.get('role')
        
        user = User.objects.filter(email=email).first()
        
        if user is None or not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            
        if role_name not in [r.name for r in user.roles.all()]:
            return Response({'detail': 'Invalid role for this user.'}, status=status.HTTP_400_BAD_REQUEST)
            
        refresh = RefreshToken.for_user(user)
        refresh['role'] = role_name
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class RegisterView(APIView):
    """A registration endpoint that accepts username separate from first and last name."""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
#                 line_items=[
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
        
#         if user_id and project_id:
#             try:
#                 user = User.objects.get(id=user_id)
#                 project = Project.objects.get(id=project_id)
                
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