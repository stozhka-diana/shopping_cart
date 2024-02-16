from rest_framework import serializers

from authentication.models import CustomUser, ContactInformation
from authentication.services.services import create_user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password',
            'repeat_password',
        ]
        extra_kwargs = {
            'username': {'required': False},
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Validates that passwords that are provided match
        each other.
        """
        if data['repeat_password'] != data['password']:
            raise serializers.ValidationError({"repeat_password": "Passwords must match each other."})
        return data

    def create(self, validated_data: dict):
        """
        Creates a new user model.
        """
        user_credentials = ['username', 'first_name', 'last_name', 'email', 'password']
        return create_user(
            **{field: value for field, value in validated_data.items() if field in user_credentials}
        )


class ContactInformationSerializer(serializers.ModelSerializer):
    """
    Serializer for user's contact information.
    """

    class Meta:
        model = ContactInformation
        fields = ['id', 'phone_number', 'location']
