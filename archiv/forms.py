from dal import autocomplete
from django import forms
from django.contrib.gis.geos import GEOSGeometry

from leaflet.forms.widgets import LeafletWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div

from .models import (
    MonumentProtection,
    ResearchEvent,
    ResearchQuestion,
    ArchEnt,
    Period,
    Site,
    AltName,
)
from .utils import geojson_to_poly, copy_shape_str_to_poly


class ArchivBaseForm(forms.ModelForm):
    paste_geojson = forms.CharField(
        widget=forms.Textarea,
        label="Paste a valid(!) GeoJson in this form",
        help_text="GeoJson must be of type 'FeatureCollection'\
        with features of type 'MultiPolygon'.",
        required=False,
    )
    paste_wkt = forms.CharField(
        widget=forms.Textarea,
        label="Paste a valid(!) WKT(Mulitpolygon) in this form",
        help_text="WKT must have srid=4326",
        required=False,
    )
    shape_string_epsg = forms.CharField(
        label="The shapes EPSG Number",
        help_text="The EPSG number form the polygon you copied, e.g.: '32633'",
        required=False,
    )
    shape_string = forms.CharField(
        widget=forms.Textarea,
        label="Paste the Polygon",
        help_text="Select the feature, hit 'strg+c' to copy it\
        an paste the content into this field",
        required=False,
    )
    delete_polygon = forms.BooleanField(
        required=False,
        initial=False,
        label="Delete existing Polygon?",
        help_text="Would you like to delete any existing Polygon?",
    )

    def clean(self):
        cleaned_data = super(ArchivBaseForm, self).clean()
        print("HALLO FROM OVERRIDEN CLEAN METHOD")
        geo_json_str = cleaned_data["paste_geojson"]
        paste_wkt = self.cleaned_data["paste_wkt"]
        shape_string_epsg = self.cleaned_data["shape_string_epsg"]
        shape_string = self.cleaned_data["shape_string"]
        if geo_json_str:
            processed_geojson = geojson_to_poly(geo_json_str)
            if processed_geojson["errors"]:
                self._errors["paste_geojson"] = self.error_class(
                    processed_geojson["errors"]
                )
        elif paste_wkt:
            try:
                GEOSGeometry(paste_wkt, srid=4326)
            except Exception as e:
                self._errors["paste_wkt"] = self.error_class(["{}".format(e)])
        elif shape_string_epsg and shape_string:
            data = copy_shape_str_to_poly(shape_string, shape_string_epsg)
            if data["errors"]:
                self._errors["shape_string"] = data["errors"]
        return cleaned_data

    def save(self, commit=True):
        instance = super(ArchivBaseForm, self).save(commit=True)
        print("HI from SAVE METHOD")
        geo_json_str = self.cleaned_data["paste_geojson"]
        paste_wkt = self.cleaned_data["paste_wkt"]
        paste_wkt = self.cleaned_data["paste_wkt"]
        shape_string_epsg = self.cleaned_data["shape_string_epsg"]
        shape_string = self.cleaned_data["shape_string"]
        if geo_json_str:
            processed_geojson = geojson_to_poly(geo_json_str)
            instance.polygon = processed_geojson["mpoly"]
            instance.save()
        elif paste_wkt:
            instance.polygon = GEOSGeometry(paste_wkt, srid=4326)
            "PASTE_WKT"
            instance.save()
        elif shape_string and shape_string_epsg:
            polygon = copy_shape_str_to_poly(shape_string, shape_string_epsg)["geom"]
            instance.polygon = polygon
            instance.save()
        if self.cleaned_data["delete_polygon"]:
            instance.polygon = None
            instance.save()
        return instance


