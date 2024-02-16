from rest_framework.serializers import Serializer


class RequestValidationMixin:
    """
    Simplifies the request data retrieving process.
    """

    def get_request_data(self, *args, **kwargs):
        """
        Returns only request validated data.
        """
        return self.get_request_serializer(*args, **kwargs).validated_data

    def get_request_serializer(self, *args, **kwargs) -> Serializer:
        """
        Returns serializer with the validated request data. Raises exception
        if the validation fails.
        """
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer
