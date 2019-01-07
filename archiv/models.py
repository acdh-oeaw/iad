import reversion
import json

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Union
from django.contrib.gis.db.models.functions import Centroid
from django.contrib.gis import geos
from django.core.serializers import serialize

from idprovider.models import IdProvider
from entities.models import Place, Person, Institution
from vocabs.models import SkosConcept
from bib.models import Reference
from shapes.models import Municipality


def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap


VALUE_STATUS_CHOICES = (
    ('1 - high', '1 - high'),
    ('2 - middle', '2 - middle'),
    ('3 - low', '3 - low'),
)

BOOLEAN_CHOICES = (
    (True, "Yes"),
    (False, "No")
)


@reversion.register()
class AltName(IdProvider):
    label = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="A name tag")
    language = models.CharField(
        blank=True, null=True, max_length=3,
        verbose_name="ISO639")

    def __str__(self):
        if self.language:
            return "{} ({})".format(self.label, self.language)
        else:
            return "{}".format(self.label)

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_archivaltnames')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:altname_create')

    def get_next(self):
        next = AltName.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = AltName.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:altname_detail', kwargs={'pk': self.id}
        )


class IadBaseClass(IdProvider):

    """A class for shared properties"""

    identifier = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="Identifier"
    )
    name = models.CharField(
        blank=True, null=True, max_length=250, verbose_name="The objects name"
    )
    alt_name = models.ManyToManyField(
        AltName, blank=True, verbose_name="Alternative Name",
        help_text="Another name of the site (another spelling, language, alias name etc.)."
    )
    alt_id = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Alternative ID",
        help_text="Any other official identifier of this entity."
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="Description of the object."
    )
    comment = models.TextField(
        blank=True, null=True,
        help_text="""Any noteworthy general information about the object
        that cannot be expressed in other fields.""",
        verbose_name="Comment"
    )
    public = models.BooleanField(
        default=False, verbose_name="Public",
        choices=BOOLEAN_CHOICES,
        help_text="Should this entry (and all related entries) be public\
        or only visible to the account holders? Can be made public\
        only after data-check was completed."
    )
    literature = models.ManyToManyField(
        Reference, blank=True, verbose_name="Literature",
        help_text="Add publication references"
    )
    polygon = models.MultiPolygonField(blank=True, null=True)
    polygon_proxy = models.BooleanField(
        default=False, verbose_name="No precise polygon",
        choices=BOOLEAN_CHOICES,
        help_text="Please set to 'Yes' in case the polygon is merely a place holder"
    )
    centroid = models.PointField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.polygon and not self.centroid:
            cent = self.polygon.centroid
            self.centroid = cent
        super().save(*args, **kwargs)

    @classmethod
    def get_points(self):
        model_name = self.__name__
        ct = ContentType.objects.get(
            app_label='archiv',
            model=model_name.lower()
        ).model_class()
        geojson = serialize(
            'geojson',
            ct.objects.all(),
            geometry_field='centroid',
            fields=(
                'name',
                'pk',
            )
        )
        return geojson

    @classmethod
    def get_shapes(self):
        model_name = self.__name__
        ct = ContentType.objects.get(
            app_label='archiv',
            model=model_name.lower()
        ).model_class()
        geojson = serialize(
            'geojson',
            ct.objects.all(),
            geometry_field='polygon',
            fields=(
                'name',
                'pk',
            )
        )
        return geojson

    @classmethod
    def get_convex_hull(self):
        if Site.objects.exclude(polygon=None):
            sites = [x.id for x in Site.objects.exclude(polygon=None) if x.polygon.valid]
            valid_sites = Site.objects.filter(id__in=sites)
            geojson = json.loads(
                    valid_sites.exclude(polygon=None)
                    .aggregate(combined=Union('polygon'))['combined']
                    .convex_hull.geojson
                )
            geojson['properties'] = {
                'name': "Convex hull of all {} objects".format(self.__name__)
            }
            geojson = json.dumps(geojson)
            return geojson
        else:
            None

    def copy_instance(self):
        """Saves a copy of the current object and returns it"""
        obj = self
        obj.id = None
        obj.pk = None
        old_name = "{}".format(self.name)
        if old_name:
            obj.name = "COPY OF {}".format(old_name)
        else:
            obj.name = "COPY of some other Object"
        obj.save()
        return obj

    class Meta:
        abstract = True


