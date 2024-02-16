from unittest.mock import patch, MagicMock

import pytest
from rest_framework.serializers import Serializer

from eager_loaded_serializer.mixin import EagerLoadedSerializerMixin


class TestEagerLoadedSerializerMixin:

    @pytest.fixture
    def compound_class(self):
        class SomeSerializer(EagerLoadedSerializerMixin, Serializer):
            pass

        return SomeSerializer

    def test_if_setup_eager_loading_not_implemented_exception_raised(self):
        with pytest.raises(NotImplementedError):
            EagerLoadedSerializerMixin.setup_eager_loading('value', False)

    def test_if_eager_loading_parameter_is_not_passed_method_is_not_called(self, compound_class):
        assert isinstance(compound_class({}), Serializer)

    @patch("eager_loaded_serializer.mixin.EagerLoadedSerializerMixin.setup_eager_loading")
    def test_if_eager_loading_parameter_is_specified_eager_loaded_method_called_with_instance_parameter(
            self, mocked_method: MagicMock, compound_class
    ):
        def raise_exception(value, many):
            raise ValueError(value)

        mocked_method.side_effect = raise_exception
        some_model = 'model'
        with pytest.raises(ValueError) as e:
            compound_class(some_model, eager_loading=True)
        assert str(e.value) == some_model

    @patch("eager_loaded_serializer.mixin.EagerLoadedSerializerMixin.setup_eager_loading")
    @pytest.mark.parametrize(
        'many, method_value',
        [
            (True, 'True'),
            (False, 'False'),
        ]
    )
    def test_many_parameter_passed_to_method_too(self, mocked_method, many, compound_class, method_value):
        def raise_exception(value, many):
            raise ValueError(str(many))

        mocked_method.side_effect = raise_exception
        with pytest.raises(ValueError) as e:
            compound_class('value', eager_loading=True, many=many)
        assert str(e.value) == method_value

    @patch("eager_loaded_serializer.mixin.EagerLoadedSerializerMixin.setup_eager_loading")
    def test_if_many_not_specified_value_is_false(self, mocked_method, compound_class):
        def raise_exception(value, many):
            raise ValueError(str(many))

        mocked_method.side_effect = raise_exception
        with pytest.raises(ValueError) as e:
            compound_class('value', eager_loading=True)
        assert str(e.value) == str(False)
