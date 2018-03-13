from dal import autocomplete
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Period, AltName


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
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
