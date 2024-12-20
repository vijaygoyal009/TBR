from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Custom permission to grant access only to Admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsCoachUser(BasePermission):
    """
    Custom permission to grant access only to Coach users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'coach'



class IsRegularUser(BasePermission):
    """
    Custom permission to grant access only to regular users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'user'



class IsAdminOrRegularUser(BasePermission):
    """
    Custom permission to allow access to Admins or Regular Users.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            (request.user.role == 'admin' or request.user.role == 'user')
        )



class IsAdminOrCoach(BasePermission):
    """
    Custom permission to grant access only to Admins and Coaches.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.role == 'coach')
        )