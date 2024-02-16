class EagerLoadedSerializerMixin:
    """
    The base class for populating instance for serializing
    with db data.
    """

    def __new__(cls, instance=None, *args, eager_loading=False, **kwargs):
        if eager_loading and instance is not None:
            instance = cls.setup_eager_loading(instance, kwargs.get('many', False))
        return super().__new__(cls, instance, *args, **kwargs)

    def __init__(self, *args, eager_loading=False, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def setup_eager_loading(value, many: bool):
        """
        This method is called when the queryset must be populated with data.
        It must return the same `value` argument.
        """
        raise NotImplementedError(
            "You haven't implemented the `setup_eager_loading` method for the data populating."
        )
