import pandas as pd
from django import template
from collections import Counter
from django.db.models import Q
from django.contrib.gis.db.models import Union
from vocabs.models import SkosConcept
from vocabs.filters import generous_concept_filter
from archiv.models import Site, MonumentProtection, ResearchEvent

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


@register.simple_tag
def sites_by_country():
    sites = Site.objects.all()
    values = sites.distinct().values("cadastral_community__ctcod")
    result = dict(Counter([x["cadastral_community__ctcod"] for x in list(values)]))
    try:
        result["None"] = result.pop(None)
    except KeyError:
        pass
    return result


@register.simple_tag
def site_count():
    return Site.objects.all().count()


@register.simple_tag
def protected_site_count():
    mps = MonumentProtection.objects.filter(
        Q(heritage_status="yes") | Q(heritage_status="partially")
    )
    sites = len(set([x.site_id for x in mps]))
    return sites


@register.simple_tag
def site_extent():
    u = Site.objects.filter(polygon__isvalid=True).aggregate(Union("polygon"))[
        "polygon__union"
    ]
    try:
        u.transform(ct=3035)
    except Exception as e:
        print(e)
        u = None
    if u:
        try:
            sq_m = "{:,.0f}".format(u.area / 1000000)
        except Exception as e:
            sq_m = "{}".format(e)
        return sq_m
    else:
        return "{} there is currently something going wrong"


@register.simple_tag
def excavation_extent():
    excavation = SkosConcept.objects.filter(pref_label="excavation")
    u_all = generous_concept_filter(
        ResearchEvent.objects.filter(polygon__isvalid=True),
        "research_method",
        excavation,
    )
    invalid_polies = []
    for x in u_all:
        try:
            x.polygon.transform(ct=3035)
        except Exception as e:
            print(x.id, e)
            invalid_polies.append(x.id)
    u = u_all.exclude(id__in=invalid_polies).aggregate(Union("polygon"))[
        "polygon__union"
    ]
    try:
        u.transform(ct=3035)
    except Exception as e:
        print(e)
        u = None
    if u:
        try:
            sq_m = "{:,.0f}".format(u.area / 1000000)
        except Exception as e:
            sq_m = "{}".format(e)
        return sq_m
    else:
        return "{} there is currently something going wrong"


@register.simple_tag
def geophysical_extent():
    excavation = SkosConcept.objects.filter(pref_label="geophysical survey")
    u = generous_concept_filter(
        ResearchEvent.objects.filter(polygon__isvalid=True),
        "research_method",
        excavation,
    ).aggregate(Union("polygon"))["polygon__union"]
    try:
        u.transform(ct=3035)
    except Exception as e:
        print(e)
        u = None
    if u:
        try:
            sq_m = "{:,.0f}".format(u.area / 1000000)
        except Exception as e:
            sq_m = "{}".format(e)
        return sq_m
    else:
        return "there is currently something going wrong"


@register.simple_tag
def touristic_potential():
    potential = [
        "accessibility",
        "visibility",
        "infrastructure",
        "long_term_management",
    ]
    df = (
        pd.DataFrame(list(Site.objects.all().values_list(*potential)))
        .fillna(4)
        .applymap(lambda x: int((str(x)[0])))
    )
    df["sum"] = df.sum(axis=1)
    df["status"] = df.apply(lambda x: calculate_potential(x["sum"]), axis=1)
    result = pd.DataFrame(df.groupby("status").count()[0])
    data = {}
    for i, row in result.iterrows():
        data[i] = row[0]
    return data


@register.inclusion_tag("archiv/tags/skos_info.html")
def skos_info(concept):
    concepts = SkosConcept.objects.filter(pref_label=concept)
    return {"concepts": concepts}
