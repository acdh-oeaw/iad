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
