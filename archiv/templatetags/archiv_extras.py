from django import template
from collections import Counter
from django.db.models import Q
from django.contrib.gis.db.models import Union
from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from archiv.models import Site, MonumentProtection, ResearchEvent

register = template.Library()


@register.simple_tag
def class_dict():
    classes = {
        'Site': 'Site',
        'ResearchEvent': 'Research Activity',
        'ArchEnt': 'Archaeological Entity',
        'MonumentProtection': 'Monument Protection',
    }
    return classes


@register.inclusion_tag('archiv/tags/archiv_colors.html', takes_context=True)
def archiv_colors(context):
    return context


@register.inclusion_tag('archiv/tags/archiv_custom_js.html', takes_context=True)
def archiv_custom_js(context):
    return context


@register.simple_tag
def sites_by_country():
    sites = Site.objects.all()
    result = dict(
        Counter(
            [x['cadastral_community__ctcod'] for x in list(
                sites.values('cadastral_community__ctcod')
            )]
        )
    )
    return result


@register.simple_tag
def site_count():
    return Site.objects.all().count()


@register.simple_tag
def protected_site_count():
    mps = MonumentProtection.objects.filter(
            Q(heritage_status='yes') | Q(heritage_status='partially')
        )
    sites = len(set([x.site_id for x in mps]))
    return sites


@register.simple_tag
def site_extent():
    u = Site.objects.filter(polygon__isvalid=True).aggregate(Union('polygon'))['polygon__union']
    u.transform(ct=3035)
    try:
        sq_m = "{:,.0f}".format(u.area/1000000)
    except Exception as e:
        sq_m = "{}".format(e)
    return sq_m


@register.simple_tag
def excavation_extent():
    excavation = SkosConcept.objects.filter(pref_label='excavation')
    u = generous_concept_filter(
        ResearchEvent.objects.filter(polygon__isvalid=True),
        'research_method', excavation
    ).aggregate(Union('polygon'))['polygon__union']
    u.transform(ct=3035)
    try:
        sq_m = "{:,.0f}".format(u.area/1000000)
    except Exception as e:
        sq_m = "{}".format(e)
    return sq_m


@register.simple_tag
def geophysical_extent():
    excavation = SkosConcept.objects.filter(pref_label='geophysical survey')
    u = generous_concept_filter(
        ResearchEvent.objects.filter(polygon__isvalid=True),
        'research_method', excavation
    ).aggregate(Union('polygon'))['polygon__union']
    u.transform(ct=3035)
    try:
        sq_m = "{:,.0f}".format(u.area/1000000)
    except Exception as e:
        sq_m = "{}".format(e)
    return sq_m


@register.inclusion_tag('archiv/tags/skos_info.html')
def skos_info(concept):
    concepts = SkosConcept.objects.filter(pref_label=concept)
    return {'concepts': concepts}
