from authentication.models import CustomUser, ContactInformation
from authentication.services.selectors import get_user_by_pk


def create_user(email: str, password: str, **kwargs):
    """
    Creates a new user model with given credentials. Password
    is automatically cached.
    """
    return CustomUser.objects.create_user(email, password, **kwargs)


def create_contact_info(contact_info: dict) -> ContactInformation:
    """
    Creates a new contact information record.
    """
    return ContactInformation.objects.create(**contact_info)


def update_or_create_contact_information(user_pk: int, contact_info: dict) -> tuple[ContactInformation, bool]:
    """
    Creates contact information for the already existing user.
    If contact information already exists, updates it.
    """
    user = get_user_by_pk(user_pk)
    if not user.contact_info:
        user.contact_info = create_contact_info(contact_info)
        user.save()
        is_created = True
    else:
        for field, value in contact_info.items():
            setattr(user.contact_info, field, value)
        user.contact_info.save()
        is_created = False
    return user.contact_info, is_created