@modify_fields(
    name={
        'verbose_name': 'Period name',
        'help_text': 'The name of the period (e.g. Iron Age, Early Iron Age, Hallstatt A…).'
        }
        )
@reversion.register()
class Period(IadBaseClass):

    """ Please provide a definition of this class """

    start_date = models.IntegerField(
        blank=True, null=True,
        verbose_name="Earliest beginning of the period (BC).",
        help_text="Must be a number!"
    )
    start_date_latest = models.IntegerField(
        blank=True, null=True,
        verbose_name="Latest beginning of the period (BC).",
        help_text="Must be a number!"
    )
    end_date = models.IntegerField(
        blank=True, null=True,
        verbose_name="Earliest end of the period (BC).",
        help_text="Must be a number!"
    )
    end_date_latest = models.IntegerField(
        blank=True, null=True,
        verbose_name="Latest end of the period (BC).",
        help_text="Must be a number!"
    )
    norm_id = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Link to some norm data record like 'http://perio.do/'"
    )
    region = models.ManyToManyField(
        Place, blank=True, related_name="has_related_period_region",
        verbose_name="Region in which this period is used in.",
        help_text="Region in which this period is used in."
    )
    country = models.ForeignKey(
        Place, blank=True, null=True, related_name="has_related_period_country",
        verbose_name="Country in which this period is used in.",
        help_text="Country in which this period is used in.",
        on_delete=models.SET_NULL
    )
    bibl = models.TextField(
        blank=True, null=True, verbose_name="Bibliographic source for this period."
    )

    class Meta:
        ordering = ['pk']
        verbose_name = "Chronology"

    def get_geojson(self):
        geojson = serialize(
            'geojson', Period.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'identifier',)
        )
        return geojson

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_periods')

    # @classmethod
    # def get_createview_url(self):
    #     return reverse('archiv:period_create')

    def get_next(self):
        next = Period.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Period.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:period_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        return "{}".format(self.name)


SITE_OWNERSHIP = (
    ('1 – private', '1 – private'),
    ('2 – public', '2 – public'),
    ('3 – private/public', '3 – private/public'),
    ('4 – information not available', '4 – information not available'),
)

SITE_ACCESSIBILITY = (
    ('1 – accessible by public transport', '1 – accessible by public transport'),
    (
        '2 – accessible for individual tourist groups',
        '2 – accessible for individual tourist groups'
    ),
    ('3 – inaccessible', '3 – inaccessible '),
    ('4 – information not available', '4 – information not available'),
)

SITE_VISIBILITY = (
    (
        '1 – reconstructed and interpreted onsite',
        '1 – reconstructed and interpreted onsite'
    ),
    ('2 – visible, but not interpreted', '2 – visible, but not interpreted'),
    ('3 - invisible archaeological heritage', '3 - invisible archaeological heritage'),
    ('4 – information not available', '4 – information not available'),
)


SITE_INFRASTRUCTURE = (
    ('1 – complete infrastructure', '1 – complete infrastructure'),
    ('2 – basic infrastructure', '2 – basic infrastructure'),
    ('3 – no infrastructure', '3 – no infrastructure'),
    ('4 – information not available', '4 – information not available'),
)

SITE_LONGTERMMANGEMENT = (
    ('1 – long-term care ensured', '1 – long-term care ensured'),
    ('2 – short-term care ensured', '2 – short-term care ensured'),
    ('3 – no care foreseen or possible', '3 – no care foreseen or possible'),
    ('4 – information not available', '4 – information not available'),
)

