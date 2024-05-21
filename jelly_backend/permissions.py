from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """
    Permission to allow access only to users with 'user_status' set to 'Active'.
    """

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado
        if not request.user.is_authenticated:
            return False

        # Verifica si el usuario tiene el estado 'Active'
        return request.user.user_status == 'A'
