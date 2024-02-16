import pytest


@pytest.fixture
def user_credentials():
    return {
        "email": "another_user@mail.com",
        "username": "i_am_user",
        "first_name": "Mark",
        "last_name": "Zuckerberg",
        "password": "qwerty",
    }


@pytest.fixture
def user_credentials_for_registration(user_credentials):
    return {
        "email": "another_user@mail.com",
        "username": "i_am_user",
        "first_name": "Mark",
        "last_name": "Zuckerberg",
        "password": "qwerty",
        "repeat_password": "qwerty",
    }


@pytest.fixture
def contact_information():
    return {
        'phone_number': '+441234567890',
        'location': 'NY',
    }
