import django_filters
from dal import autocomplete
from django.urls import reverse
from archiv.models import *
from bib.models import *
from entities.models import Place, AlternativeName, Institution, Person
from vocabs.models import SkosConcept, SkosConceptScheme
from vocabs.filters import generous_concept_filter
from shapes.models import CadastralCommunity


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
    current_land_use = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="current-land-use"
            ),
        help_text=MonumentProtection._meta.get_field('current_land_use').help_text,
        label=MonumentProtection._meta.get_field('current_land_use').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/current-land-use",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    heritage_status = django_filters.ChoiceFilter(
        help_text=MonumentProtection._meta.get_field('heritage_status').help_text,
        label=MonumentProtection._meta.get_field('heritage_status').verbose_name,
        choices=HERITAGE_STATUS_CHOICES
        )
    natural_heritage_status = django_filters.ChoiceFilter(
        help_text=MonumentProtection._meta.get_field('natural_heritage_status').help_text,
        label=MonumentProtection._meta.get_field('natural_heritage_status').verbose_name,
        choices=HERITAGE_STATUS_CHOICES
        )
    threats = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="threats"
            ),
        help_text=MonumentProtection._meta.get_field('threats').help_text,
        label=MonumentProtection._meta.get_field('threats').verbose_name,
        method=generous_concept_filter
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
    ent_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="archaeological-entity-type"
            ),
        help_text=ArchEnt._meta.get_field('ent_type').help_text,
        label=ArchEnt._meta.get_field('ent_type').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/archaeological-entity-type",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    burial_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="burial-type"
            ),
        help_text=ArchEnt._meta.get_field('burial_type').help_text,
        label=ArchEnt._meta.get_field('burial_type').verbose_name,
        method=generous_concept_filter
        )
    burial_construction = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="burial-construction"
            ),
        help_text=ArchEnt._meta.get_field('burial_construction').help_text,
        label=ArchEnt._meta.get_field('burial_construction').verbose_name,
        method=generous_concept_filter
        )
    site_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Site.objects.all(),
        help_text=ArchEnt._meta.get_field('site_id').help_text,
        label=ArchEnt._meta.get_field('site_id').verbose_name
        )
    settlement_fortification = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="settlement-fortification"
            ),
        help_text=ArchEnt._meta.get_field('settlement_fortification').help_text,
        label=ArchEnt._meta.get_field('settlement_fortification').verbose_name,
        method=generous_concept_filter
        )
    settlement_occupation = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="settlement-occupation"
            ),
        help_text=ArchEnt._meta.get_field('settlement_occupation').help_text,
        label=ArchEnt._meta.get_field('settlement_occupation').verbose_name,
        method=generous_concept_filter
        )
    topography = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="topography"
            ),
        help_text=ArchEnt._meta.get_field('topography').help_text,
        label=ArchEnt._meta.get_field('topography').verbose_name,
        method=generous_concept_filter
        )
    type_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('type_certainty').help_text,
        label=ArchEnt._meta.get_field('type_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    dating_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('dating_certainty').help_text,
        label=ArchEnt._meta.get_field('dating_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    location_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('location_certainty').help_text,
        label=ArchEnt._meta.get_field('location_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    period = django_filters.ModelMultipleChoiceFilter(
        queryset=Period.objects.all(),
        help_text=ArchEnt._meta.get_field('period').help_text,
        label=ArchEnt._meta.get_field('period').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="/archiv-ac/period-autocomplete",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
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
    has_research_activity = django_filters.ModelMultipleChoiceFilter(
        queryset=ResearchEvent.objects.all(),
        name='has_research_activity',
        label="Research activity"
        )
    cadastral_community = django_filters.ModelMultipleChoiceFilter(
        queryset=CadastralCommunity.objects.all(),
        help_text=Site._meta.get_field('cadastral_community').help_text,
        label=Site._meta.get_field('cadastral_community').verbose_name,
        widget=autocomplete.Select2Multiple(
            url='shapes-ac:cadastralcommunity-autocomplete',
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
    ownership = django_filters.ChoiceFilter(
        choices=SITE_OWNERSHIP,
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
    accessibility = django_filters.ChoiceFilter(
        choices=SITE_ACCESSIBILITY,
        help_text=Site._meta.get_field('accessibility').help_text,
        label=Site._meta.get_field('accessibility').verbose_name
        )
    visibility = django_filters.ChoiceFilter(
        choices=SITE_VISIBILITY,
        help_text=Site._meta.get_field('visibility').help_text,
        label=Site._meta.get_field('visibility').verbose_name
        )
    infrastructure = django_filters.ChoiceFilter(
        choices=SITE_INFRASTRUCTURE,
        help_text=Site._meta.get_field('infrastructure').help_text,
        label=Site._meta.get_field('infrastructure').verbose_name
        )
    long_term_management = django_filters.ChoiceFilter(
        choices=SITE_LONGTERMMANGEMENT,
        help_text=Site._meta.get_field('long_term_management').help_text,
        label=Site._meta.get_field('long_term_management').verbose_name
        )
    potential_surrounding = django_filters.ChoiceFilter(
        choices=SITE_POTENTIALSURROUNDINGS,
        help_text=Site._meta.get_field('potential_surrounding').help_text,
        label=Site._meta.get_field('potential_surrounding').verbose_name
        )
    # museum = django_filters.ModelMultipleChoiceFilter(
    #     queryset=Institution.objects.all(),
    #     help_text=Site._meta.get_field('museum').help_text,
    #     label=Site._meta.get_field('museum').verbose_name,
    #     )
##################### Research Activity Fields ####################
    has_research_activity__start_date = django_filters.DateFilter(
        lookup_expr='gte',
        help_text=ResearchEvent._meta.get_field('start_date').help_text,
        label=ResearchEvent._meta.get_field('start_date').verbose_name
        )
    has_research_activity__end_date = django_filters.DateFilter(
        lookup_expr='lte',
        help_text=ResearchEvent._meta.get_field('end_date').help_text,
        label=ResearchEvent._meta.get_field('end_date').verbose_name
        )
    has_research_activity__responsible_researcher = django_filters.ModelMultipleChoiceFilter(
        queryset=Person.objects.all(),
        help_text=ResearchEvent._meta.get_field('responsible_researcher').help_text,
        label=ResearchEvent._meta.get_field('responsible_researcher').verbose_name
        )
    has_research_activity__responsible_institution = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(),
        help_text=ResearchEvent._meta.get_field('responsible_institution').help_text,
        label=ResearchEvent._meta.get_field('responsible_institution').verbose_name
        )
    has_research_activity__research_type = django_filters.ModelChoiceFilter(
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="research-type"),
        help_text=ResearchEvent._meta.get_field('research_type').help_text,
        label=ResearchEvent._meta.get_field('research_type').verbose_name,
        )
    has_research_activity__research_method = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="research-methods"),
        help_text=ResearchEvent._meta.get_field('research_method').help_text,
        label=ResearchEvent._meta.get_field('research_method').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/research-methods",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    has_research_activity__research_question = django_filters.ModelMultipleChoiceFilter(
        queryset=ResearchQuestion.objects.all(),
        help_text=ResearchEvent._meta.get_field('research_question').help_text,
        label=ResearchEvent._meta.get_field('research_question').verbose_name
        )
    has_research_activity__generation_data_set = django_filters.DateFilter(
        lookup_expr='exact',
        help_text=ResearchEvent._meta.get_field('generation_data_set').help_text,
        label=ResearchEvent._meta.get_field('generation_data_set').verbose_name
        )
##################### Arch.Entity Fields ####################
    has_archent__ent_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="archaeological-entity-type"
            ),
        help_text=ArchEnt._meta.get_field('ent_type').help_text,
        label=ArchEnt._meta.get_field('ent_type').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/archaeological-entity-type",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    has_archent__burial_type = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="burial-type"
            ),
        help_text=ArchEnt._meta.get_field('burial_type').help_text,
        label=ArchEnt._meta.get_field('burial_type').verbose_name,
        method=generous_concept_filter
        )
    has_archent__settlement_fortification = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="settlement-fortification"
            ),
        help_text=ArchEnt._meta.get_field('settlement_fortification').help_text,
        label=ArchEnt._meta.get_field('settlement_fortification').verbose_name,
        method=generous_concept_filter
        )
    has_archent__settlement_occupation = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="settlement-occupation"
            ),
        help_text=ArchEnt._meta.get_field('settlement_occupation').help_text,
        label=ArchEnt._meta.get_field('settlement_occupation').verbose_name,
        method=generous_concept_filter
        )
    has_archent__topography = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="topography"
            ),
        help_text=ArchEnt._meta.get_field('topography').help_text,
        label=ArchEnt._meta.get_field('topography').verbose_name,
        method=generous_concept_filter
        )
    has_archent__type_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('type_certainty').help_text,
        label=ArchEnt._meta.get_field('type_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    has_archent__dating_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('dating_certainty').help_text,
        label=ArchEnt._meta.get_field('dating_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    has_archent__location_certainty = django_filters.ChoiceFilter(
        help_text=ArchEnt._meta.get_field('location_certainty').help_text,
        label=ArchEnt._meta.get_field('location_certainty').verbose_name,
        choices=ARCHENT_CERTAINTY
        )
    has_archent__period = django_filters.ModelMultipleChoiceFilter(
        queryset=Period.objects.all(),
        help_text=ArchEnt._meta.get_field('period').help_text,
        label=ArchEnt._meta.get_field('period').verbose_name,
        widget=autocomplete.Select2Multiple(
            url="/archiv-ac/period-autocomplete",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    has_archent__period__start_date = django_filters.NumberFilter(
        lookup_expr='exact',
        help_text=Period._meta.get_field('start_date').help_text,
        label=Period._meta.get_field('start_date').verbose_name
        )
    has_archent__period__start_date_latest = django_filters.NumberFilter(
        lookup_expr='exact',
        help_text=Period._meta.get_field('start_date_latest').help_text,
        label=Period._meta.get_field('start_date_latest').verbose_name
        )
    has_archent__period__end_date = django_filters.NumberFilter(
        lookup_expr='exact',
        help_text=Period._meta.get_field('end_date').help_text,
        label=Period._meta.get_field('end_date').verbose_name
        )
    has_archent__period__end_date_latest = django_filters.NumberFilter(
        lookup_expr='exact',
        help_text=Period._meta.get_field('end_date_latest').help_text,
        label=Period._meta.get_field('end_date_latest').verbose_name
        )
##################### Monument Protection Fields ####################
    has_monument_protection__current_land_use = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="current-land-use"
            ),
        help_text=MonumentProtection._meta.get_field('current_land_use').help_text,
        label=MonumentProtection._meta.get_field('current_land_use').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/current-land-use",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    has_monument_protection__heritage_status = django_filters.ChoiceFilter(
        help_text=MonumentProtection._meta.get_field('heritage_status').help_text,
        label=MonumentProtection._meta.get_field('heritage_status').verbose_name,
        choices=HERITAGE_STATUS_CHOICES
        )
    has_monument_protection__natural_heritage_status = django_filters.ChoiceFilter(
        help_text=MonumentProtection._meta.get_field('natural_heritage_status').help_text,
        label=MonumentProtection._meta.get_field('natural_heritage_status').verbose_name,
        choices=HERITAGE_STATUS_CHOICES
        )
    has_monument_protection__threats = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(
            scheme__dc_title__icontains="threats"
            ),
        help_text=MonumentProtection._meta.get_field('threats').help_text,
        label=MonumentProtection._meta.get_field('threats').verbose_name,
        method=generous_concept_filter
        )



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
    start_date = django_filters.DateFilter(
        lookup_expr='gte',
        help_text=ResearchEvent._meta.get_field('start_date').help_text,
        label=ResearchEvent._meta.get_field('start_date').verbose_name
        )
    end_date = django_filters.DateFilter(
        lookup_expr='lte',
        help_text=ResearchEvent._meta.get_field('end_date').help_text,
        label=ResearchEvent._meta.get_field('end_date').verbose_name
        )
    responsible_researcher = django_filters.ModelMultipleChoiceFilter(
        queryset=Person.objects.all(),
        help_text=ResearchEvent._meta.get_field('responsible_researcher').help_text,
        label=ResearchEvent._meta.get_field('responsible_researcher').verbose_name
        )
    responsible_institution = django_filters.ModelMultipleChoiceFilter(
        queryset=Institution.objects.all(),
        help_text=ResearchEvent._meta.get_field('responsible_institution').help_text,
        label=ResearchEvent._meta.get_field('responsible_institution').verbose_name
        )
    research_type = django_filters.ModelChoiceFilter(
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="research-type"),
        help_text=ResearchEvent._meta.get_field('research_type').help_text,
        label=ResearchEvent._meta.get_field('research_type').verbose_name
        )
    research_method = django_filters.ModelMultipleChoiceFilter(
        queryset=SkosConcept.objects.filter(scheme__dc_title__icontains="research-methods"),
        help_text=ResearchEvent._meta.get_field('research_method').help_text,
        label=ResearchEvent._meta.get_field('research_method').verbose_name,
        method=generous_concept_filter,
        widget=autocomplete.Select2Multiple(
            url="/vocabs-ac/specific-concept-ac/research-methods",
            attrs={
                'data-placeholder': 'Autocomplete ...',
                'data-minimum-input-length': 3,
                },
        )
        )
    research_question = django_filters.ModelMultipleChoiceFilter(
        queryset=ResearchQuestion.objects.all(),
        help_text=ResearchEvent._meta.get_field('research_question').help_text,
        label=ResearchEvent._meta.get_field('research_question').verbose_name
        )
    generation_data_set = django_filters.DateFilter(
        lookup_expr='exact',
        help_text=ResearchEvent._meta.get_field('generation_data_set').help_text,
        label=ResearchEvent._meta.get_field('generation_data_set').verbose_name
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
