from django_filters import CharFilter, BaseInFilter


class CharInFilter(BaseInFilter, CharFilter):
    """
    Filters chars that are comma-separated from the
    query parameters.
    """
    pass
