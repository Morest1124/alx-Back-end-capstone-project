from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    role = serializers.ChoiceField(choices=Profile.UserRoles.choices, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'role')
        read_only_fields = ('id',)

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, role=role)
        return user
