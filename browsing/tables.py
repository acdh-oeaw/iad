import django_tables2 as tables
from django_tables2.utils import A
from entities.models import *
from archiv.models import *
from bib.models import *


class ReferenceTable(tables.Table):
    id = tables.LinkColumn(
        'bib:reference_detail',
        args=[A('pk')], verbose_name='ID'
    )

    class Meta:
        model = Reference
        sequence = ('id', 'zotero_item', 'page')
        attrs = {"class": "table table-responsive table-hover"}


class MonumentProtectionTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:monumentprotection_detail',
        args=[A('pk')], verbose_name='ID'
    )

    class Meta:
        model = MonumentProtection
        sequence = ('id', 'site_id')
        attrs = {"class": "table table-responsive table-hover"}


class ResearchQuestionTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:researchquestion_detail',
        args=[A('pk')], verbose_name='ID'
    )
    question = tables.LinkColumn(
        'archiv:researchquestion_detail',
        args=[A('pk')], verbose_name='Question'
    )

    class Meta:
        model = ResearchQuestion
        sequence = ('id', 'question')
        attrs = {"class": "table table-responsive table-hover"}


class ArchEntTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:archent_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'archiv:archent_detail',
        args=[A('pk')], verbose_name='Name'
    )
    comment = tables.TemplateColumn("{{ record.comment|truncatechars:250 }}")
    site_id = tables.Column()
    public = tables.Column()
    topography = tables.ManyToManyColumn()
    period = tables.ManyToManyColumn()

    class Meta:
        model = ArchEnt
        sequence = ('id', 'name', 'site_id', 'ent_type')
        attrs = {"class": "table table-responsive table-hover"}


class SiteTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:site_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'archiv:site_detail',
        args=[A('pk')], verbose_name='Name'
    )
    cadastral_community = tables.ManyToManyColumn()
    other_period = tables.ManyToManyColumn()
    country = tables.TemplateColumn(
        "{% for x in record.cadastral_community.all %}{{ x.ctcod }}|{% endfor %}",
        orderable=False
    )
    # ArchEnt-Cols
    arch_ent_type = tables.TemplateColumn(
        "{% for x in record.has_archent.all %}{{ x.ent_type }}|{% endfor %}",
        orderable=False
    )
    # ResearchEvent-Cols
    ra = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity"
    )
    ra_start = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.start_date }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity start date"
    )
    ra_end = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.end_date }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity end date"
    )
    ra_id = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.id }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Identifier"
    )
    ra_responsible_researcher = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{% for y in x.responsible_researcher.all %}{{ y }} # {% endfor %}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Researcher(s)"
    )
    ra_responsible_institution = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{% for y in x.responsible_institution.all %}{{ y }} # {% endfor %}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Institution(s)"
    )
    ra_type = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.research_type }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Type"
    )
    ra_research_method = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{% for y in x.research_method.all %}{{ y }} # {% endfor %}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Method(s)"
    )
    ra_research_question = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.research_question }}|{% endfor %}",
        orderable=False, verbose_name="Research Activity Question"
    )
    ra_generation_data_set = tables.TemplateColumn(
        "{% for x in record.has_research_activity.all %}{{ x.generation_data_set }}|{% endfor %}",
        orderable=False, verbose_name="When was the data-set generated?"
    )
    public = tables.Column()

    class Meta:
        model = Site
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}


class ResearchEventTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:researchevent_detail',
        args=[A('pk')], verbose_name='ID'
    )
    start_date = tables.DateColumn(format='Y-m-d')
    end_date = tables.DateColumn(format='Y-m-d')
    site_id = tables.ManyToManyColumn()
    responsible_researcher = tables.ManyToManyColumn()
    responsible_institution = tables.ManyToManyColumn()
    research_method = tables.ManyToManyColumn()

    class Meta:
        model = ResearchEvent
        sequence = ('id', 'start_date', 'end_date')
        attrs = {"class": "table table-responsive table-hover"}


class AltNameTable(tables.Table):
    label = tables.LinkColumn(
        'archiv:altname_detail',
        args=[A('pk')], verbose_name='Name'
    )
    language = tables.Column()

    class Meta:
        model = AltName
        sequence = ('label', 'language')
        attrs = {"class": "table table-responsive table-hover"}


class PeriodTable(tables.Table):
    id = tables.LinkColumn(
        'archiv:period_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'archiv:period_detail',
        args=[A('pk')], verbose_name='Name'
    )
    start_date = tables.Column()
    start_date_latest = tables.Column()
    end_date = tables.Column()
    end_date_latest = tables.Column()

    class Meta:
        model = Period
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}


class PersonTable(tables.Table):
    id = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='ID'
    )
    name = tables.LinkColumn(
        'entities:person_detail',
        args=[A('pk')], verbose_name='Name'
    )
    forename = tables.Column()

    class Meta:
        model = Person
        sequence = ('id', 'written_name',)
        attrs = {"class": "table table-responsive table-hover"}


class InstitutionTable(tables.Table):
    written_name = tables.LinkColumn(
        'entities:institution_detail',
        args=[A('pk')], verbose_name='Name'
    )
    location = tables.Column()

    class Meta:
        model = Institution
        sequence = ('id', 'written_name',)
        attrs = {"class": "table table-responsive table-hover"}


class PlaceTable(tables.Table):
    name = tables.LinkColumn(
        'entities:place_detail',
        args=[A('pk')], verbose_name='Name'
    )
    part_of = tables.Column()

    class Meta:
        model = Place
        sequence = ('id', 'name',)
        attrs = {"class": "table table-responsive table-hover"}


class AlternativeNameTable(tables.Table):
    name = tables.LinkColumn(
        'entities:alternativename_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = AlternativeName
        sequence = ('name',)
        attrs = {"class": "table table-responsive table-hover"}