SITE_POTENTIALSURROUNDINGS = (
    (
        '1 – touristic region with excellent infrastructure',
        '1 – touristic region with excellent infrastructure'
    ),
    (
        '2 – touristic offer in development',
        '2 – touristic offer in development'
    ),
    (
        '3 – no or little attempts for tourism',
        '3 – no or little attempts for tourism'
    ),
    ('4 – information not available', '4 – information not available'),
)


@modify_fields(
    name={
        'verbose_name': 'Site Name',
        'help_text': 'The name of the site in the language of\
        the country where the site is located.'
        },
    description={
        'verbose_name': 'Description',
        'help_text': 'Description of the whole site.'
    })
@reversion.register()
class Site(IadBaseClass):
    """SITE is the highest class in the database and includes mostly geographical and
    administrative information about the area where past human activity has been recognized.
    It is defined by a spatial polygon"""

    cadastral_community = models.ManyToManyField(
        Municipality, blank=True, verbose_name="Municipality",
        help_text="The municipality where the site is located.",
        related_name="has_sites"
    )
    sm_adm = models.TextField(
        blank=True, verbose_name="Smallest Administrative Unit",
        help_text="Smallest Administrative Unit."
    )
    cadastral_number = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Cadastral Number (will be moved to Place-Class)",
        help_text="The cadastral number."
    )
    heritage_number = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Heritage Register Number",
        help_text="The heritage register number."
    )
    plot_number = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Plot Number",
        help_text="The plot number (applies to Slovenian sites)."
    )
    ownership = models.CharField(
        blank=True, null=True, verbose_name="Ownership",
        help_text="Ownership of the land, where the site is located.",
        max_length=250,
        choices=SITE_OWNERSHIP
    )
    other_period = models.ManyToManyField(
        SkosConcept, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site.",
        related_name="has_other_period"
    )
    accessibility = models.CharField(
        blank=True, null=True, verbose_name="Accessibility",
        help_text="Transportation types available on the site.",
        max_length=250,
        choices=SITE_ACCESSIBILITY
    )
    visibility = models.CharField(
        blank=True, null=True, verbose_name="Visibility",
        help_text="How visible are the remains on site.",
        max_length=250,
        choices=SITE_VISIBILITY
    )
    infrastructure = models.CharField(
        blank=True, null=True, verbose_name="Infrastructure",
        help_text="What kind of infrastructure is available in the vicinity of the site\
        (restaurants, parking, etc.)",
        max_length=250,
        choices=SITE_INFRASTRUCTURE
    )
    long_term_management = models.CharField(
        blank=True, null=True, verbose_name="Long-Term Management",
        help_text="What kind of management of the site is foreseen?",
        max_length=250,
        choices=SITE_LONGTERMMANGEMENT
    )
    potential_surrounding = models.CharField(
        blank=True, null=True, verbose_name="Potential of the Surroundings",
        help_text="How well is the region where the site is located visited by tourists?\
        What is the potential of other touristic attractions in the vicinity?",
        max_length=250,
        choices=SITE_POTENTIALSURROUNDINGS
    )
    museum = models.ManyToManyField(
        Institution, blank=True, verbose_name="Museum",
        help_text="Where are the finds from the site stored?",
        related_name="is_museum"
    )
    iad_app = models.BooleanField(
        verbose_name="App",
        default=False, choices=BOOLEAN_CHOICES,
        help_text="Should this site be used in the IAD-App?"
    )
    app_description = models.TextField(
        blank=True, null=True, verbose_name="App Description",
        help_text="If the site is going to be used in the IAD app, please provide the \
        description of the site to be implemented into the app."
    )
    tourism_comment = models.TextField(
        blank=True, null=True,
        help_text="Any noteworthy information about the touristic potential of the site that \
        has not been expressed in other fields.",
        verbose_name="Comment"
    )
    site_checked_by = models.ForeignKey(
        User, blank=True, null=True, related_name="site_checked_by_user",
        verbose_name="Checked by",
        help_text="Who and when checked the entered data (The 'when' is stored automatically).",
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['pk']
        verbose_name = "Site"

    def get_geojson(self):
        geojson = serialize(
            'geojson', Site.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'identifier', 'pk')
        )
        return geojson

    def get_point(self):
        if self.centroid:
            geojson = serialize(
                'geojson', Site.objects.filter(id=self.id),
                geometry_field='centroid',
                fields=('name', 'identifier', 'pk')
            )
        else:
            geojson = None
        return geojson

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_sites')

    @classmethod
    def get_dl_url(self):
        return reverse('browsing:dl_sites')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:site_create')

    def convex_hull_archents(self):
        if self.has_archent.exclude(polygon=None):
            try:
                geojson = json.loads(
                    self.has_archent.exclude(polygon=None)
                    .aggregate(combined=Union('polygon'))['combined']
                    .convex_hull.geojson
                )
                geojson['properties'] = {
                    'name': "Convex hull of all Archaeological Entities"
                }
                geojson = json.dumps(geojson)
            except:
                geojson = None
            return geojson
        else:
            return None

    def get_next(self):
        next = Site.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Site.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_next_public(self):
        next = Site.objects.filter(id__gt=self.id)\
            .exclude(site_checked_by=None).exclude(public=False)
        if next:
            return next.first().id
        return False

    def get_prev_public(self):
        prev = Site.objects.filter(id__lt=self.id)\
            .exclude(site_checked_by=None).exclude(public=False).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:site_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.id)


