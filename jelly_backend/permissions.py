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


class IsAdminUserLoggedIn(BasePermission):
    """
    Permission class to allow access only to admin users who are logged in.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.user_admin
        return False
