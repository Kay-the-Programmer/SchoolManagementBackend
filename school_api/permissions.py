from rest_framework import permissions

class IsAdministrator(permissions.BasePermission):
    """
    Custom permission to only allow administrators to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Administrator'

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to only allow teachers to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Teacher'

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow students to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Student'

class IsParent(permissions.BasePermission):
    """
    Custom permission to only allow parents to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'Parent'

class IsOwnerOrAdministrator(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or administrators to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or an administrator
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        
        if hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        
        return request.user.role == 'Administrator'

class IsTeacherOrAdministrator(permissions.BasePermission):
    """
    Custom permission to only allow teachers or administrators to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'Teacher' or request.user.role == 'Administrator'
        )

class IsStudentOrTeacherOrAdministrator(permissions.BasePermission):
    """
    Custom permission to only allow students, teachers, or administrators to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.role == 'Student' or 
            request.user.role == 'Teacher' or 
            request.user.role == 'Administrator'
        )