from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import *


class GenericFilterFormHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(GenericFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))


class ReferenceFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ReferenceFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'zotero_item',
                'page',
                css_id="basic_search_fields"
                ),
            )


class MonumentProtectionFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MonumentProtectionFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'current_land_use',
                'site_id',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    'heritage_status',
                    'natural_heritage_status',
                    'threats',
                    css_id="more"
                )
                )
            )


class ResearchQuestionFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ResearchQuestionFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'question',
                css_id="basic_search_fields"
                ),
####### Uncomment if there are advanced options ####################
            # Accordion(
            #     AccordionGroup(
            #         'Advanced search options',
            #         'zotero_item',
            #         'page',
            #         css_id="more"
            #     )
            #     )
            )


class ArchEntFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ArchEntFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'ent_type',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    'site_id',
                    'burial_type',
                    'burial_construction',
                    'settlement_fortification',
                    'settlement_occupation',
                    'topography',
                    'type_certainty',
                    'dating_certainty',
                    'location_certainty',
                    'period',
                    # 'public',
                    css_id="more"
                    ),
                )
            )


class SiteFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(SiteFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'has_research_activity',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    # 'public',
                    'cadastral_community',
                    # 'cadastral_number',
                    'heritage_number',
                    'plot_number',
                    'ownership',
                    'other_period',
                    'accessibility',
                    'visibility',
                    'infrastructure',
                    'long_term_management',
                    'potential_surrounding',
                    # 'museum',
                    css_id="more",
                    css_class="test"
                    ),
                ),
            Accordion(
                AccordionGroup(
                    'Research Activity search options',
                    'has_research_activity__start_date',
                    'has_research_activity__end_date',
                    'has_research_activity__responsible_researcher',
                    'has_research_activity__responsible_institution',
                    'has_research_activity__research_type',
                    'has_research_activity__research_method',
                    'has_research_activity__research_question',
                    'has_research_activity__generation_data_set',
                    css_id="research_activity_options"
                    ),
                ),
            Accordion(
                AccordionGroup(
                    'Arch. Entity search options',
                    'has_archent__ent_type',
                    'has_archent__burial_type',
                    'has_archent__settlement_fortification',
                    'has_archent__settlement_occupation',
                    'has_archent__topography',
                    'has_archent__type_certainty',
                    'has_archent__dating_certainty',
                    'has_archent__location_certainty',
                    'has_archent__period',
                    'has_archent__period__start_date',
                    'has_archent__period__start_date_latest',
                    'has_archent__period__end_date',
                    'has_archent__period__end_date_latest',
                    css_id="arch_entity_options"
                    ),
                ),
            Accordion(
                AccordionGroup(
                    'Monument protection search options',
                    'has_monument_protection__current_land_use',
                    'has_monument_protection__heritage_status',
                    'has_monument_protection__natural_heritage_status',
                    'has_monument_protection__threats',
                    css_id="monument_protection_options"
                    ),
                )
            )


class ResearchEventFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ResearchEventFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    'start_date',
                    'end_date',
                    'responsible_researcher',
                    'responsible_institution',
                    'research_type',
                    'research_method',
                    'research_question',
                    'generation_data_set',
                    css_id="more"
                )
                )
            )


class AltNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AltNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'label',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    'language',
                    css_id="more"
                    ),
                )
            )


class PeriodFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PeriodFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    # 'public',
                    'start_date',
                    'start_date_latest',
                    'end_date',
                    'end_date_latest',
                    'country',
                    css_id="more"
                    ),
                )
            )


class PersonFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PersonFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'written_name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options',
                    'acad_title',
                    'alt_names',
                    'authority_url',
                    'belongs_to_institution',
                    css_id="more"
                    ),
                )
            )


class AlternativeNameFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AlternativeNameFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                css_id="basic_search_fields"
                ),
####### Uncomment and add your fields if there are advanced options ####################
            # Accordion(
            #     AccordionGroup(
            #         'Advanced search options',
            #         'zotero_item',
            #         'page',
            #         css_id="more"
            #     )
            #     )
            )


class InstitutionFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(InstitutionFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'written_name',
                'alt_names',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options'
                    'authority_url',
                    'location',
                    css_id="more"
                    ),
                )
            )


class PlaceFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(PlaceFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'name',
                'alternative_name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search options'
                    'geonames_id',
                    'part_of',
                    css_id="more"
                    ),
                )
            )
