from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import UserSerializer, ContactInformationSerializer
from authentication.services.services import update_or_create_contact_information
from view_mixins.mixins.compounds import CompoundMixin


class UserView(CompoundMixin, GenericViewSet):
    """
    Handles the User model.
    """

    queryset = True
    serializer_class = {
        'create': UserSerializer,
        'contact_information': ContactInformationSerializer,
    }

    def create(self, request: Request):
        """
        Registers a new user model with given credentials.
        """
        serializer = self.get_request_serializer(data=request.data)
        created_user = serializer.create(serializer.validated_data)
        return Response(self.get_serializer(created_user).data, status=201)

    @action(methods=['put'], detail=True)
    def contact_information(self, request: Request, pk: int):
        """
        Updates or creates the contact information of specific user.
        """
        validated_data = self.get_request_data(data=request.data)
        contact_information, is_created = update_or_create_contact_information(pk, validated_data)
        return Response(self.get_serializer(contact_information).data, status=201 if is_created else 200)
