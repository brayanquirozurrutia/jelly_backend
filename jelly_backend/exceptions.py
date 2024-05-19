from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, DRFValidationError) and isinstance(exc.detail, dict):
        error_message = next(iter(exc.detail.values()))[0] if exc.detail else None
        if error_message:
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    return exception_handler(exc, context)
