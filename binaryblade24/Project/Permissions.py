from rest_framework import permissions
from User.models import Profile, User  

class IsClient(permissions.BasePermission):
    """
    Custom permission to only allow 'CLIENT'
    """
    message = 'Access denied. Only clients are allowed to perform this action.'

    def has_permission(self, request, view):
        # Allow read access (GET, HEAD, OPTIONS) for browsing purposes
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the authenticated user has a 'CLIENT' role
        if request.user and request.user.is_authenticated:
            try:
                # Access the profile to check the role
                return request.user.profile.role == Profile.UserRoles.CLIENT
            except Profile.DoesNotExist:
                return False
        return False

class IsFreelancer(permissions.BasePermission):
    """
    Custom permession for Only freelencers allowd
    """
    message = 'Access denied. Only freelancers are allowed to perform this action.'

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            try:
                # Access the profile to check the role
                return request.user.profile.role == Profile.UserRoles.FREELANCER
            except Profile.DoesNotExist:
                return False
        return False

class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow the project creator (client) to edit or delete it.
    """
    message = 'You do not have permission to modify this project.'
    
    def has_object_permission(self, request, view, obj):
        # Allow read permissions (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, PATCH, DELETE) are only allowed to the owner
        return obj.client == request.user