@reversion.register()
class ResearchQuestion(IdProvider):
    question = models.TextField(
        blank=True, null=True, verbose_name="research question"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_researchquestions')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:researchquestion_create')

    def get_next(self):
        next = ResearchQuestion.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = ResearchQuestion.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:researchquestion_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['pk']
        verbose_name = "Research Question"


@modify_fields(identifier={
    'verbose_name': 'Activity ID',
    'help_text': 'Applies to Austrian sites.'})
@reversion.register()
class ResearchEvent(IadBaseClass):
    """The data set RESEARCH ACTIVITY comprises data on archaeological research conducted on\
    a specific site. At the same time a single research activity may result in discovery or\
    analysis of more than one site. Its extent is defined through a spatial polygon and type\
    of research, institution and duration. Research activity is any archaeological work that\
    contributed to new knowledge about the past. Data acquisition (ALS) conducted by\
    “non-archaeological” project will not be entered as a separate research activity.

    """

    site_id = models.ManyToManyField(
        Site, help_text="The unique identifier of related sites.",
        verbose_name="Related Sites", blank=True, related_name="has_research_activity"
    )
    legacy_research_id = models.CharField(
        blank=True, null=True,
        max_length=250,
    )
    start_date = models.DateField(
        blank=True, null=True,
        verbose_name="Start Date.",
        help_text="When did the research activity start? (YYYY-MM-DD)"
    )
    end_date = models.DateField(
        blank=True, null=True,
        verbose_name="End Date.",
        help_text="When did the research activity end? (YYYY-MM-DD)"
    )
    responsible_researcher = models.ManyToManyField(
        Person, blank=True, verbose_name="Responsible Researcher",
        related_name="has_research",
        help_text="Who is the responsible researcher/project leader of the conducted research?"
    )
    responsible_institution = models.ManyToManyField(
        Institution, blank=True, verbose_name="Responsible Institution",
        related_name="has_research",
        help_text="Which institution conducted the research?"
    )
    research_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Research Type",
        help_text="Was it a development led research or scientific research?",
        related_name="is_research_type_of",
        on_delete=models.SET_NULL
    )
    research_method = models.ManyToManyField(
        SkosConcept, blank=True, verbose_name="Research Methods",
        help_text="Which method has been applied?",
        related_name="is_research_method_of"
    )
    research_question = models.ForeignKey(
        ResearchQuestion, blank=True, null=True, verbose_name="Research Question",
        related_name="is_research_question_of",
        help_text="What was the initial research question to be answered\
        with the conducted research methods? Only for scientific research.",
        on_delete=models.SET_NULL
    )
    generation_data_set = models.DateField(
        blank=True, null=True,
        verbose_name="When was the data-set generated?", help_text="provide some (YYYY-MM-DD)"
    )

    class Meta:
        ordering = ['pk']
        verbose_name = "Research Activity"
        verbose_name_plural = "Research Activities"

    def get_geojson(self):
        geojson = serialize(
            'geojson', ResearchEvent.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'identifier', 'pk',)
        )
        return geojson

    def get_site_geojson(self):
        if self.site_id:
            geojson = serialize(
                'geojson', Site.objects.filter(has_research_activity__in=[self.id]),
                geometry_field='polygon',
                fields=('name', 'identifier',)
            )
        else:
            geojson = None
        return geojson

    def __str__(self):
        if self.start_date and self.responsible_researcher and self.research_method:
            researchers = " | ".join(
                [x.name for x in self.responsible_researcher.all()]
            )
            methods = " | ".join([x.pref_label for x in self.research_method.all()])
            return "{}; {}; {} (id:{})".format(
                self.start_date, researchers, methods, self.id
            )
        elif self.start_date and self.research_method:
            methods = " | ".join([x.pref_label for x in self.research_method.all()])
            return "{}; {} (id:{})".format(
                self.start_date, methods, self.id
            )
        return "{}".format(self.id)

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_researchevents')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:researchevent_create')

    @classmethod
    def get_dl_url(self):
        return reverse('browsing:dl_researchevent')

    def get_next(self):
        next = ResearchEvent.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = ResearchEvent.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:researchevent_detail', kwargs={'pk': self.id}
        )

    def convex_hulls(self):
        if self.site_id.exclude(polygon=None):
            geojson = json.loads(
                self.site_id.exclude(polygon=None)
                .aggregate(combined=Union('polygon'))['combined']
                .convex_hull.geojson
            )
            geojson['properties'] = {
                'name': "Convex hull of all related Sites"
            }
            geojson = json.dumps(geojson)
            return geojson
        else:
            return None


