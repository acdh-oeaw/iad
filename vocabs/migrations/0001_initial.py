# Generated by Django 5.0.7 on 2024-07-17 13:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Metadata",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=300)),
                (
                    "indentifier",
                    models.URLField(
                        blank=True, default="http://www.vocabs/provide-some-namespace/"
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "description_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                (
                    "language",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                ("version", models.CharField(blank=True, max_length=300)),
                (
                    "creator",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                (
                    "contributor",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                (
                    "subject",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                (
                    "owner",
                    models.CharField(
                        blank=True, help_text="Organisation or Person", max_length=300
                    ),
                ),
                ("license", models.CharField(blank=True, max_length=300)),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "date_issued",
                    models.DateField(blank=True, help_text="YYYY-MM-DD", null=True),
                ),
                (
                    "relation",
                    models.URLField(
                        blank=True,
                        help_text="e.g. in case of relation to a project, add link to a project website",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkosCollection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=300, verbose_name="Label"),
                ),
                (
                    "label_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                (
                    "creator",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                ("legacy_id", models.CharField(blank=True, max_length=200)),
                ("skos_note", models.CharField(blank=True, max_length=500)),
                (
                    "skos_note_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("skos_scopenote", models.TextField(blank=True)),
                (
                    "skos_scopenote_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("skos_changenote", models.CharField(blank=True, max_length=500)),
                ("skos_editorialnote", models.CharField(blank=True, max_length=500)),
                ("skos_example", models.CharField(blank=True, max_length=500)),
                ("skos_historynote", models.CharField(blank=True, max_length=500)),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkosLabel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="The entities label or name.",
                        max_length=100,
                        verbose_name="Label",
                    ),
                ),
                (
                    "label_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("prefLabel", "prefLabel"),
                            ("altLabel", "altLabel"),
                            ("hiddenLabel", "hiddenLabel"),
                        ],
                        help_text="The type of the label.",
                        max_length=30,
                    ),
                ),
                (
                    "isoCode",
                    models.CharField(
                        blank=True,
                        help_text="The ISO 639-3 code for the label's language.",
                        max_length=3,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkosNamespace",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "namespace",
                    models.URLField(
                        blank=True, default="http://www.vocabs/provide-some-namespace/"
                    ),
                ),
                (
                    "prefix",
                    models.CharField(blank=True, default="repos", max_length=50),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkosConceptScheme",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dc_title", models.CharField(blank=True, max_length=300)),
                (
                    "dc_title_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                (
                    "dc_creator",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                ("dc_description", models.TextField(blank=True)),
                (
                    "dc_description_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("legacy_id", models.CharField(blank=True, max_length=200)),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "namespace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vocabs.skosnamespace",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SkosConcept",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("pref_label", models.CharField(blank=True, max_length=300)),
                (
                    "pref_label_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("definition", models.TextField(blank=True)),
                (
                    "definition_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("notation", models.CharField(blank=True, max_length=300)),
                (
                    "top_concept",
                    models.BooleanField(
                        default=False,
                        help_text="Is this concept a top concept of main concept scheme?",
                    ),
                ),
                (
                    "same_as_external",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                        null=True,
                        verbose_name="URL of external Concept with the same meaning",
                    ),
                ),
                (
                    "source_description",
                    models.TextField(
                        blank=True,
                        help_text="A verbose description of the concept's source",
                        null=True,
                        verbose_name="Source",
                    ),
                ),
                ("legacy_id", models.CharField(blank=True, max_length=200)),
                (
                    "name_reverse",
                    models.CharField(
                        blank=True,
                        help_text='Inverse relation like:         "is sub-class of" vs. "is super-class of".',
                        max_length=255,
                        verbose_name="Name reverse",
                    ),
                ),
                ("skos_note", models.CharField(blank=True, max_length=500)),
                (
                    "skos_note_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("skos_scopenote", models.TextField(blank=True)),
                (
                    "skos_scopenote_lang",
                    models.CharField(blank=True, default="eng", max_length=3),
                ),
                ("skos_changenote", models.CharField(blank=True, max_length=500)),
                ("skos_editorialnote", models.CharField(blank=True, max_length=500)),
                ("skos_example", models.CharField(blank=True, max_length=500)),
                ("skos_historynote", models.CharField(blank=True, max_length=500)),
                (
                    "dc_creator",
                    models.TextField(
                        blank=True,
                        help_text="If more than one list all using a semicolon ;",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "broader_concept",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="narrower_concepts",
                        to="vocabs.skosconcept",
                        verbose_name="Broader Term",
                    ),
                ),
                (
                    "collection",
                    models.ManyToManyField(
                        blank=True,
                        related_name="has_members",
                        to="vocabs.skoscollection",
                    ),
                ),
                (
                    "skos_broader",
                    models.ManyToManyField(
                        blank=True, related_name="narrower", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_broadmatch",
                    models.ManyToManyField(
                        blank=True, related_name="narrowmatch", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_closematch",
                    models.ManyToManyField(
                        blank=True, related_name="closematch", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_exactmatch",
                    models.ManyToManyField(
                        blank=True, related_name="exactmatch", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_narrower",
                    models.ManyToManyField(
                        blank=True, related_name="broader", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_narrowmatch",
                    models.ManyToManyField(
                        blank=True, related_name="broadmatch", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_related",
                    models.ManyToManyField(
                        blank=True, related_name="related", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "skos_relatedmatch",
                    models.ManyToManyField(
                        blank=True, related_name="relatedmatch", to="vocabs.skosconcept"
                    ),
                ),
                (
                    "scheme",
                    models.ManyToManyField(
                        blank=True,
                        related_name="has_concepts",
                        to="vocabs.skosconceptscheme",
                    ),
                ),
                (
                    "other_label",
                    models.ManyToManyField(blank=True, to="vocabs.skoslabel"),
                ),
                (
                    "namespace",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vocabs.skosnamespace",
                    ),
                ),
            ],
        ),
    ]
