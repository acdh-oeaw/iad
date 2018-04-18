from django.urls import reverse
from django.contrib.gis.db import models
from idprovider.models import IdProvider
from entities.models import Place, Person, Institution
from vocabs.models import SkosConcept
from bib.models import Book

HERITAGE_STATUS_CHOICES = (
    ('yes', 'yes'),
    ('no', 'no'),
    ('partially', 'partially'),
)


VALUE_STATUS_CHOICES = (
    ('1 - high', '1 - high'),
    ('2 - middle', '2 - middle'),
    ('3 - low', '3 - low'),
)


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
        blank=True, null=True, help_text="""Any noteworthy general information about the object
        that cannot be expressed in other fields."""
    )
    public = models.BooleanField(
        default=False, help_text="""Should this entry (and all related entries) be public
        or only visible to the account holders?
        Can be made public only after data-check was completed."""
    )
    literature = models.ManyToManyField(
        Book, blank=True, help_text="provide some"
    )
    polygon = models.MultiPolygonField(blank=True, null=True, srid=4326)

    class Meta:
        abstract = True


class Period(IadBaseClass):
    start_date = models.IntegerField(
        blank=True, null=True,
        verbose_name="Earliest beginning of the period.",
        help_text="Must be a number!"
    )
    start_date_latest = models.IntegerField(
        blank=True, null=True,
        verbose_name="Latest beginning of the period.",
        help_text="Must be a number!"
    )
    end_date = models.IntegerField(
        blank=True, null=True,
        verbose_name="Earliest end of the period.",
        help_text="Must be a number!"
    )
    end_date_latest = models.IntegerField(
        blank=True, null=True,
        verbose_name="Latest end of the period.",
        help_text="Must be a number!"
    )
    norm_id = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Link to some norm data record like period io"
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
        on_delete=models.CASCADE
    )
    bibl = models.TextField(
        blank=True, null=True, verbose_name="Bibliographic source for this period."
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_periods')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:period_create')

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


class ResearchEvent(IadBaseClass):
    """Please Provide some Information about this Class"""

    start_date = models.CharField(
        blank=True, null=True,
        max_length=250,
        verbose_name="Start Date.",
        help_text="Start Date"
    )
    end_date = models.CharField(
        max_length=250,
        blank=True, null=True,
        verbose_name="End Date.",
        help_text="End Date"
    )
    responsible_researcher = models.ManyToManyField(
        Person, blank=True, verbose_name="Responsible Researcher",
        related_name="has_research"
    )
    responsible_institution = models.ManyToManyField(
        Institution, blank=True, verbose_name="Responsible Institution",
        related_name="has_research"
    )
    research_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        verbose_name="Research Methods",
        related_name="is_research_type_of",
        on_delete=models.CASCADE
    )
    research_method = models.ManyToManyField(
        SkosConcept, blank=True, verbose_name="Research Methods",
        related_name="is_research_method_of"
    )
    research_question = models.ForeignKey(
        ResearchQuestion, blank=True, null=True, verbose_name="Research Question",
        related_name="is_research_question_of",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.name)

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_researchevents')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:researchevent_create')

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


class Site(IadBaseClass):
    """SITE is the highest class in the database and includes mostly geographical and
    administrative information about the area where past human activity has been recognized.
    It is defined by a spatial polygon"""

    cadastral_community = models.ManyToManyField(
        Place, blank=True, verbose_name="Cadastral Community",
        help_text="The cadastral community where the site is located.",
        related_name="has_sites"
    )
    cadastral_number = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Cadastral Number",
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
    period = models.ManyToManyField(
        Period, blank=True, verbose_name="Period (to be deprecated)",
        help_text="Dating of all ARCHAEOLOGICAL ENTITIES of this particular site"
    )
    other_period = models.ManyToManyField(
        SkosConcept, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site.",
        related_name="has_other_period"
    )
    information_source = models.ManyToManyField(
        ResearchEvent, blank=True,
        help_text="How was the site discovered? Choose the corresponding research event.",
        related_name="has_related_site"
    )
    accessibility = models.CharField(
        blank=True, null=True, verbose_name="accessibility",
        help_text="provide some",
        max_length=250,
        choices=VALUE_STATUS_CHOICES
    )
    visibility = models.CharField(
        blank=True, null=True, verbose_name="visibility",
        help_text="provide some",
        max_length=250,
        choices=VALUE_STATUS_CHOICES
    )
    infrastructure = models.CharField(
        blank=True, null=True, verbose_name="infrastructure",
        help_text="provide some",
        max_length=250,
        choices=VALUE_STATUS_CHOICES
    )
    long_term_management = models.CharField(
        blank=True, null=True, verbose_name="long_term_management",
        help_text="provide some",
        max_length=250,
        choices=VALUE_STATUS_CHOICES
    )
    potential_surrounding = models.CharField(
        blank=True, null=True, verbose_name="potential_surrounding",
        help_text="provide some",
        max_length=250,
        choices=VALUE_STATUS_CHOICES
    )
    museum = models.ManyToManyField(
        Institution, blank=True, verbose_name="Responsible Institution",
        help_text="Where are the finds from the site stored?",
        related_name="is_museum"
    )
    iad_app = models.BooleanField(
        verbose_name="iad_app",
        default=False, help_text="Should this site be used in the IAD-App?"
    )
    app_description = models.TextField(
        blank=True, null=True, verbose_name="app_description",
        help_text="If the site is going to be used in the IAD app, please provide the \
        description of the site to be implemented into the app."
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_sites')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:site_create')

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

    def get_absolute_url(self):
        return reverse(
            'archiv:site_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        if self.name:
            return "{}".format(self.name)
        else:
            return "{}".format(self.identifier)


class ArchEnt(IadBaseClass):
    """An archaeological entity is defined by a specific human activity (entity type),
    period of this activity (dating) and spatial location (polygon inside of the site)."""

    site_id = models.ForeignKey(
        Site, help_text="The unique identifier of the site.",
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="has_archent"
    )
    ent_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_type_related",
        on_delete=models.CASCADE
    )
    topography = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_topography",
        on_delete=models.CASCADE
    )
    burial_type = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_burial_type",
        on_delete=models.CASCADE
    )
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    type_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_type_cert_related",
        on_delete=models.CASCADE
    )
    dating_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_dating_cert_related",
        on_delete=models.CASCADE
    )
    location_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="archent_location_related",
        on_delete=models.CASCADE
    )
    period = models.ManyToManyField(
        Period, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site."
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_archents')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:archent_create')

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


class MonumentProtection(IadBaseClass):
    site_id = models.ForeignKey(
        Site, help_text="The unique identifier of the site.",
        verbose_name="Site",
        blank=True, null=True, on_delete=models.CASCADE,
        related_name="has_monument_protection"
    )
    current_land_use = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="current land use",
        related_name="monument_protection_current_land_use",
        help_text="provide some"
    )
    heritage_status = models.CharField(
        blank=True, null=True, verbose_name="heritage status",
        help_text="provide some",
        max_length=250,
        choices=HERITAGE_STATUS_CHOICES
    )
    threats = models.ManyToManyField(
        SkosConcept, blank=True,
        verbose_name="threats",
        related_name="monument_protection_threats",
        help_text="provide some"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_monumentprotections')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:monumentprotection_create')

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
