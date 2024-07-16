# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "bib"

urlpatterns = [
    path(
        "reference/detail/<int:pk>$",
        views.ReferenceDetailView.as_view(),
        name="reference_detail",
    ),
    path(
        "reference/delete/<int:pk>$",
        views.ReferenceDelete.as_view(),
        name="reference_delete",
    ),
    path("references/$", views.ReferenceListView.as_view(), name="browse_references"),
]
