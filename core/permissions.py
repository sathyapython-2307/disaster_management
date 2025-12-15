from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

# Role definitions
ADMIN = 'admin'
ANALYST = 'analyst'
RESPONDER = 'responder'
PUBLIC = 'public'

ALL_ROLES = [ADMIN, ANALYST, RESPONDER, PUBLIC]

# Role hierarchy
ROLE_HIERARCHY = {
    ADMIN: [ADMIN, ANALYST, RESPONDER, PUBLIC],
    ANALYST: [ANALYST, RESPONDER, PUBLIC],
    RESPONDER: [RESPONDER, PUBLIC],
    PUBLIC: [PUBLIC],
}

# Permission mapping
ROLE_PERMISSIONS = {
    ADMIN: [
        'manage_users',
        'manage_system',
        'view_audit_logs',
        'manage_geofences',
        'manage_data_sources',
        'configure_alerts',
        'view_all_disasters',
        'view_all_analytics',
        'manage_policies',
    ],
    ANALYST: [
        'view_disasters',
        'view_analytics',
        'export_reports',
        'view_risk_models',
    ],
    RESPONDER: [
        'view_disasters',
        'acknowledge_alerts',
        'manage_incidents',
        'view_active_events',
    ],
    PUBLIC: [
        'view_public_alerts',
        'view_public_disasters',
    ],
}


def require_role(*allowed_roles):
    """Decorator to restrict view access by role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden('You do not have permission to access this page.')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_permission(permission):
    """Decorator to restrict view access by permission"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            user_permissions = ROLE_PERMISSIONS.get(request.user.role, [])
            if permission not in user_permissions:
                return HttpResponseForbidden('You do not have permission to perform this action.')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


class IsAdmin(BasePermission):
    """Permission class for admin-only access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == ADMIN


class IsAdminOrAnalyst(BasePermission):
    """Permission class for admin and analyst access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in [ADMIN, ANALYST]


class IsAdminOrResponder(BasePermission):
    """Permission class for admin and responder access"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in [ADMIN, RESPONDER]


class IsAuthenticated(BasePermission):
    """Permission class for authenticated users"""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class HasPermission(BasePermission):
    """Permission class for checking specific permissions"""
    def __init__(self, permission):
        self.permission = permission
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        user_permissions = ROLE_PERMISSIONS.get(request.user.role, [])
        return self.permission in user_permissions


def check_role_permission(user, permission):
    """Check if user has a specific permission"""
    if not user or not user.is_authenticated:
        return False
    
    user_permissions = ROLE_PERMISSIONS.get(user.role, [])
    return permission in user_permissions


def get_user_role_display(role):
    """Get display name for role"""
    role_display = {
        ADMIN: 'Administrator',
        ANALYST: 'Analyst',
        RESPONDER: 'Responder',
        PUBLIC: 'Public Viewer',
    }
    return role_display.get(role, 'Unknown')
