from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError


class ValidationError(DRFValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Неверный запрос'
    default_code = 'invalid'
