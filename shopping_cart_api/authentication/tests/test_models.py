import pytest

from authentication.models import CustomUser


@pytest.mark.django_db
class TestCustomUserManager:

    @pytest.mark.parametrize(
        'invalid_email',
        ['', 0, {}]
    )
    def test_create_user_must_retrieve_valid_email(self, invalid_email):
        with pytest.raises(ValueError):
            CustomUser.objects.create_user(invalid_email, 'qwerty')

    def test_create_superuser_has_superuser_fields_set_to_true(self):
        superuser = CustomUser.objects.create_superuser('test@test.com', 'qwerty')
        assert superuser.is_superuser
        assert superuser.is_active
        assert superuser.is_staff
