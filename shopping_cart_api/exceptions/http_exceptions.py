from rest_framework import status
from rest_framework.exceptions import APIException


class StateConflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Request conflicts with state of the server.'
    default_code = 'conflict'
