from django import template
from collections import Counter

from archiv.models import Site

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
