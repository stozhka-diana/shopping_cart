from view_mixins.mixins.multiple_serializers import MultipleSerializerMixin
from view_mixins.mixins.request_validation import RequestValidationMixin


class CompoundMixin(MultipleSerializerMixin, RequestValidationMixin):
    pass
