from django.urls import path
from . import views

app_name = "vocabs"


urlpatterns = [
    path("", views.SkosConceptListView.as_view(), name="skosconcept_list"),
    path("concepts/browse/", views.SkosConceptListView.as_view(), name="browse_vocabs"),
    path(
        "<int:pk>",
        views.SkosConceptDetailView.as_view(),
        name="skosconcept_detail",
    ),
    path("create/", views.SkosConceptCreate.as_view(), name="skosconcept_create"),
    path(
        "update/<int:pk>",
        views.SkosConceptUpdate.as_view(),
        name="skosconcept_update",
    ),
    path(
        "delete/<int:pk>",
        views.SkosConceptDelete.as_view(),
        name="skosconcept_delete",
    ),
    path("scheme/", views.SkosConceptSchemeListView.as_view(), name="browse_schemes"),
    path(
        "scheme/<int:pk>",
        views.SkosConceptSchemeDetailView.as_view(),
        name="skosconceptscheme_detail",
    ),
    path(
        "scheme/create/",
        views.SkosConceptSchemeCreate.as_view(),
        name="skosconceptscheme_create",
    ),
    path(
        "scheme/update/<int:pk>",
        views.SkosConceptSchemeUpdate.as_view(),
        name="skosconceptscheme_update",
    ),
    path(
        "scheme/delete/<int:pk>",
        views.SkosConceptSchemeDelete.as_view(),
        name="skosconceptscheme_delete",
    ),
    path("label/", views.SkosLabelListView.as_view(), name="browse_skoslabels"),
    path(
        "label/<int:pk>",
        views.SkosLabelDetailView.as_view(),
        name="skoslabel_detail",
    ),
    path("label/create/", views.SkosLabelCreate.as_view(), name="skoslabel_create"),
    path(
        "label/update/<int:pk>",
        views.SkosLabelUpdate.as_view(),
        name="skoslabel_update",
    ),
    path(
        "skoslabel/delete/<int:pk>",
        views.SkosLabelDelete.as_view(),
        name="skoslabel_delete",
    ),
    path("vocabs-download/", views.SkosConceptDL.as_view(), name="vocabs-download"),
    path("metadata/", views.MetadataListView.as_view(), name="metadata"),
    path(
        "metadata/<int:pk>",
        views.MetadataDetailView.as_view(),
        name="metadata_detail",
    ),
    path("metadata/create/", views.MetadataCreate.as_view(), name="metadata_create"),
    path(
        "metadata/update/<int:pk>",
        views.MetadataUpdate.as_view(),
        name="metadata_update",
    ),
    path(
        "metadata/delete/<int:pk>",
        views.MetadataDelete.as_view(),
        name="metadata_delete",
    ),
    path(
        "collection/",
        views.SkosCollectionListView.as_view(),
        name="browse_skoscollections",
    ),
    path(
        "collection/<int:pk>",
        views.SkosCollectionDetailView.as_view(),
        name="skoscollection_detail",
    ),
    path(
        "collection/create/",
        views.SkosCollectionCreate.as_view(),
        name="skoscollection_create",
    ),
    path(
        "collection/update/<int:pk>",
        views.SkosCollectionUpdate.as_view(),
        name="skoscollection_update",
    ),
    path(
        "collection/delete/<int:pk>",
        views.SkosCollectionDelete.as_view(),
        name="skoscollection_delete",
    ),
]
