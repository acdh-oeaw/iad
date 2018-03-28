import django_tables2 as tables
from django_tables2.utils import A
from entities.models import *
from archiv.models import *


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
    qeustion = tables.LinkColumn(
        'archiv:researchquestion_detail',
        args=[A('pk')], verbose_name='Question'
    )

    class Meta:
        model = ResearchQuestion
        sequence = ('id', 'qeustion')
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
    site_id = tables.Column()
    public = tables.Column()

    class Meta:
        model = ArchEnt
        sequence = ('id', 'name', 'site_id')
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
    name = tables.LinkColumn(
        'archiv:researchevent_detail',
        args=[A('pk')], verbose_name='Name'
    )

    class Meta:
        model = ResearchEvent
        sequence = ('id', 'name',)
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
