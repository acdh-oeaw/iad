import django_filters
from . models import CadastralCommunity

django_filters.filters.LOOKUP_TYPES = [
    ('', '---------'),
    ('exact', 'Is equal to'),
    ('iexact', 'Is equal to (case insensitive)'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than/before'),
    ('gt', 'Greater than/after'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('icontains', 'Contains (case insensitive)'),
    ('not_contains', 'Does not contain'),
]


class CadastralCommunityListFilter(django_filters.FilterSet):
    cadcom_nam = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=CadastralCommunity._meta.get_field('cadcom_nam').help_text,
        label=CadastralCommunity._meta.get_field('cadcom_nam').verbose_name
        )

    class Meta:
        model = CadastralCommunity
        fields = [
            'id'
        ]
