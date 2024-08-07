from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from crispy_forms.bootstrap import Accordion, AccordionGroup
from .models import Municipality


class MunicipalityFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(MunicipalityFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = "genericFilterForm"
        self.form_method = "GET"
        self.helper.form_tag = False
        self.add_input(Submit("Filter", "Search"))
        self.layout = Layout(
            Fieldset("Basic search options", "lau2nam", css_id="basic_search_fields"),
            Accordion(
                AccordionGroup(
                    "Advanced search", "nuts3nam", "ctnam", "lau2_id", css_id="more"
                ),
            ),
        )


class MunicipalityForm(forms.ModelForm):
    class Meta:
        model = Municipality
        exclude = [
            "geom",
        ]

    def __init__(self, *args, **kwargs):
        super(MunicipalityForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )
