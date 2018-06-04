from django import forms
from dal import autocomplete
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from . models import CadastralCommunity


class CadastralCommunityFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(CadastralCommunityFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'cadcom_nam',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Advanced search',
                    'nuts3_name',
                    'nuts2_name',
                    css_id="more"
                    ),
                )
            )


class CadastralCommunityForm(forms.ModelForm):
    class Meta:
        model = CadastralCommunity
        exclude = [
            'geom',
        ]

    def __init__(self, *args, **kwargs):
        super(CadastralCommunityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)
