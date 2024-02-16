import pytest
from model_bakery import baker
from rest_framework.exceptions import NotFound

from authentication.models import CustomUser, ContactInformation
from authentication.services.services import create_user, update_or_create_contact_information


@pytest.mark.django_db
class TestCustomUserServices:

    def test_create_user_creates_record_in_db(self, user_credentials):
        assert not CustomUser.objects.all().exists()
        new_user = create_user(**user_credentials)
        assert CustomUser.objects.first() == new_user

    def test_create_user_automatically_hash_password(self, user_credentials):
        new_user = create_user(**user_credentials)
        assert new_user.password != user_credentials['password']


@pytest.mark.django_db
class TestContactInformationServices:

    def test_if_user_doesnt_exist_contact_information_will_not_be_created(self, contact_information):
        assert not ContactInformation.objects.all().exists()
        with pytest.raises(NotFound):
            update_or_create_contact_information(1, contact_information)
        assert not ContactInformation.objects.all().exists()

    def test_contact_information_is_successfully_created_if_user_exists(self, contact_information):
        user = baker.make(CustomUser)
        assert not ContactInformation.objects.all().exists()
        contact_info, is_created = update_or_create_contact_information(user.pk, contact_information)
        user.refresh_from_db()
        assert user.contact_info == contact_info
        assert is_created

    def test_if_user_has_already_contact_information_it_will_be_updated(self, contact_information):
        user = baker.make(CustomUser, contact_info=baker.make(ContactInformation, phone_number="+441234567822"))
        contact_info, is_created = update_or_create_contact_information(user.pk, contact_information)
        assert not is_created
        assert contact_information['phone_number'] == contact_info.phone_number
        assert contact_information['location'] == contact_info.location
