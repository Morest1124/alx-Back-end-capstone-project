from rest_framework import permissions

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
            return request.user.roles.filter(name='CLIENT').exists()
        return False

class IsFreelancer(permissions.BasePermission):
    """
    Custom permession for Only freelencers allowd
    """
    message = 'Access denied. Only freelancers are allowed to perform this action.'

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user.roles.filter(name='FREELANCER').exists()
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

class IsClientOrFreelancer(permissions.BasePermission):
    """
    Custom permission to allow both 'CLIENT' and 'FREELANCER' roles.
    Used for creating projects (GIGs or JOBs).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # Check if user has either role
        return request.user.roles.filter(name__in=['CLIENT', 'FREELANCER']).exists()
