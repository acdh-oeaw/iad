import django_filters
from . models import Municipality

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


class MunicipalityListFilter(django_filters.FilterSet):
    lau2nam = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Municipality._meta.get_field('lau2nam').help_text,
        label=Municipality._meta.get_field('lau2nam').verbose_name
        )
    lau2_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Municipality._meta.get_field('lau2_id').help_text,
        label=Municipality._meta.get_field('lau2_id').verbose_name
        )
    nuts3nam = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Municipality._meta.get_field('nuts3nam').help_text,
        label=Municipality._meta.get_field('nuts3nam').verbose_name
        )
    ctnam = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Municipality._meta.get_field('ctnam').help_text,
        label=Municipality._meta.get_field('ctnam').verbose_name
        )

    class Meta:
        model = Municipality
        fields = [
            'id', 'lau2nam', 'ctnam'
        ]
