from rest_framework.exceptions import NotFound

from authentication.models import CustomUser


def get_user_by_pk(pk: int) -> CustomUser:
    """
    Gets a user model or raises 404 exception.
    """
    try:
        return CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        raise NotFound("User with id %s doesn't exist." % pk)
