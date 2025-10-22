# API Field References

This document lists all occurrences of the following keywords in the project: `id`, `username`, `first_name`, `last_name`, `email`, `password`, `profile`, `identity_number`, `profile_picture`.

---
File: .env.example
L9: MYSQL_PASSWORD=
.gitignore:30:# IDEs and OS
---
File: .gitignore
L31: .idea/
---
File: API_ENDPOINTS.md
L11: | **User** | GET | `/api/users/{id}/` | Retrieves a specific user's public profile. |
API_ENDPOINTS.md:12:| | PUT | `/api/users/{id}/` | Updates the authenticated user's details. |
API_ENDPOINTS.md:13:| **User Profile** | GET | `/api/users/{id}/profile/` | Retrieves the detailed profile for a user. |
API_ENDPOINTS.md:14:| | PUT | `/api/users/{id}/profile/` | Creates or updates the detailed profile for the authenticated user.|
API_ENDPOINTS.md:16:| | GET | `/api/projects/{id}/` | Retrieves a specific project's details. |
API_ENDPOINTS.md:18:| | PUT | `/api/projects/{id}/` | Updates an existing project (Client only). |
API_ENDPOINTS.md:19:| | DELETE | `/api/projects/{id}/` | Deletes a project (Client only). |
API_ENDPOINTS.md:20:| **Proposal** | GET | `/api/projects/{project_id}/proposals/`| Retrieves all proposals for a specific project. |
API_ENDPOINTS.md:21:| | GET | `/api/proposals/{id}/` | Retrieves a specific proposal's details. |
API_ENDPOINTS.md:22:| | POST | `/api/projects/{project_id}/proposals/`| Submits a new proposal to a project (Freelancer only). |
API_ENDPOINTS.md:23:| | PUT | `/api/proposals/{id}/status/` | Client accepts or rejects a proposal. |
API_ENDPOINTS.md:24:| | GET | `/api/users/{id}/proposals/` | Retrieves all proposals submitted by a specific freelancer. |
API_ENDPOINTS.md:25:| **Review** | POST | `/api/projects/{project_id}/reviews/` | Client submits a review/rating for a freelancer. |
API_ENDPOINTS.md:26:| | GET | `/api/users/{id}/reviews/` | Retrieves all reviews received by a user. |
API_ENDPOINTS.md:27:| **Comment** | POST | `/api/projects/{project_id}/comments/` | Adds a comment to a specific project. |
API_ENDPOINTS.md:28:| | GET | `/api/projects/{project_id}/comments/` | Retrieves all comments for a specific project. |
API_ENDPOINTS.md:33:| | GET | `/api/messages/{id}/` | Retrieves a single message and marks it as read. |
README.md:9:The core idea behind this project is to create a freelance marketplace that prioritizes user trust and safety. To combat spam and scams prevalent on other platforms, this marketplace requires mandatory ID verification for all users. This ensures that all interactions are between verified individuals, fostering a community built on trust.
README.md:24: git clone https://github.com/your_username_/your_project_name.git
README.md:32: MYSQL_PASSWORD=your_db_password
README.md:33: MYSQL_ROOT_PASSWORD=your_db_root_password
binaryblade24/Comment/migrations/0001_initial.py:21: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/Comment/models.py:12: return f'Comment on {self.project} by {self.user.username}'
binaryblade24/Project/Permissions.py:2:from User.models import Profile, User
---
File: binaryblade24\Project\Permissions.py
L18: # Access the profile to check the role
L19: return request.user.profile.role == Profile.UserRoles.CLIENT
L20: except Profile.DoesNotExist:
L33: # Access the profile to check the role
L34: return request.user.profile.role == Profile.UserRoles.FREELANCER
L35: except Profile.DoesNotExist:
---
File: binaryblade24\Project\Serializers.py
L17: read_only_fields = ['id', 'slug']
L21: # Nested field to display the client's public username
L31: 'id',
L52: 'id',
L67: fields = ['id', 'title', 'budget']
---
File: binaryblade24\Project\migrations\0001_initial.py
L20: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/Project/migrations/0001_initial.py:28: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/Project/migrations/0001_initial.py:33: ('project_id', models.IntegerField(unique=True)),
binaryblade24/Project/models.py:19: project_id = models.IntegerField(unique=True, blank=False)
---
File: binaryblade24\Project\models.py
L44: # client id will be created automatically
---
File: binaryblade24\Project\views.py
L5: from User.Serializers import Profile
L15: from User.models import Profile # To access UserRoles
L43: def get_queryset(self): # pyright: ignore[reportIncompatibleMethodOverride]
L51: is_client = self.request.user.profile.role == Profile.UserRoles.CLIENT
L52: except Profile.DoesNotExist:
L65: # CRUCIAL: Set the client and default status ('OPEN') from the server side.(Suggested by Gemini)
---
File: binaryblade24\Proposal\Permissions.py
L2: from User.models import Profile
---
File: binaryblade24\Proposal\Serializer.py
L15: fields = ['id', 'username', 'first_name', 'last_name']
L24: fields = ['id', 'title', 'budget']
L36: 'id',
L39: 'bid_amount',
L55: def validate_bid_amount(self, value):
L57: Example validation: Ensure the bid amount is positive.
L60: raise serializers.ValidationError("Bid amount must be greater than 5.")
---
File: binaryblade24\Proposal\migrations\0001_initial.py
L21: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/Proposal/migrations/0001_initial.py:22: ('bid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
binaryblade24/Proposal/models.py:8: bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
---
File: binaryblade24\Proposal\models.py
L41: return f"Proposal for {self.project.title} by {self.freelancer.username}"
---
File: binaryblade24\Proposal\views.py
L5: from rest_framework.serializers import ValidationError
L17: from User.models import Profile, User # To access UserRoles
L23: - POST /projects/{project_id}/proposals (Freelancer submits a bid)
L24: - GET /projects/{project_id}/proposals (Client views bids for their project)
L38: def get_queryset(self): # pyright: ignore[reportIncompatibleMethodOverride]
L40: Filters proposals by the project ID in the URL.
L42: project_id = self.kwargs.get('project_pk')
L43: project = get_object_or_404(Project, pk=project_id)
L50: # (A separate /users/{id}/proposals endpoint handles freelancer lists)
L59: project_id = self.kwargs.get('project_pk')
L60: project = get_object_or_404(Project, pk=project_id)
L64: raise ValidationError({"detail": "Cannot submit proposal: Project is not open."})
L77: Endpoint: PATCH /proposals/{id}/status
L82: # Use a serializer for validation (only accept status field)
L84: serializer.is_valid(raise_exception=True)
L86: new_status = serializer.validated_data.get('status')
L89: return Response({"detail": "Invalid status update. Only ACCEPTED or REJECTED are allowed."},
L113: Retrieves a single proposal by its ID.
L128: user_id = self.kwargs.get('pk')
L129: user = get_object_or_404(User, pk=user_id)
---
File: binaryblade24\Review\migrations\0001_initial.py
L21: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/Review/models.py:14: return f'Review for {self.project} by {self.reviewer.username}'
binaryblade24/User/Serializers.py:3:from .models import Profile
---
File: binaryblade24\User\Serializers.py
L4: from django.contrib.auth.hashers import make_password
L13: fields = ['id', 'username', 'first_name', 'last_name']
L16: class ProfileSerializer(serializers.ModelSerializer):
L18: model = Profile
L23: password = serializers.CharField(write_only=True, required=True, min_length=8)
L24: profile = ProfileSerializer(required=False)
L28: fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile', 'identity_number', 'profile_picture')
L29: read_only_fields = ('id',)
L31: def create(self, validated_data):
L32: profile_data = validated_data.pop('profile', None)
L33: password = validated_data.pop('password')
L34: if 'identity_number' in validated_data:
L35: validated_data['identity_number'] = make_password(validated_data['identity_number'])
L36: user = User.objects.create_user(password=password, **validated_data)
L37: if profile_data:
L38: Profile.objects.create(user=user, **profile_data)
L40: Profile.objects.create(user=user) # Create profile with default role
L43: def update(self, instance, validated_data):
L44: if 'password' in validated_data:
L45: password = validated_data.pop('password')
L46: instance.set_password(password)
L48: if 'identity_number' in validated_data:
L49: instance.identity_number = make_password(validated_data.pop('identity_number'))
L51: profile_data = validated_data.pop('profile', None)
L52: if profile_data:
L53: profile = instance.profile
L54: for attr, value in profile_data.items():
L55: setattr(profile, attr, value)
L56: profile.save()
L58: for attr, value in validated_data.items():
---
File: binaryblade24\User\admin.py
L10: list_display = ('username', 'email', 'first_name', 'last_name')
L11: search_fields = ('username', 'email', 'first_name', 'last_name')
L12: ordering = ('username',)
L14: (None, {'fields': ('username', 'password')}),
L15: ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
L18: ('Custom fields', {'fields': ('country_origin', 'phone_number', 'identity_number')}),
---
File: binaryblade24\User\management\commands\delete_mock_data.py
L12: # Delete all data in a specific order to avoid foreign key constraints
binaryblade24/User/management/commands/load_mock_data.py:19: user.set_password(user_data['password'])
binaryblade24/User/migrations/0001_initial.py:4:import django.contrib.auth.validators
---
File: binaryblade24\User\migrations\0001_initial.py
L14: ('auth', '0012_alter_user_first_name_max_length'),
L21: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
L22: ('password', models.CharField(max_length=128, verbose_name='password')),
L25: ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
L29: ('first_name', models.CharField(max_length=150)),
L30: ('last_name', models.CharField(max_length=150)),
L32: ('email', models.EmailField(max_length=254, unique=True)),
L34: ('identity_number', models.CharField(max_length=255, unique=True)),
---
File: binaryblade24\User\migrations\0002_remove_user_user_name_alter_user_first_name_and_more.py
L12: ('auth', '0012_alter_user_first_name_max_length'),
L22: name='first_name',
L32: name='last_name',
L41: name='Profile',
L43: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
L47: ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
---
File: binaryblade24\User\migrations\0003_user_profile_picture.py
L9: ('User', '0002_remove_user_user_name_alter_user_first_name_and_more'),
L15: name='profile_picture',
L16: field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
---
File: binaryblade24\User\migrations\0004_profile_availability_profile_hourly_rate.py
L9: ('User', '0003_user_profile_picture'),
L14: model_name='profile',
L19: model_name='profile',
---
File: binaryblade24\User\migrations\0005_alter_user_profile_picture.py
L9: ('User', '0004_profile_availability_profile_hourly_rate'),
L15: name='profile_picture',
---
File: binaryblade24\User\migrations\0006_alter_user_profile_picture.py
L9: ('User', '0005_alter_user_profile_picture'),
L15: name='profile_picture',
L16: field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
---
File: binaryblade24\User\migrations\0007_profile_avatar_profile_level.py
L9: ('User', '0006_alter_user_profile_picture'),
L14: model_name='profile',
L19: model_name='profile',
---
File: binaryblade24\User\migrations\0008_profile_rating_alter_profile_hourly_rate.py
L9: ('User', '0007_profile_avatar_profile_level'),
L14: model_name='profile',
L19: model_name='profile',
---
File: binaryblade24\User\migrations\0009_payment.py
L12: ('User', '0008_profile_rating_alter_profile_hourly_rate'),
binaryblade24/User/migrations/0009_payment.py:19: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/User/migrations/0009_payment.py:22: ('transaction_id', models.CharField(max_length=255)),
binaryblade24/User/models.py:4:from django.core.validators import MaxValueValidator, MinValueValidator
---
File: binaryblade24\User\models.py
L5: from django.contrib.auth.hashers import check_password
L12: email = models.EmailField(blank=False, unique=True)
L14: identity_number = models.CharField(max_length=255, unique=True, null=False, blank=False)
L16: # NOTE: profilePicture renamed to profile_picture (snake_case convention)
L17: profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
L19: # Use 'email' for login:
L20: USERNAME_FIELD = 'email'
L21: REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'country_origin']
L23: # Field overrides (required to avoid Django's default User model conflicts in a custom user model setup)
L37: def check_identity_number(self, raw_identity_number):
L38: return check_password(raw_identity_number, self.identity_number)
L41: return self.username
L44: class Profile(models.Model):
L50: related_name='profile'
L67: # Other non-identity profile fields
L72: # validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]),
L102: return f"{self.user.username}'s Profile ({self.get_role_display()})"
L114: transaction_id = models.CharField(max_length=255)
L119: return f"Payment of {self.amount} for {self.project.title} by {self.user.username} via {self.get_payment_method_display()}"
binaryblade24/User/urls.py:7: UserProfileView,
binaryblade24/User/urls.py:21: path('users/<int:pk>/profile/', UserProfileView.as_view(), name='user-profile'),
binaryblade24/User/views.py:4:from .Serializers import UserSerializer, ProfileSerializer
binaryblade24/User/views.py:10:from .models import Profile #, Payment
binaryblade24/User/views.py:28: """A registration endpoint that accepts username separate from first and last name."""
binaryblade24/User/views.py:32: if serializer.is_valid():
binaryblade24/User/views.py:65: if serializer.is_valid():
binaryblade24/User/views.py:71:class UserProfileView(APIView):
binaryblade24/User/views.py:73: Retrieve or update a user's profile.
binaryblade24/User/views.py:79: profile = get_object_or_404(Profile, user=user)
binaryblade24/User/views.py:80: serializer = ProfileSerializer(profile)
binaryblade24/User/views.py:85: profile = get_object_or_404(Profile, user=user)
binaryblade24/User/views.py:87: serializer = ProfileSerializer(profile, data=request.data, partial=True)
binaryblade24/User/views.py:88: if serializer.is_valid():
binaryblade24/User/views.py:100:# project_id = request.data.get('project_id')
binaryblade24/User/views.py:102:# project = Project.objects.get(id=project_id)
binaryblade24/User/views.py:121:# 'project_id': project.id,
binaryblade24/User/views.py:122:# 'user_id': request.user.id
binaryblade24/User/views.py:125:# return Response({'id': checkout_session.id})
binaryblade24/User/views.py:142:# # Invalid payload
binaryblade24/User/views.py:143:# return JsonResponse({'status': 'invalid payload'}, status=400)
binaryblade24/User/views.py:145:# # Invalid signature
binaryblade24/User/views.py:146:# return JsonResponse({'status': 'invalid signature'}, status=400)
binaryblade24/User/views.py:151:# project_id = session.get('metadata', {}).get('project_id')
binaryblade24/User/views.py:152:# user_id = session.get('metadata', {}).get('user_id')
binaryblade24/User/views.py:154:# if user_id and project_id:
binaryblade24/User/views.py:156:# user = User.objects.get(id=user_id)
binaryblade24/User/views.py:157:# project = Project.objects.get(id=project_id)
binaryblade24/User/views.py:163:# transaction_id=session.get('payment_intent'),
binaryblade24/User/views.py:179:# "client_id": settings.PAYPAL_CLIENT_ID,
binaryblade24/User/views.py:188:# project_id = request.data.get('project_id')
binaryblade24/User/views.py:190:# project = Project.objects.get(id=project_id)
binaryblade24/User/views.py:200:# "return_url": settings.SITE_URL + '/api/users/payment/paypal/execute/?project_id=' + str(project.id),
binaryblade24/User/views.py:207:# "sku": "project-" + str(project.id),
binaryblade24/User/views.py:236:# payment_id = request.query_params.get('paymentId')
binaryblade24/User/views.py:237:# payer_id = request.query_params.get('PayerID')
binaryblade24/User/views.py:238:# project_id = request.query_params.get('project_id')
binaryblade24/User/views.py:240:# if not all([payment_id, payer_id, project_id]):
binaryblade24/User/views.py:241:# return Response({"error": "Missing paymentId, PayerID, or project_id"}, status=status.HTTP_400_BAD_REQUEST)
binaryblade24/User/views.py:244:# project = Project.objects.get(id=project_id)
binaryblade24/User/views.py:248:# payment = paypalrestsdk.Payment.find(payment_id)
binaryblade24/User/views.py:250:# if payment.execute({"payer_id": payer_id}):
binaryblade24/User/views.py:255:# transaction_id=payment.id,
binaryblade24/User/views.py:260:# return Response({"status": "success", "payment_id": payment.id}, status=status.HTTP_200_OK)
binaryblade24/binaryblade24/settings.py:11:# Build paths inside the project like this: BASE_DIR / 'subdir'.
binaryblade24/binaryblade24/settings.py:53:MIDDLEWARE = [
binaryblade24/binaryblade24/settings.py:54: 'django.middleware.security.SecurityMiddleware',
binaryblade24/binaryblade24/settings.py:55: # WhiteNoise middleware for serving static files efficiently in production
binaryblade24/binaryblade24/settings.py:56: 'whitenoise.middleware.WhiteNoiseMiddleware',
binaryblade24/binaryblade24/settings.py:57: 'django.contrib.sessions.middleware.SessionMiddleware',
binaryblade24/binaryblade24/settings.py:58: 'corsheaders.middleware.CorsMiddleware', # CORS middleware
binaryblade24/binaryblade24/settings.py:59: 'django.middleware.common.CommonMiddleware',
binaryblade24/binaryblade24/settings.py:60: 'django.middleware.csrf.CsrfViewMiddleware',
binaryblade24/binaryblade24/settings.py:61: 'django.contrib.auth.middleware.AuthenticationMiddleware',
binaryblade24/binaryblade24/settings.py:62: 'django.contrib.messages.middleware.MessageMiddleware',
binaryblade24/binaryblade24/settings.py:63: 'django.middleware.clickjacking.XFrameOptionsMiddleware',
binaryblade24/binaryblade24/settings.py:99:# --- Password Validation ---
binaryblade24/binaryblade24/settings.py:100:# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
binaryblade24/binaryblade24/settings.py:102:AUTH_PASSWORD_VALIDATORS = [
binaryblade24/binaryblade24/settings.py:103: {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
binaryblade24/binaryblade24/settings.py:104: {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
binaryblade24/binaryblade24/settings.py:105: {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
binaryblade24/binaryblade24/settings.py:106: {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
binaryblade24/dashboard/views.py:47: achievement_rating = freelancer.profile.rating or 0
binaryblade24/manage.py:15: "available on your PYTHONPATH environment variable? Did you "
---
File: binaryblade24\message\migrations\0001_initial.py
L20: ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
binaryblade24/message/serializers.py:5: sender_username = serializers.ReadOnlyField(source='sender.username')
binaryblade24/message/serializers.py:6: recipient_username = serializers.ReadOnlyField(source='recipient.username')
binaryblade24/message/serializers.py:10: fields = ['id', 'sender', 'sender_username', 'recipient', 'recipient_username', 'subject', 'body', 'timestamp', 'is_read']
build.sh:24:SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-DJANGO_SUPERUSER_USERNAME}"
build.sh:25:SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-DJANGO_SUPERUSER_EMAIL}"
build.sh:26:SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-DJANGO_SUPERUSER_PASSWORD}"
build.sh:34: user = User.objects.get(username='$SUPERUSER_USERNAME')
build.sh:35: # If the user exists, only update the password/email if the env vars are set
build.sh:36: user.email = '$SUPERUSER_EMAIL'
build.sh:37: user.set_password('$SUPERUSER_PASSWORD')
build.sh:44: User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
changelog.md:7:* **User Profile Enhancements**
changelog.md:8: * **Profile Pictures**: Users can now upload their own profile pictures. A new `profile_picture` field has been added to the `User` model, and the necessary configuration for handling image uploads has been implemented.
changelog.md:9: * **Freelancer Details**: The `Profile` model has been enhanced with `hourly_rate` and `availability` fields, allowing freelancers to provide more information to potential clients.
changelog.md:16:* The `endpoint.txt` file has been updated to include the new `/api/proposals/` endpoint and to provide more detailed and accurate information about all the existing endpoints.
changelog.md:27: * The `Pillow` library has been added to the project to handle image processing for the new profile picture feature.
changelog.md:33:* **Mock Data**: Scripts have been created to bulk-create mock users, projects, and proposals. This will help to speed up development and testing by providing a realistic dataset.
mock_data.json:18: "username": "client1",
---
File: mock_data.json
L19: "first_name": "Client",
L20: "last_name": "One",
L21: "email": "client1@example.com",
L22: "password": "password123",
L24: "identity_number": "1111111111"
L27: "username": "freelancer1",
L28: "first_name": "Freelancer",
L29: "last_name": "One",
L30: "email": "freelancer1@example.com",
L31: "password": "password123",
L33: "identity_number": "2222222222"
L36: "username": "freelancer2",
L37: "first_name": "Freelancer",
L38: "last_name": "Two",
L39: "email": "freelancer2@example.com",
L40: "password": "password123",
L42: "identity_number": "3333333333"
L45: "username": "client2",
L46: "first_name": "Client",
L47: "last_name": "Two",
L48: "email": "client2@example.com",
L49: "password": "password123",
L51: "identity_number": "4444444444"
L54: "username": "admin1",
L55: "first_name": "Admin",
L56: "last_name": "One",
L57: "email": "admin1@example.com",
L58: "password": "password123",
L60: "identity_number": "5555555555"
L63: "username": "freelancer3",
L64: "first_name": "Freelancer",
L65: "last_name": "Three",
L66: "email": "freelancer3@example.com",
L67: "password": "password123",
L69: "identity_number": "6666666666"
L72: "username": "client3",
L73: "first_name": "Client",
L74: "last_name": "Three",
L75: "email": "client3@example.com",
L76: "password": "password123",
L78: "identity_number": "7777777777"
L81: "username": "freelancer4",
L82: "first_name": "Freelancer",
L83: "last_name": "Four",
L84: "email": "freelancer4@example.com",
L85: "password": "password123",
L87: "identity_number": "8888888888"
L90: "username": "client4",
L91: "first_name": "Client",
L92: "last_name": "Four",
L93: "email": "client4@example.com",
L94: "password": "password123",
L96: "identity_number": "9999999999"
L99: "username": "freelancer5",
L100: "first_name": "Freelancer",
L101: "last_name": "Five",
L102: "email": "freelancer5@example.com",
L103: "password": "password123",
L105: "identity_number": "1010101010"
