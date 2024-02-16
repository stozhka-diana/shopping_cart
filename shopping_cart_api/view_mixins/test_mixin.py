from unittest.mock import patch, MagicMock

from view_mixins.mixins.multiple_serializers import MultipleSerializerMixin


class TestMultipleSerializerMixin:

    @patch.dict('view_mixins.mixins.multiple_serializers.__builtins__', {'super': lambda: MagicMock()})
    def test_if_serializer_class_is_not_dict_returns_what_returns_parent_method(self):
        assert isinstance(MultipleSerializerMixin().get_serializer_class(), MagicMock)

    @patch.dict(
        'view_mixins.mixins.multiple_serializers.__builtins__',
        {'super': lambda: type('class', (), {'get_serializer_class': lambda: {}})}
    )
    @patch('view_mixins.mixins.multiple_serializers.MultipleSerializerMixin._get_serializer_from_dict')
    def test_if_parent_method_returns_dict_it_will_call_method_for_it(self, mocked_method):
        return_value = 'serializer from dict'
        mocked_method.return_value = return_value
        assert MultipleSerializerMixin().get_serializer_class() == return_value

    def test_get_serializer_from_dict_return_first_value_if_it_is_a_string_field(self):
        return_serializer = 'correct serializer class'
        fake_action = 'action'
        MultipleSerializerMixin.serializer_class = {
            fake_action: return_serializer,
            (fake_action, 'another field'): 'invalid serializer'
        }
        MultipleSerializerMixin.action = fake_action
        assert MultipleSerializerMixin()._get_serializer_from_dict() == return_serializer

    def test_if_action_not_in_dict_it_will_return_it_from_tuples(self):
        return_serializer = 'correct serializer class'
        fake_action = 'action'
        MultipleSerializerMixin.action = fake_action
        MultipleSerializerMixin.serializer_class = {
            fake_action + '1': 'invalid serializer',
            (fake_action, 'another field'): return_serializer,
            ('some field', 'another field1'): 'wrong_value',
        }

        assert MultipleSerializerMixin()._get_serializer_from_dict() == return_serializer