class MonumentProtectionForm(ArchivBaseForm):

    class Meta:
        model = MonumentProtection
        fields = [
            "site_id",
            "public",
            "polygon",
            "current_land_use",
            "heritage_status",
            "natural_heritage_status",
            "threats",
            "comment",
        ]
        widgets = {
            "alt_name": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:altname-autocomplete"
            ),
            "literature": autocomplete.ModelSelect2Multiple(
                url="bib-ac:reference-autocomplete"
            ),
            "polygon": LeafletWidget(),
            "site_id": autocomplete.ModelSelect2(url="archiv-ac:site-autocomplete"),
            "current_land_use": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/current-land-use"
            ),
            "threats": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/threats"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MonumentProtectionForm, self).__init__(*args, **kwargs)
        self.fields["site_id"].required = True
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(
            Submit("submit", "save"),
        )
        self.helper.layout = Layout(
            Div("public", css_class="col-md-9"),
            Div("polygon", css_class="col-md-12"),
            Div(
                "site_id",
                "current_land_use",
                "heritage_status",
                "natural_heritage_status",
                "threats",
                "comment",
                css_class="col-md-9",
            ),
            Fieldset(
                "Import/Delete Spatial Data",
                Div(
                    "paste_geojson",
                    "paste_wkt",
                    "shape_string_epsg",
                    "shape_string",
                    "delete_polygon",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
        )


class ResearchQuestionForm(ArchivBaseForm):
    class Meta:
        model = ResearchQuestion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ResearchQuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )


class ArchEntForm(ArchivBaseForm):
    class Meta:
        model = ArchEnt
        fields = [
            "public",
            "polygon",
            "site_id",
            "name",
            "alt_name",
            "ent_type",
            "burial_type",
            "burial_construction",
            "settlement_fortification",
            "settlement_occupation",
            "topography",
            "period",
            "type_certainty",
            "dating_certainty",
            "location_certainty",
            "comment",
        ]
        widgets = {
            "alt_name": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:altname-autocomplete"
            ),
            "literature": autocomplete.ModelSelect2Multiple(
                url="bib-ac:reference-autocomplete"
            ),
            "polygon": LeafletWidget(),
            "site_id": autocomplete.ModelSelect2(url="archiv-ac:site-autocomplete"),
            "ent_type": autocomplete.ModelSelect2(
                url="/vocabs-ac/specific-concept-ac/archaeological-entity-type"
            ),
            "burial_type": autocomplete.ModelSelect2(
                url="/vocabs-ac/specific-concept-ac/burial-type"
            ),
            "burial_construction": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/burial-construction"
            ),
            "settlement_fortification": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/settlement-fortification"
            ),
            "settlement_occupation": autocomplete.ModelSelect2(
                url="/vocabs-ac/specific-concept-ac/settlement-occupation"
            ),
            "topography": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/topography"
            ),
            "period": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:period-autocomplete"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ArchEntForm, self).__init__(*args, **kwargs)
        self.fields["site_id"].required = True
        self.fields["ent_type"].required = True
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(
            Submit("submit", "save"),
        )
        self.helper.layout = Layout(
            Div("public", css_class="col-md-9"),
            Div("polygon", css_class="col-md-12"),
            Div(
                "site_id",
                "name",
                "alt_name",
                "ent_type",
                Div(
                    "burial_type",
                    "burial_construction",
                    css_class="hidden_burial",
                ),
                Div(
                    "settlement_fortification",
                    css_class="hidden_settlement",
                ),
                Div(
                    "settlement_occupation",
                    css_class="hidden_settlement",
                ),
                "topography",
                "period",
                "type_certainty",
                "dating_certainty",
                "location_certainty",
                "comment",
                css_class="col-md-9",
            ),
            Fieldset(
                "Import/Delete Spatial Data",
                Div(
                    "paste_geojson",
                    "paste_wkt",
                    "shape_string_epsg",
                    "shape_string",
                    "delete_polygon",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
        )


class ResearchEventForm(ArchivBaseForm):

    class Meta:
        model = ResearchEvent
        fields = [
            "public",
            "polygon",
            "site_id",
            "research_type",
            "research_method",
            "start_date",
            "end_date",
            "identifier",
            "responsible_researcher",
            "responsible_institution",
            "research_question",
            "comment",
            "generation_data_set",
            "polygon_proxy",
        ]
        widgets = {
            "site_id": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:site-autocomplete"
            ),
            "alt_name": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:altname-autocomplete"
            ),
            "literature": autocomplete.ModelSelect2Multiple(
                url="bib-ac:reference-autocomplete"
            ),
            "polygon": LeafletWidget(),
            "responsible_researcher": autocomplete.ModelSelect2Multiple(
                url="entities-ac:person-autocomplete"
            ),
            "responsible_institution": autocomplete.ModelSelect2Multiple(
                url="entities-ac:institution-autocomplete"
            ),
            "research_type": autocomplete.ModelSelect2(
                url="/vocabs-ac/specific-concept-ac/research-type"
            ),
            "research_method": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/research-methods"
            ),
            "start_date": forms.DateInput(
                attrs={"placeholder": "YYYY-MM-DD"}, format=("%Y-%m-%d")
            ),
            "end_date": forms.DateInput(
                attrs={"placeholder": "YYYY-MM-DD"}, format=("%Y-%m-%d")
            ),
            "research_question": autocomplete.ModelSelect2(
                url="archiv-ac:researchquestion-autocomplete"
            ),
            "generation_data_set": forms.DateInput(
                attrs={"placeholder": "YYYY-MM-DD"}, format=("%Y-%m-%d")
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ResearchEventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["start_date"].required = True
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(
            Submit("submit", "save"),
        )
        self.helper.layout = Layout(
            Div("public", css_class="col-md-9"),
            Div("polygon", css_class="col-md-12"),
            Div(
                "site_id",
                "research_type",
                "research_method",
                "start_date",
                "end_date",
                "identifier",
                "responsible_researcher",
                "responsible_institution",
                "research_question",
                "comment",
                "generation_data_set",
                css_class="col-md-9",
            ),
            Fieldset(
                "Import/Delete Spatial Data",
                Div(
                    "paste_geojson",
                    "paste_wkt",
                    "shape_string_epsg",
                    "shape_string",
                    "delete_polygon",
                    "polygon_proxy",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
        )


class PeriodForm(ArchivBaseForm):
    class Meta:
        model = Period
        fields = [
            "name",
            "country",
            "region",
            "polygon",
            "start_date",
            "start_date_latest",
            "end_date",
            "end_date_latest",
            "norm_id",
            "bibl",
            "comment",
        ]
        widgets = {
            "polygon": LeafletWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.add_input(
            Submit("submit", "save"),
        )
        self.helper.layout = Layout(
            Div("name", "country", "region", css_class="col-md-9"),
            Div("polygon", css_class="col-md-12"),
            Div(
                "start_date",
                "start_date_latest",
                "end_date",
                "end_date_latest",
                "norm_id",
                "bibl",
                "comment",
                "paste_geojson",
                "paste_wkt",
                "shape_string_epsg",
                "shape_string",
                "delete_polygon",
                css_class="col-md-9",
            ),
        )


class SiteForm(ArchivBaseForm):

    class Meta:
        model = Site
        fields = [
            "public",
            "name",
            "cadastral_community",
            "polygon",
            "alt_id",
            "alt_name",
            "sm_adm",
            "heritage_number",
            "plot_number",
            "ownership",
            "other_period",
            "description",
            "comment",
            "literature",
            # tourism field
            "accessibility",
            "visibility",
            "infrastructure",
            "long_term_management",
            "potential_surrounding",
            "museum",
            "iad_app",
            "app_description",
            "tourism_comment",
            "site_checked_by",
            "polygon_proxy",
        ]
        widgets = {
            "sm_adm": forms.TextInput(),
            "alt_name": autocomplete.ModelSelect2Multiple(
                url="archiv-ac:altname-autocomplete"
            ),
            "literature": autocomplete.ModelSelect2Multiple(
                url="bib-ac:reference-autocomplete"
            ),
            "polygon": LeafletWidget(),
            "cadastral_community": autocomplete.ModelSelect2Multiple(
                url="shapes-ac:municipality-autocomplete"
            ),
            "other_period": autocomplete.ModelSelect2Multiple(
                url="/vocabs-ac/specific-concept-ac/other-present-archaeological-period"
            ),
            "museum": autocomplete.ModelSelect2Multiple(
                url="entities-ac:institution-autocomplete"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["name"].required = True
        self.fields["public"].required = False
        self.fields["polygon_proxy"].required = False
        self.helper.form_tag = True
        self.helper.form_class = "form-group"
        self.helper.add_input(
            Submit("submit", "save"),
        )
        self.helper.layout = Layout(
            Fieldset(
                "Site description",
                Div("public", "name", "cadastral_community", css_class="col-md-9"),
                Div("polygon", css_class="col-md-12"),
                Div(
                    "alt_id",
                    "alt_name",
                    "sm_adm",
                    "heritage_number",
                    "plot_number",
                    "ownership",
                    "other_period",
                    "research_activities",
                    "description",
                    "comment",
                    "literature",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
            Fieldset(
                "Tourism",
                Div(
                    "accessibility",
                    "visibility",
                    "infrastructure",
                    "long_term_management",
                    "potential_surrounding",
                    "museum",
                    "iad_app",
                    "app_description",
                    "tourism_comment",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
            Fieldset(
                "Import/Delete Spatial Data",
                Div(
                    "paste_geojson",
                    "paste_wkt",
                    "shape_string_epsg",
                    "shape_string",
                    "delete_polygon",
                    "polygon_proxy",
                    css_class="col-md-9",
                ),
                css_class="separate-panel",
            ),
            Fieldset(
                "Quality Control",
                Div("site_checked_by", css_class="col-md-9"),
                css_class="separate-panel",
            ),
        )


class AltNameForm(forms.ModelForm):
    class Meta:
        model = AltName
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AltNameForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3"
        self.helper.field_class = "col-md-9"
        self.helper.add_input(
            Submit("submit", "save"),
        )
