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
        blank=True, null=True, help_text="Description of the object."
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

    def __str__(self):
        return "{}".format(self.name)


class Period(IadBaseClass):
    start_date = models.IntegerField(blank=True, null=True)
    end_date = models.IntegerField(blank=True, null=True)
    norm_id = models.CharField(
        blank=True, null=True, max_length=250,
        verbose_name="Link to some norm data record like period io"
    )


class ResearchEvent(IadBaseClass):
    pass


class Site(IadBaseClass):
    """SITE is the highest class in the database and includes mostly geographical and
    administrative information about the area where past human activity has been recognized.
    It is defined by a spatial polygon"""

    cadastral_community = models.ManyToManyField(
        Place, blank=True, verbose_name="Cadastral Community",
        help_text="The cadastral community where the site is located."
    )
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
        related_name="basearch_type_certainty",
        on_delete='PROTECT'
    )
    dating_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="basearch_dating_certainty",
        on_delete='PROTECT'
    )
    location_certainty = models.ForeignKey(
        SkosConcept, blank=True, null=True,
        related_name="basearch_location_certainty",
        on_delete='PROTECT'
    )
    period = models.ManyToManyField(
        Period, blank=True, verbose_name="Other Present Periods",
        help_text="Other periods that were recorded on the site."
    )

    def __str__(self):
        return "Site: {}".format(self.site_id.name)


class Settlement(BaseArchEnt):
    topography = models.ManyToManyField(
        SkosConcept, blank=True, help_text="Where is the settlement located",
        related_name="settlement_topography"
    )
    fortification = models.ManyToManyField(
        SkosConcept, blank=True, help_text="Is the settlement fortified?",
        related_name="settlement_fortification"
    )


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