ARCHENT_CERTAINTY = (
    (
        '1 - high: data from more complementary methods and/or with relevant comparisons',
        '1 - high: data from more complementary methods and/or with relevant comparisons'
    ),
    (
        '2 - basic: data from only one method and without relevant comparisons',
        '2 - basic: data from only one method and without relevant comparisons'
    ),
    (
        '3 - low: not certain data from old finds or old not-verifiable sources',
        '3 - low: not certain data from old finds or old not-verifiable sources'
    )
)


@modify_fields(
    name={
        'verbose_name': 'Entity Name',
        'help_text': 'The name of the entity in the language\
        of the country where the entity is located.'
    },
    alt_name={
        'verbose_name': 'Entity Alternative Name',
        'help_text': 'Another name / Other names of the entity\
        (another spelling, language, alias name etc.)'
        }
    )
@reversion.register()
class ArchEnt(IadBaseClass):
    """An archaeological entity is defined by a specific human activity (entity type),
    period of this activity (dating) and spatial location (polygon inside of the site)."""

    site_id = models.ForeignKey(
        Site, help_text="The unique identifier of the site.",
        verbose_name="Site Name",
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="has_archent"
    )
    ent_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Entity Type", help_text="What type of area is it?",
        related_name="archent_type_related",
        on_delete=models.SET_NULL
    )
    burial_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Burial Type", help_text="Provide some helptext",
        related_name="burial_type_related",
        on_delete=models.SET_NULL
    )
    burial_construction = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Burial Construction", help_text="Provide some helptext",
        related_name="burial_construction_related",
    )
    settlement_fortification = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Settlement Fortification",
        help_text="If 'settlement' is the entity type, specify the type of fortification.",
        related_name="settlement_fortification_related"
    )
    settlement_occupation = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Settlement Occupation",
        help_text="If 'settlement' is the entity type, specify the type of occupation.",
        related_name="settlement_occupation_related",
        on_delete=models.SET_NULL
    )
    topography = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Topography",
        help_text="Where is the entity located",
        related_name="archent_topography"
    )
    type_certainty = models.CharField(
        blank=True, null=True, verbose_name="Entity Type Certainty",
        help_text="How certain is the interpretation of the arch. entity type",
        max_length=250,
        choices=ARCHENT_CERTAINTY
    )
    dating_certainty = models.CharField(
        blank=True, null=True, verbose_name="Dating Certainty",
        help_text="How reliable is the dating of the archaeological entity?",
        max_length=250,
        choices=ARCHENT_CERTAINTY
    )
    location_certainty = models.CharField(
        blank=True, null=True, verbose_name="Location Certainty",
        help_text="How accurate is the information on the location of the arch. entity",
        max_length=250,
        choices=ARCHENT_CERTAINTY
    )
    period = models.ManyToManyField(
        Period, blank=True, verbose_name="Dating",
        help_text="Dating of the archaeological entity."
    )

    def get_site_geojson(self):
        if self.site_id:
            geojson = serialize(
                'geojson', Site.objects.filter(has_archent__in=[self.id]),
                geometry_field='polygon',
                fields=('name', 'identifier',)
            )
        else:
            geojson = None
        return geojson

    class Meta:
        ordering = ['pk']
        verbose_name = "Archaeological Entity"

    def get_geojson(self):
        geojson = serialize(
            'geojson', ArchEnt.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'identifier', 'pk')
        )
        return geojson

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_archents')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:archent_create')

    @classmethod
    def get_dl_url(self):
        return reverse('browsing:dl_archent')

    def get_next(self):
        next = ArchEnt.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = ArchEnt.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:archent_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.identifier)


