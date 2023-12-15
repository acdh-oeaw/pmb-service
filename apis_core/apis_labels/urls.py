# -*- coding: utf-8 -*-
from django.urls import path

from . import views

app_name = "apis_labels"

urlpatterns = [
    path("list/", views.LabelListView.as_view(), name="label_list"),
    path("create/", views.label_create, name="label_create"),
    path("edit/<int:pk>", views.label_edit, name="label_edit"),
    path("delete/<int:pk>", views.LabelDelete.as_view(), name="label_delete"),
    path("delete-from-tabel/<int:label_id>/", views.delete_label, name="label_delete"),
]
