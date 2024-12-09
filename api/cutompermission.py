from rest_framework.permissions import BasePermission
from rest_framework import permissions
from .models import User

class IsStudent(permissions.BasePermission):
    """
    Custom permission to allow only users with the 'student' role to access API 
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has the role 'student' role

        return request.user.is_authenticated and request.user.role == 'student'
    
    
    

    





    
    