HERITAGE_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
    ('partially', 'partially'),
    ('in process', 'in process'),
)


@modify_fields(comment={
    'help_text': 'Any noteworthy information about the protection\
    of the site that has not been expressed in other fields. (other types ).'})
@reversion.register()
class MonumentProtection(IadBaseClass):

    """A table gathering information on the protection status of the site.\
    It is defined by a polygon."""

    site_id = models.ForeignKey(
        Site, help_text="The unique identifier of the site.",
        verbose_name="Site Name",
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name="has_monument_protection"
    )
    current_land_use = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Current Land Use",
        related_name="monument_protection_current_land_use",
        help_text="What activities are currently present at the site location?"
    )
    heritage_status = models.CharField(
        blank=True, null=True, verbose_name="Cultural Heritage Status",
        help_text="Has the site status of cultural heritage?",
        max_length=250,
        choices=HERITAGE_STATUS_CHOICES
    )
    natural_heritage_status = models.CharField(
        blank=True, null=True, verbose_name="Natural Heritage Status",
        help_text="Has the site status of natural heritage?",
        max_length=250,
        choices=HERITAGE_STATUS_CHOICES
    )
    threats = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="Threats",
        related_name="monument_protection_threats",
        help_text="Which activity is threatening the site?"
    )

    class Meta:
        ordering = ['pk']
        verbose_name = 'Monument Protection'

    def get_geojson(self):
        geojson = serialize(
            'geojson', MonumentProtection.objects.filter(id=self.id),
            geometry_field='polygon',
            fields=('name', 'identifier', 'pk',)
        )
        return geojson

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_monumentprotections')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:monumentprotection_create')

    @classmethod
    def get_dl_url(self):
        return reverse('browsing:dl_monumentprotection')

    def get_site_geojson(self):
        if self.site_id:
            geojson = serialize(
                'geojson', Site.objects.filter(has_monument_protection__in=[self.id]),
                geometry_field='polygon',
                fields=('name', 'identifier',)
            )
        else:
            geojson = None
        return geojson

    def get_next(self):
        next = MonumentProtection.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = MonumentProtection.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:monumentprotection_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        return "MonumentProtection {} for Site {}".format(self.id, self.site_id)
