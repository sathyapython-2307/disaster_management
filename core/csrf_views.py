"""
CSRF and error handling views that return JSON for API requests
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    """Handle CSRF failures by returning JSON for API requests"""
    logger.warning(f"CSRF failure: {reason}")
    return JsonResponse(
        {
            'error': 'CSRF validation failed',
            'detail': 'Missing or invalid CSRF token'
        },
        status=403,
        content_type='application/json'
    )


def handle_403(request, exception=None):
    """Handle 403 Forbidden errors"""
    logger.warning(f"403 Forbidden: {exception}")
    return JsonResponse(
        {
            'error': 'Forbidden',
            'detail': 'You do not have permission to access this resource'
        },
        status=403,
        content_type='application/json'
    )


def handle_404(request, exception=None):
    """Handle 404 Not Found errors"""
    logger.warning(f"404 Not Found: {request.path}")
    return JsonResponse(
        {
            'error': 'Not found',
            'detail': f'The requested resource was not found: {request.path}'
        },
        status=404,
        content_type='application/json'
    )


def handle_500(request):
    """Handle 500 Internal Server errors"""
    logger.error("500 Internal Server Error")
    return JsonResponse(
        {
            'error': 'Internal server error',
            'detail': 'An unexpected error occurred on the server'
        },
        status=500,
        content_type='application/json'
    )
