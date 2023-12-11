from rest_framework.permissions import BasePermission, IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken


class IsAccountOwner(BasePermission):
    """
    Custom permission to only allow account owners to perform certain actions.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the account

        # Extract user from JWT token
        if isinstance(request.auth, AccessToken):
            token_payload = request.auth.payload
            user = token_payload.get('user_id')
            return user and obj.user.id == user
        return False



