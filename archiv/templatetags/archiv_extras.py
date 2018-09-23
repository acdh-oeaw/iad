from django import template

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
