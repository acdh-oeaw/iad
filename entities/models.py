import re
from django.db import models
from django.urls import reverse
from idprovider.models import IdProvider

BOOLEAN_CHOICES = ((True, "Yes"), (False, "No"))


class AlternativeName(IdProvider):
    name = models.CharField(max_length=250, blank=True, help_text="Alternative Name")

    def get_absolute_url(self):
        return reverse("entities:alternativename_detail", kwargs={"pk": self.id})

    @classmethod
    def get_listview_url(self):
        return reverse("browsing:browse_altnames")

    @classmethod
    def get_createview_url(self):
        return reverse("entities:alternativename_create")

    def get_next(self):
        next = AlternativeName.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = AlternativeName.objects.filter(id__lt=self.id).order_by("-id")
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse("entities:alternativename_detail", kwargs={"pk": self.id})

    def __str__(self):
        return "{}".format(self.name)


class Place(IdProvider):
    PLACE_TYPES = (("city", "city"), ("country", "country"))

    """Holds information about entities."""
    name = models.CharField(max_length=250, blank=True, help_text="Normalized name")
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250,
        blank=True,
        help_text="Alternative names",
        related_name="altname_of_place",
    )
    geonames_id = models.CharField(max_length=50, blank=True, help_text="GND-ID")
    lat = models.DecimalField(max_digits=20, decimal_places=12, blank=True, null=True)
    lng = models.DecimalField(max_digits=20, decimal_places=12, blank=True, null=True)
    part_of = models.ForeignKey(
        "Place",
        null=True,
        blank=True,
        help_text="A place (country) this place is part of.",
        related_name="has_child",
        on_delete=models.CASCADE,
    )
    place_type = models.CharField(
        choices=PLACE_TYPES, null=True, blank=True, max_length=50
    )

    def get_geonames_url(self):
        if self.geonames_id.startswith("ht") and self.geonames_id.endswith(".html"):
            return self.geonames_id
        elif self.geonames_id.startswith("ht"):
            return self.geonames_id
        else:
            return "http://www.geonames.org/{}".format(self.geonames_id)

    def get_geonames_rdf(self):
        try:
            number = re.findall(r"\d+", str(self.geonames_id))[0]
            return None
        except Exception as e:
            return None

    def save(self, *args, **kwargs):
        if self.geonames_id:
            new_id = self.get_geonames_url()
            self.geonames_id = new_id
        super(Place, self).save(*args, **kwargs)

    @classmethod
    def get_listview_url(self):
        return reverse("browsing:browse_places")

    @classmethod
    def get_createview_url(self):
        return reverse("entities:place_create")

    @classmethod
    def get_arche_dump(self):
        return reverse("browsing:rdf_places")

    def get_next(self):
        next = Place.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Place.objects.filter(id__lt=self.id).order_by("-id")
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse("entities:place_detail", kwargs={"pk": self.id})

    def __str__(self):
        return "{}".format(self.name)


class Institution(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    written_name = models.CharField(
        max_length=300, blank=True, verbose_name="Written name"
    )
    inst_alt_name = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Alternative Name(s) for this Institution",
        help_text="Use '; ' to separate many alterantive names.",
    )
    authority_url = models.CharField(
        max_length=300, blank=True, verbose_name="Authority url"
    )
    adress = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Adress",
        help_text="Adress of the research institution/museum.",
    )
    contact = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Contact",
        help_text="Contact (email) of the research institution/museum.",
    )
    homepage = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Homepage",
        help_text="URL of the research institution/museum.",
    )
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250,
        blank=True,
        related_name="altname_of_inst",
        verbose_name="Alternative names",
    )
    abbreviation = models.CharField(
        max_length=300, blank=True, verbose_name="Abbreviation"
    )
    location = models.ForeignKey(
        Place, blank=True, null=True, on_delete=models.CASCADE, verbose_name="Location"
    )
    parent_institution = models.ForeignKey(
        "Institution",
        blank=True,
        null=True,
        related_name="children_institutions",
        on_delete=models.CASCADE,
        verbose_name="Parent institution",
    )
    comment = models.TextField(blank=True, verbose_name="Comment")

    @classmethod
    def get_arche_dump(self):
        return reverse("browsing:rdf_institutions")

    @classmethod
    def get_listview_url(self):
        return reverse("browsing:browse_institutions")

    @classmethod
    def get_createview_url(self):
        return reverse("entities:institution_create")

    def get_absolute_url(self):
        return reverse("entities:institution_detail", kwargs={"pk": self.id})

    def get_next(self):
        next = Institution.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Institution.objects.filter(id__lt=self.id).order_by("-id")
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "{}".format(self.written_name)


class Person(IdProvider):
    legacy_id = models.CharField(max_length=300, blank=True, verbose_name="Legacy ID")
    written_name = models.CharField(
        max_length=300, blank=True, verbose_name="Written name"
    )
    forename = models.CharField(max_length=300, blank=True, verbose_name="Forename")
    name = models.CharField(max_length=300, blank=True, verbose_name="Name")
    pers_alt_name = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Alternative Name(s) for this Person",
        help_text="Use '; ' to separate many alterantive names.",
    )
    acad_title = models.CharField(
        max_length=300, blank=True, verbose_name="Academic title"
    )
    alt_names = models.ManyToManyField(
        AlternativeName,
        max_length=250,
        blank=True,
        related_name="altname_of_persons",
        verbose_name="Alternative names",
    )
    belongs_to_institution = models.ForeignKey(
        Institution,
        blank=True,
        null=True,
        related_name="has_member",
        on_delete=models.CASCADE,
        verbose_name="Belongs to institution",
    )
    place_of_birth = models.ForeignKey(
        Place,
        blank=True,
        null=True,
        related_name="is_birthplace",
        on_delete=models.CASCADE,
        verbose_name="Place of Birth",
    )
    date_of_birth = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name="Date of Birth",
        help_text="YYYY-MM-DD",
    )
    authority_url = models.CharField(
        max_length=300, blank=True, verbose_name="Authority url"
    )
    comment = models.TextField(blank=True, verbose_name="Comment")
    public = models.BooleanField(
        default=False,
        verbose_name="Public",
        choices=BOOLEAN_CHOICES,
        help_text="Should this entry (and all related entries) be public\
        or only visible to the account holders? Can be made public\
        only after data-check was completed.",
    )

    class Meta:
        verbose_name = "Researcher"

    @classmethod
    def get_createview_url(self):
        return reverse("entities:person_create")

    @classmethod
    def get_listview_url(self):
        return reverse("browsing:browse_persons")

    @classmethod
    def get_arche_dump(self):
        return reverse("browsing:rdf_persons")

    def get_absolute_url(self):
        return reverse("entities:person_detail", kwargs={"pk": self.id})

    def get_next(self):
        next = Person.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Person.objects.filter(id__lt=self.id).order_by("-id")
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        if self.written_name:
            return "{}".format(self.written_name)
        elif self.name and self.forename:
            return "{}, {}".format(self.name, self.forename)
        elif self.name:
            return "{}".format(self.name)
        else:
            return "No name provided"
