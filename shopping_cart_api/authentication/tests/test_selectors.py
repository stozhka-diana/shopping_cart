import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from authentication.models import CustomUser
from authentication.services.selectors import get_user_by_pk


@pytest.mark.django_db
class TestCustomUserSelectors:

    def test_get_user_by_pk_raises_an_exception_if_none_exists(self):
        with pytest.raises(NotFound):
            get_user_by_pk(1)

    def test_get_user_by_pk_returns_specific_user(self):
        created_user = baker.make(CustomUser)
        user = get_user_by_pk(created_user.pk)
        assert created_user == user
