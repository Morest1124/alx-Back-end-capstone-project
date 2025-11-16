from rest_framework import serializers
from django.contrib.auth import get_user_model
# Prefer importing the concrete User class from local models so static analyzers
# and type checkers know about custom fields like `roles`.
from .models import Profile, Role
try:
    from .models import User
except Exception:
    # Fallback to get_user_model at runtime if direct import isn't possible
    User = get_user_model()
from django.contrib.auth.hashers import make_password
from django.db.models import Avg
from Project.models import Project
from Review.models import Review

# Ensure User is the concrete custom User model (imported above)
class FreelancerDetailSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for User details, used for nesting.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    # Computed/read-only fields
    completed_projects = serializers.SerializerMethodField(read_only=True)
    portfolio = serializers.SerializerMethodField(read_only=True)
    active_projects = serializers.SerializerMethodField(read_only=True)
    projects_posted = serializers.SerializerMethodField(read_only=True)
    avg_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        # include profile editable fields plus computed read-only fields
        fields = (
            'bio', 'skills', 'hourly_rate', 'rating', 'level', 'availability',
            'completed_projects', 'portfolio', 'active_projects', 'projects_posted', 'avg_rating'
        )

        read_only_fields = ('completed_projects', 'portfolio', 'active_projects', 'projects_posted', 'avg_rating')

    def get_completed_projects(self, obj):
        """Return a list of minimal completed project info for this user's created projects."""
        projects = Project.objects.filter(client=obj.user, status=Project.ProjectStatus.COMPLETED)
        result = []
        for p in projects:
            result.append({
                'id': p.id,
                'title': p.title,
                'thumbnail': p.thumbnail.url if p.thumbnail else None,
                'status': p.status,
            })
        return result

    def get_portfolio(self, obj):
        """Return a list of thumbnail URLs from completed projects (portfolio)."""
        projects = Project.objects.filter(client=obj.user, status=Project.ProjectStatus.COMPLETED).exclude(thumbnail='')
        thumbs = [p.thumbnail.url for p in projects if p.thumbnail]
        return thumbs

    def get_active_projects(self, obj):
        projects = Project.objects.filter(client=obj.user, status=Project.ProjectStatus.IN_PROGRESS)
        return [{'id': p.id, 'title': p.title, 'status': p.status} for p in projects]

    def get_projects_posted(self, obj):
        return Project.objects.filter(client=obj.user).count()

    def get_avg_rating(self, obj):
        # Prefer calculating from Review model; fall back to stored profile.rating
        agg = Review.objects.filter(reviewee=obj.user).aggregate(avg=Avg('rating'))
        avg = agg.get('avg')
        if avg is None:
            return obj.rating
        # round to one decimal for presentation
        return round(avg, 1)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    profile = ProfileSerializer(required=False)
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        required=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile', 'identity_number', 'profile_picture', 'roles', 'date_joined', 'last_login', 'country_origin')
        read_only_fields = ('id', 'date_joined', 'last_login')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        roles_data = validated_data.pop('roles')

        # Convert Role objects to a set of role names for easier lookup
        role_names = {role.name for role in roles_data}

        # If 'freelancer' is one of the chosen roles, automatically add 'client'
        if 'freelancer' in role_names:
            client_role, created = Role.objects.get_or_create(name='client')
            # Add the client role object to the list for setting the relationship
            if client_role not in roles_data:
                roles_data.append(client_role)

        if 'identity_number' in validated_data:
            validated_data['identity_number'] = make_password(validated_data['identity_number'])
        user = User.objects.create_user(password=password, **validated_data)
        
        # roles is a custom ManyToMany on the concrete User model; static type
        user.roles.set(roles_data)  # type: ignore[attr-defined]
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        if 'identity_number' in validated_data:
            new_identity_number = validated_data.pop('identity_number')
            #(Suggested by Gemini)
            # Only hash if the new identity number is different and doesn't look already hashed
            # This is a heuristic; a more robust solution might involve a separate endpoint
            # or a clear distinction between plain and hashed values.
            if new_identity_number != instance.identity_number and not new_identity_number.startswith(('pbkdf2_sha256$', 'bcrypt$', 'sha1$')):
                instance.identity_number = make_password(new_identity_number)
            elif new_identity_number != instance.identity_number: # If it's different and already hashed, assume it's a valid pre-hashed value
                instance.identity_number = new_identity_number

        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        if 'roles' in validated_data:
            roles_data = validated_data.pop('roles')
            instance.roles.set(roles_data)  # type: ignore[attr-defined]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance