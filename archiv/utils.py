import geojson
from django.contrib.gis.geos import GEOSGeometry


def geojson_to_poly(geo_json_str):
    """ tries to convert a geojson-string to a GEOSGeometry object """
    result = {}
    errors = []
    result['mpoly'] = None
    try:
        geo_json = geojson.loads(geo_json_str)
    except Exception as e:
        geo_json = None
        errors.append('Failed to read JSON because of: {}'.format(e))
    if geo_json:
        try:
            coords = geo_json['features'][0]['geometry']
        except Exception as e:
            coords = None
            errors.append(
                'Failed extract coordinates from Featurecollection because of: {}'.format(e)
            )
        if coords:
            try:
                result['mpoly'] = GEOSGeometry(geo_input=str(coords))
            except Exception as e:
                errors.append(
                    'Failed to transform coordinates to GEOSGeomentry because of: {}'.format(e)
                )
    result["errors"] = errors

    return result


SITE = [
    (('pk'), ('internal id')),
    (('identifier'), ('Identifier')),
    (('name'), ('Site Name')),
    (('alt_name'), ('Alternative Name')),
    (('alt_id'), ('Alt ID')),
    (('description'), ('Description')),
    (('comment'), ('Comment')),
    (('public'), ('Public')),
    (('literature__zotero_item__zoterokey'), ('Literatur')),
    (('cadastral_community__cadcom_nam'), ('Cadastral Community')),
    (('cadastral_number'), ('Cadastral Nummer')),
    (('heritage_number'), ('Heritage Number')),
    (('plot_number'), ('Plot Number')),
    (('ownership'), ('Ownership')),
    (('other_period__pref_label'), ('Other Period')),
    (('accessibility'), ('accessibility')),
    (('visibility'), ('visibility')),
    (('infrastructure'), ('infrastructure')),
    (('long_term_management'), ('long term management')),
    (('potential_surrounding'), ('potential surrounding')),
    (('museum__written_name'), ('Museum')),
    (('iad_app'), ('Iad App')),
    (('app_description'), ('App Description')),
    (('tourism_comment'), ('Tourism Comment')),
    (('site_checked_by__username'), ('Site checked by')),
]


ARCHENT = [
    (('pk'), ('internal id')),
    (('identifier'), ('Identifier')),
    (('name'), ('Site Name')),
    (('alt_name'), ('Alternative Name')),
    (('alt_id'), ('Alt ID')),
    (('description'), ('Description')),
    (('comment'), ('Comment')),
    (('public'), ('Public')),
    (('literature__zotero_item__zoterokey'), ('Literatur')),
    (('site_id__name'), ('Site')),
    (('ent_type__pref_label'), ('Entity Type')),
    (('burial_type__pref_label'), ('Burial Type')),
    (('settlement_fortification__pref_label'), ('Settlement Fortification')),
    (('settlement_occupation__pref_label'), ('Settlement Occupation')),
    (('topography__pref_label'), ('Topography')),
    (('type_certainty'), ('Entity Type Certainty')),
    (('dating_certainty'), ('Dating Certainty')),
    (('location_certainty'), ('Location Certainty')),
    (('period__name'), ('Dating')),
]


RESEARCHEVENT = [
    (('pk'), ('internal id')),
    (('identifier'), ('Identifier')),
    (('description'), ('Description')),
    (('comment'), ('Comment')),
    (('public'), ('Public')),
    (('literature__zotero_item__zoterokey'), ('Literatur')),
    (('site_id__name'), ('Site')),
    (('legacy_research_id'), ('legacy_research_id')),
    (('start_date'), ('Start Date')),
    (('end_date'), ('End Date')),
    (('responsible_researcher__name'), ('Responsible Researcher')),
    (('responsible_institution__written_name'), ('Responsible Institution')),
    (('research_type__pref_label'), ('Research Type')),
    (('research_method__pref_label'), ('Research Methods')),
    (('research_question__question'), ('Research Question')),
    (('generation_data_set'), ('When was the data-set generated?')),
]

MONUMENTPROTECTION = [
    (('pk'), ('internal id')),
    (('identifier'), ('Identifier')),
    (('description'), ('Description')),
    (('comment'), ('Comment')),
    (('public'), ('Public')),
    (('literature__zotero_item__zoterokey'), ('Literatur')),
    (('site_id__name'), ('Site')),
    (('current_land_use__pref_label'), ('Current Land Use')),
    (('heritage_status'), ('Cultural Heritage Status')),
    (('natural_heritage_status__pref_label'), ('Natural Heritage Status')),
    (('threats'), ('Threats')),
]
