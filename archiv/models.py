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
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    norm_id = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Link to some norm data record like period io"
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
        Period, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site."
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
        return "{}".format(self.name)


class BaseArchEnt(IadBaseClass):
    """An archaeological entity is defined by a specific human activity (entity type),
    period of this activity (dating) and spatial location (polygon inside of the site)."""

    site_id = models.ForeignKey(
        Site, help_text="The unique identifier of the site.",
        blank=True, null=True, on_delete='PROTECT'
    )
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    type_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="%(app_label)s_%(class)s_type_related",
        on_delete='PROTECT'
    )
    dating_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="%(app_label)s_%(class)s_dating_related",
        on_delete='PROTECT'
    )
    location_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="%(app_label)s_%(class)s_location_related",
        on_delete='PROTECT'
    )
    period = models.ManyToManyField(
        Period, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site."
    )

    class Meta:
        abstract = True


class Settlement(BaseArchEnt):
    topography = models.ManyToManyField(
        SkosConcept, blank=True, help_text="Where is the settlement located",
        related_name="settlement_topography"
    )
    fortification = models.ManyToManyField(
        SkosConcept, blank=True, help_text="Is the settlement fortified?",
        related_name="settlement_fortification"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_settlements')

    @classmethod
    def get_createview_url(self):
        return reverse('archiv:settlement_create')

    def get_next(self):
        next = Settlement.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Settlement.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse(
            'archiv:settlement_detail', kwargs={'pk': self.id}
        )

    def __str__(self):
        return "{}".format(self.name)


class Cemetery(BaseArchEnt):
    grave_type = models.ManyToManyField(
        SkosConcept, blank=True, help_text="provide some helptext",
        related_name="cemetery_grave_type"
    )
    burial_type = models.ManyToManyField(
        SkosConcept, blank=True, help_text="provide some helptext",
        related_name="cemetery_burial_type"
    )

    def __str__(self):
        return "Site: {}, Type: {}".format(self.site_id.name, self.__class__.__name__)


class ExtractionArea(BaseArchEnt):
    ea_type = models.ManyToManyField(
        SkosConcept, blank=True, help_text="provide some helptext",
        related_name="ea_grave_type"
    )


class Communication(BaseArchEnt):
    comm_type = models.ManyToManyField(
        SkosConcept, blank=True, help_text="provide some helptext",
        related_name="comm_grave_type"
    )


class Find(BaseArchEnt):
    find_type = models.ManyToManyField(
        SkosConcept, blank=True, help_text="provide some helptext",
        related_name="find_grave_type"
    )
