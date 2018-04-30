import django_filters
from dal import autocomplete
from django.urls import reverse
from archiv.models import *
from bib.models import *
from entities.models import Place, AlternativeName, Institution, Person
from vocabs.models import SkosConcept, SkosConceptScheme
from vocabs.filters import generous_concept_filter


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


class ReferenceListFilter(django_filters.FilterSet):
    zotero_item = django_filters.ModelMultipleChoiceFilter(
        queryset=Reference.objects.all(),
        help_text=Reference._meta.get_field('zotero_item').help_text,
        label=Reference._meta.get_field('zotero_item').verbose_name
        )

    class Meta:
        model = Reference
        fields = '__all__'


class MonumentProtectionListFilter(django_filters.FilterSet):
    current_land_use = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.all(),
        help_text=MonumentProtection._meta.get_field('current_land_use').help_text,
        label=MonumentProtection._meta.get_field('current_land_use').verbose_name
        )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        help_text=MonumentProtection._meta.get_field('site_id').help_text,
        label=MonumentProtection._meta.get_field('site_id').verbose_name
        )

    class Meta:
        model = MonumentProtection
        exclude = ['polygon']


class ResearchQuestionListFilter(django_filters.FilterSet):
    question = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ResearchQuestion._meta.get_field('question').help_text,
        label=ResearchQuestion._meta.get_field('question').verbose_name
        )

    class Meta:
        model = ResearchQuestion
        fields = '__all__'


class ArchEntListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ArchEnt._meta.get_field('name').help_text,
        label=ArchEnt._meta.get_field('name').verbose_name
        )

    class Meta:
        model = ArchEnt
        exclude = ['polygon']


class SiteListFilter(django_filters.FilterSet):
    # url = reverse('vocabs-ac:specific-concept-ac', kwargs={'schema': 'archenttype'})
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('name').help_text,
        label=Site._meta.get_field('name').verbose_name
        )
    has_archent__ent_type = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/archenttype",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        ),
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="archenttype"),
        help_text="Site contains specific archaeological entity?",
        label="Greedy Archaeological Entity"
        )
    example = django_filters.ModelMultipleChoiceFilter(
        name="has_archent__ent_type",
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/archenttype",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        ),
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="archenttype"),
        help_text="Site contains specific archaeological entity?",
        label="Generous Archaeological Entity"
        )
    has_research_activity = django_filters.ModelMultipleChoiceFilter(
        queryset=ResearchEvent.objects.all(),
        name='has_research_activity',
        label="Research activity"
        )
    cadastral_community = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.objects.all(),
        help_text=Site._meta.get_field('cadastral_community').help_text,
        label=Site._meta.get_field('cadastral_community').verbose_name,
        widget=autocomplete.Select2Multiple(
            url='entities-ac:place-autocomplete-search',
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    cadastral_number = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('cadastral_number').help_text,
        label=Site._meta.get_field('cadastral_number').verbose_name
        )
    heritage_number = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('heritage_number').help_text,
        label=Site._meta.get_field('heritage_number').verbose_name
        )
    plot_number = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('plot_number').help_text,
        label=Site._meta.get_field('plot_number').verbose_name
        )
    ownership = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('ownership').help_text,
        label=Site._meta.get_field('ownership').verbose_name
        )
    other_period = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="other-present-archaeological-period"),
        help_text=Site._meta.get_field('other_period').help_text,
        label=Site._meta.get_field('other_period').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/other-present-archaeological-period",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    accessibility = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('accessibility').help_text,
        label=Site._meta.get_field('accessibility').verbose_name
        )
    visibility = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('visibility').help_text,
        label=Site._meta.get_field('visibility').verbose_name
        )
    infrastructure = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('infrastructure').help_text,
        label=Site._meta.get_field('infrastructure').verbose_name
        )
    long_term_management = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('long_term_management').help_text,
        label=Site._meta.get_field('long_term_management').verbose_name
        )
    potential_surrounding = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Site._meta.get_field('potential_surrounding').help_text,
        label=Site._meta.get_field('potential_surrounding').verbose_name
        )
    # museum = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Institution.objects.all(),
    #     help_text=Site._meta.get_field('museum').help_text,
    #     label=Site._meta.get_field('museum').verbose_name,
    #     )


    class Meta:
        model = Site
        exclude = ['polygon']


class AltNameListFilter(django_filters.FilterSet):
    label = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=AltName._meta.get_field('label').help_text,
        label=AltName._meta.get_field('label').verbose_name
        )

    class Meta:
        model = AltName
        exclude = ['polygon']


class ResearchEventListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=ResearchEvent._meta.get_field('name').help_text,
        label=ResearchEvent._meta.get_field('name').verbose_name
        )

    class Meta:
        model = ResearchEvent
        exclude = ['polygon']


class PeriodListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Period._meta.get_field('name').help_text,
        label=Period._meta.get_field('name').verbose_name
        )

    class Meta:
        model = Period
        exclude = ['polygon']


class PersonListFilter(django_filters.FilterSet):
    current_land_use = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(),
        help_text=MonumentProtection._meta.get_field('site_id').help_text,
        label=MonumentProtection._meta.get_field('site_id').verbose_name
        )
    belongs_to_institution = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        help_text=MonumentProtection._meta.get_field('site_id').help_text,
        label=MonumentProtection._meta.get_field('site_id').verbose_name
        )

    class Meta:
        model = Person
        fields = "__all__"


class InstitutionListFilter(django_filters.FilterSet):
    written_name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Institution._meta.get_field('written_name').help_text,
        label=Institution._meta.get_field('written_name').verbose_name
        )
    alt_names = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Institution._meta.get_field('alt_names').help_text,
        label=Institution._meta.get_field('alt_names').verbose_name
        )
    authority_url = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Institution._meta.get_field('authority_url').help_text,
        label=Institution._meta.get_field('authority_url').verbose_name
        )
    location = django_filters.ModelMultipleChoiceFilter(
        queryset=AlternativeName.objects.all(),
        help_text=Institution._meta.get_field('location').help_text,
        label=Institution._meta.get_field('location').verbose_name
        )

    class Meta:
        model = Institution
        fields = [
            'id', 'written_name', 'authority_url', 'location'
        ]


class PlaceListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Place._meta.get_field('name').help_text,
        label=Place._meta.get_field('name').verbose_name
        )
    geonames_id = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=Place._meta.get_field('geonames_id').help_text,
        label=Place._meta.get_field('geonames_id').verbose_name
        )
    alt_names = django_filters.ModelMultipleChoiceFilter(
        queryset=AlternativeName.objects.all(),
        help_text=Place._meta.get_field('alt_names').help_text,
        label=Place._meta.get_field('alt_names').verbose_name
        )
    part_of = django_filters.ModelMultipleChoiceFilter(
        queryset=Place.objects.all(),
        help_text=Place._meta.get_field('part_of').help_text,
        label=Place._meta.get_field('part_of').verbose_name
        )

    class Meta:
        model = Place
        fields = [
            'id'
        ]


class AlternativeNameListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        help_text=AlternativeName._meta.get_field('name').help_text,
        label=AlternativeName._meta.get_field('name').verbose_name
        )

    class Meta:
        model = AlternativeName
        fields = [
            'id'
        ]
