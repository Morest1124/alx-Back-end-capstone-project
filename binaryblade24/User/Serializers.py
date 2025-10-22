from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Role
from django.contrib.auth.hashers import make_password

User = get_user_model()
class FreelancerDetailSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for User details, used for nesting.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'skills', 'hourly_rate', 'rating','level', 'availability')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    profile = ProfileSerializer(required=False)
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'profile', 'identity_number', 'profile_picture', 'roles')
        read_only_fields = ('id',)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        roles_data = validated_data.pop('roles')
        if 'identity_number' in validated_data:
            validated_data['identity_number'] = make_password(validated_data['identity_number'])
        user = User.objects.create_user(password=password, **validated_data)
        user.roles.set(roles_data)
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        else:
            Profile.objects.create(user=user) # Create profile with default role
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        if 'identity_number' in validated_data:
            instance.identity_number = make_password(validated_data.pop('identity_number'))

        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        if 'roles' in validated_data:
            roles_data = validated_data.pop('roles')
            instance.roles.set(roles_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance