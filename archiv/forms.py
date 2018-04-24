from dal import autocomplete
from django import forms
from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import *


class MonumentProtectionForm(forms.ModelForm):
    class Meta:
        model = MonumentProtection
        fields = [
            'public', 'polygon', 'current_land_use',
            'heritage_status', 'threats', 'comment'
            ]
        widgets = {
            'alt_name': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:altname-autocomplete'),
            'literature': autocomplete.ModelSelect2Multiple(
                url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
            'site_id': autocomplete.ModelSelect2(
                url='archiv-ac:site-autocomplete'),
            'current_land_use': autocomplete.ModelSelect2Multiple(
                url='/vocabs-ac/specific-concept-ac/current-land-use'),
            'threats': autocomplete.ModelSelect2Multiple(
                url='/vocabs-ac/specific-concept-ac/threats'),
        }

    def __init__(self, *args, **kwargs):
        super(MonumentProtectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ResearchQuestionForm(forms.ModelForm):
    class Meta:
        model = ResearchQuestion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ResearchQuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ArchEntForm(forms.ModelForm):
    class Meta:
        model = ArchEnt
        fields = [
            'public', 'polygon', 'site_id', 'name', 'alt_name',
            'ent_type', 'topography', 'burial_type', 'period', 'type_certainty',
            'dating_certainty', 'location_certainty', 'comment'
        ]
        widgets = {
            'alt_name': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:altname-autocomplete'),
            'literature': autocomplete.ModelSelect2Multiple(
                url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
            'site_id': autocomplete.ModelSelect2(
                url='archiv-ac:site-autocomplete'),
            'ent_type': autocomplete.ModelSelect2(
                url='/vocabs-ac/specific-concept-ac/archaeological-entity-type'),
            'topography': autocomplete.ModelSelect2(
                url='/vocabs-ac/specific-concept-ac/topography'),
            'burial_type': autocomplete.ModelSelect2(
                url='/vocabs-ac/specific-concept-ac/burial-type'),
            'period': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:period-autocomplete'),
            }

    def __init__(self, *args, **kwargs):
        super(ArchEntForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class ResearchEventForm(forms.ModelForm):
    class Meta:
        model = ResearchEvent
        fields = [
            'public', 'polygon', 'research_type', 'research_method', 'start_date', 'end_date',
            'identifier', 'responsible_researcher', 'responsible_institution',
            'research_question', 'comment', 'generation_data_set'
        ]
        widgets = {
            'alt_name': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:altname-autocomplete'),
            'literature': autocomplete.ModelSelect2Multiple(
                url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
            'responsible_researcher': autocomplete.ModelSelect2Multiple(
                url='entities-ac:person-autocomplete'),
            'responsible_institution': autocomplete.ModelSelect2Multiple(
                url='entities-ac:institution-autocomplete'),
            'research_type': autocomplete.ModelSelect2(
                url='/vocabs-ac/specific-concept-ac/research-type'),
            'research_method': autocomplete.ModelSelect2Multiple(
                url='/vocabs-ac/specific-concept-ac/research-methods'),
            'research_question': autocomplete.ModelSelect2(
                url='archiv-ac:researchquestion-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(ResearchEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = "__all__"
        widgets = {
            'alt_name': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:altname-autocomplete'),
            'literature': autocomplete.ModelSelect2Multiple(
                url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
            'public', 'name', 'polygon', 'alt_id', 'alt_name',
            'cadastral_community', 'heritage_number', 'plot_number',
            'ownership', 'other_period', 'information_source',
            'description', 'comment', 'literature',
            # tourism field
            'accessibility', 'visibility', 'infrastructure', 'long_term_management',
            'potential_surrounding', 'museum', 'iad_app', 'app_description'
        ]
        widgets = {
            'alt_name': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:altname-autocomplete'),
            'literature': autocomplete.ModelSelect2Multiple(
                url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
            'cadastral_community': autocomplete.ModelSelect2Multiple(
                url='entities-ac:place-autocomplete'),
            'other_period': autocomplete.ModelSelect2Multiple(
                url='/vocabs-ac/specific-concept-ac/other-present-archaeological-period'),
            'information_source': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:researchevent-autocomplete'),
            'museum': autocomplete.ModelSelect2Multiple(
                url='entities-ac:institution-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AltNameForm(forms.ModelForm):
    class Meta:
        model = AltName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AltNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)
