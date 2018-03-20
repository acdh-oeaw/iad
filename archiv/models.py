from django.urls import reverse
from django.contrib.gis.db import models
from idprovider.models import IdProvider
from entities.models import Place
from vocabs.models import SkosConcept
from bib.models import Book


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


class ResearchEvent(IadBaseClass):
    """Please Provide some Information about this Class"""

    def __str__(self):
        return self.name

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
        help_text="The cadastral community where the site is located."
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
        Period, blank=True, verbose_name="some verbose name???"
    )
    other_period = models.ManyToManyField(
        SkosConcept, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site.",
        related_name="has_other_period"
    )
    information_source = models.ManyToManyField(
        ResearchEvent, blank=True,
        help_text="How was the site discovered? Choose the corresponding research event."
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
