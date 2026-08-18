from django import template

from vocabs.models import SkosConcept

register = template.Library()


def calculate_potential(x):
    if x <= 8:
        status = "High"
    elif x <= 12:
        status = "Middle"
    else:
        status = "Low"
    return status


@register.simple_tag
def class_dict():
    classes = {
        "Site": "Site",
        "ResearchEvent": "Research Activity",
        "ArchEnt": "Archaeological Entity",
        "MonumentProtection": "Monument Protection",
    }
    return classes


@register.inclusion_tag("archiv/tags/archiv_colors.html", takes_context=True)
def archiv_colors(context):
    return context


@register.inclusion_tag("archiv/tags/archiv_custom_js.html", takes_context=True)
def archiv_custom_js(context):
    return context


@register.inclusion_tag("archiv/tags/skos_info.html")
def skos_info(concept):
    concepts = SkosConcept.objects.filter(pref_label=concept)
    return {"concepts": concepts}
