from dal import autocomplete
from django import forms
from .models import ResearchEvent
from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, MultiField, HTML

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
        self.helper.add_input(Submit('submit', 'save'),)
        self.helper.layout = Layout(
            Div(
                'public',
                css_class="col-md-9"
                ),
            Div(
                'polygon',
                css_class="col-md-12"
                ),
            Div(
                'current_land_use',
                'heritage_status',
                'threats',
                'comment',
                css_class="col-md-9"
                )
            )


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
            'ent_type', 'topography', 'period', 'type_certainty',
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
            'period': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:period-autocomplete'),
            }

    def __init__(self, *args, **kwargs):
        super(ArchEntForm, self).__init__(*args, **kwargs)
        self.fields['ent_type'].required = True
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'save'),)
        self.helper.layout = Layout(
            Div(
                'public',
                css_class="col-md-9"
                ),
            Div(
                'polygon',
                css_class="col-md-12"
                ),
            Div(
                'site_id',
                'name',
                'alt_name',
                'ent_type',
                'topography',
                'period',
                'type_certainty',
                'dating_certainty',
                'location_certainty',
                'comment',
                css_class="col-md-9"
                )
            )


class ResearchEventForm(forms.ModelForm):
    class Meta:
        model = ResearchEvent
        fields = [
            'public', 'polygon', 'site_id', 'research_type',
            'research_method', 'start_date', 'end_date',
            'identifier', 'responsible_researcher', 'responsible_institution',
            'research_question', 'comment', 'generation_data_set'
        ]
        widgets = {
            'site_id': autocomplete.ModelSelect2Multiple(
                url='archiv-ac:site-autocomplete'),
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
        self.helper.add_input(Submit('submit', 'save'),)
        self.helper.layout = Layout(
            Div(
                'public',
                css_class="col-md-9"
                ),
            Div(
                'polygon',
                css_class="col-md-12"
                ),
            Div(
                'site_id',
                'research_type',
                'research_method',
                'start_date',
                'end_date',
                'identifier',
                'responsible_researcher',
                'responsible_institution',
                'research_question',
                'comment',
                'generation_data_set',
                css_class="col-md-9"
                )
            )


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = [
            'name', 'country', 'region', 'polygon',
            'start_date', 'start_date_latest', 'end_date',
            'end_date_latest', 'norm_id',
            'bibl', 'comment'
        ]
        widgets = {
            # 'alt_name': autocomplete.ModelSelect2Multiple(
            #     url='archiv-ac:altname-autocomplete'),
            # 'literature': autocomplete.ModelSelect2Multiple(
            #     url='bib-ac:reference-autocomplete'),
            'polygon': LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('submit', 'save'),)
        self.helper.layout = Layout(
            Div(
                'name',
                'country',
                'region',
                css_class="col-md-9"
                ),
            Div(
                'polygon',
                css_class="col-md-12"
                ),
            Div(
                'start_date',
                'start_date_latest',
                'end_date',
                'end_date_latest',
                'norm_id',
                'bibl',
                'comment',
                css_class="col-md-9"
                )
            )


class SiteForm(forms.ModelForm):
    OPTIONS = [(x.id, x) for x in ResearchEvent.objects.all()]

    research_activities = forms.MultipleChoiceField(
        choices=OPTIONS, required=False, widget=autocomplete.Select2Multiple(
            url='archiv-ac:researchevent-autocomplete'),
        label="Information Source",
        help_text="How was the site discovered? Choose the corresponding research event."
    )

    class Meta:
        model = Site
        fields = [
            'public', 'name', 'polygon', 'alt_id', 'alt_name',
            'cadastral_community', 'heritage_number', 'plot_number',
            'ownership', 'other_period', 'description', 'comment', 'literature',
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
            'museum': autocomplete.ModelSelect2Multiple(
                url='entities-ac:institution-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        try:
            instance = kwargs['instance']
            init_data = [x.id for x in ResearchEvent.objects.filter(site_id=instance.id)]
            self.fields['research_activities'].initial = init_data
        except AttributeError:
            pass
        self.fields['name'].required = True
        self.helper.form_tag = True
        self.helper.form_class = 'form-group'
        self.helper.add_input(Submit('submit', 'save'),)
        self.helper.layout = Layout(
            Fieldset(
                'Site description',
                Div(
                    'public',
                    'name',
                    css_class="col-md-9"
                ),
                Div(
                    'polygon',
                    css_class="col-md-12"
                    ),
                Div(
                    'alt_id',
                    'alt_name',
                    'cadastral_community',
                    'heritage_number',
                    'plot_number',
                    'ownership',
                    'other_period',
                    'information_source',
                    'description',
                    'comment',
                    'literature',
                    css_class="col-md-9"
                    ),
                css_class="separate-panel",
            ),
            Fieldset(
                'Tourism',
                Div(
                    'accessibility',
                    'visibility',
                    'infrastructure',
                    'long_term_management',
                    'potential_surrounding',
                    'museum',
                    'iad_app',
                    'app_description',
                    css_class="col-md-9"
                ),
                css_class="separate-panel",
            )
        )

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, True)
        try:
            res_acts = [int(x) for x in self.cleaned_data['research_activities']]
        except:
            res_acts = None
        if res_acts:
            res_obj = [x for x in ResearchEvent.objects.filter(pk__in=res_acts)]
            instance.has_research_activity.set(res_obj)
        return super(SiteForm, self).save(commit=commit)


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
