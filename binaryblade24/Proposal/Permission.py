from rest_framework import permissions
from User.models import Profile 
from django.core.exceptions import ObjectDoesNotExist


class IsFreelancer(permissions.BasePermission):
    """
    Custom permission to only allow users with the 'FREELANCER' role to proceed.
    This check is mandatory for POSTing a proposal.
    """
    message = 'Access denied. Only freelancers are allowed to submit proposals.'

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return False
            try:
                # Access the profile to check the role
                # NOTE: Ensure Profile.UserRoles is imported or accessible.(Suggested by Gemini)
                return request.user.profile.role == Profile.UserRoles.FREELANCER
            except Profile.DoesNotExist:
                return False
        return False

class IsProposalProjectOwner(permissions.BasePermission):
    """
    Custom permission to allow only the owner of the related Project 
    to manage (accept/reject) the Proposal status.
    This applies to PATCH/PUT requests on the proposal detail view.
    """
    message = 'You must be the project owner to manage this proposal.'
    
    def has_object_permission(self, request, view, obj):
        #Permission to protects PATCH/PUT 
        if request.method in permissions.SAFE_METHODS:
            return True # Allow read GET

        # Write permissions (PUT, PATCH) are only allowed if the request user 
        return obj.project.client == request.user
