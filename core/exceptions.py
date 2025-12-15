"""
Custom exception handlers for DRF to ensure all errors return JSON
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that ensures all exceptions are returned as JSON.
    This handles both DRF exceptions and Django exceptions.
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        # DRF handled the exception, ensure it has proper headers
        response['Content-Type'] = 'application/json'
        return response
    
    # If DRF didn't handle it, create a JSON response for unhandled exceptions
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return Response(
        {
            'error': 'Internal server error',
            'detail': str(exc) if str(exc) else 'An unexpected error occurred'
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content_type='application/json'
    )
