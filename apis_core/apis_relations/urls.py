from django.urls import path

from . import views
from . import person_place_relation_views
from . import person_work_relation_views
from . import person_person_relation_views
from . import person_institution_relation_views
from . import person_event_relation_views
from . import place_place_relation_views
from . import place_event_relation_views
from . import place_work_relation_views
from . import institution_institution_relation_views
from . import institution_place_relation_views
from . import institution_work_relation_views
from . import institution_event_relation_views
from .views import copy_relation


app_name = "apis_relations"

urlpatterns = [
    path(
        "copy/<relation_class>/<int:pk>",
        copy_relation,
        name="copy_relation",
    ),
    path(
        "institution-event/",
        institution_event_relation_views.InstitutionEventListView.as_view(),
        name="institutionevent",
    ),
    path(
        "institution-event/create/",
        institution_event_relation_views.InstitutionEventCreate.as_view(),
        name="institutionevent_create",
    ),
    path(
        "institution-event/edit/<int:pk>",
        institution_event_relation_views.InstitutionEventUpdate.as_view(),
        name="institutionevent_edit",
    ),
    path(
        "institution-work/",
        institution_work_relation_views.InstitutionWorkListView.as_view(),
        name="institutionwork",
    ),
    path(
        "institution-work/create/",
        institution_work_relation_views.InstitutionWorkCreate.as_view(),
        name="institutionwork_create",
    ),
    path(
        "institution-work/edit/<int:pk>",
        institution_work_relation_views.InstitutionWorkUpdate.as_view(),
        name="institutionwork_edit",
    ),
    path(
        "institution-place/",
        institution_place_relation_views.InstitutionPlaceListView.as_view(),
        name="institutionplace",
    ),
    path(
        "institution-place/create/",
        institution_place_relation_views.InstitutionPlaceCreate.as_view(),
        name="institutionplace_create",
    ),
    path(
        "institution-place/edit/<int:pk>",
        institution_place_relation_views.InstitutionPlaceUpdate.as_view(),
        name="institutionplace_edit",
    ),
    path(
        "institution-institution/",
        institution_institution_relation_views.InstitutionInstitutionListView.as_view(),
        name="institutioninstitution",
    ),
    path(
        "institution-institution/create/",
        institution_institution_relation_views.InstitutionInstitutionCreate.as_view(),
        name="institutioninstitution_create",
    ),
    path(
        "institution-institution/edit/<int:pk>",
        institution_institution_relation_views.InstitutionInstitutionUpdate.as_view(),
        name="institutioninstitution_edit",
    ),
    path(
        "place-work/",
        place_work_relation_views.PlaceWorkListView.as_view(),
        name="placework",
    ),
    path(
        "place-work/create/",
        place_work_relation_views.PlaceWorkCreate.as_view(),
        name="placework_create",
    ),
    path(
        "place-work/edit/<int:pk>",
        place_work_relation_views.PlaceWorkUpdate.as_view(),
        name="placework_edit",
    ),
    path(
        "place-event/",
        place_event_relation_views.PlaceEventListView.as_view(),
        name="placeevent",
    ),
    path(
        "place-event/create/",
        place_event_relation_views.PlaceEventCreate.as_view(),
        name="placeevent_create",
    ),
    path(
        "place-event/edit/<int:pk>",
        place_event_relation_views.PlaceEventUpdate.as_view(),
        name="placeevent_edit",
    ),
    path(
        "place_place/",
        place_place_relation_views.PlacePlaceListView.as_view(),
        name="placeplace",
    ),
    path(
        "place_place/create/",
        place_place_relation_views.PlacePlaceCreate.as_view(),
        name="placeplace_create",
    ),
    path(
        "place_place/edit/<int:pk>",
        place_place_relation_views.PlacePlaceUpdate.as_view(),
        name="placeplace_edit",
    ),
    path(
        "person-event/",
        person_event_relation_views.PersonEventListView.as_view(),
        name="personevent",
    ),
    path(
        "person-event/create/",
        person_event_relation_views.PersonEventCreate.as_view(),
        name="personevent_create",
    ),
    path(
        "person-event/edit/<int:pk>",
        person_event_relation_views.PersonEventUpdate.as_view(),
        name="personevent_edit",
    ),
    path(
        "person-institution/",
        person_institution_relation_views.PersonInstitutionListView.as_view(),
        name="personinstitution",
    ),
    path(
        "person-institution/create/",
        person_institution_relation_views.PersonInstitutionCreate.as_view(),
        name="personinstitution_create",
    ),
    path(
        "person-institution/edit/<int:pk>",
        person_institution_relation_views.PersonInstitutionUpdate.as_view(),
        name="personinstitution_edit",
    ),
    path(
        "person-place/",
        person_place_relation_views.PersonPlaceListView.as_view(),
        name="personplace",
    ),
    path(
        "person-place/create/",
        person_place_relation_views.PersonPlaceCreate.as_view(),
        name="personplace_create",
    ),
    path(
        "person-place/edit/<int:pk>",
        person_place_relation_views.PersonPlaceUpdate.as_view(),
        name="personplace_edit",
    ),
    path(
        "person-work/",
        person_work_relation_views.PersonWorkListView.as_view(),
        name="personwork",
    ),
    path(
        "person-work/create/",
        person_work_relation_views.PersonWorkCreate.as_view(),
        name="personwork_create",
    ),
    path(
        "person-work/edit/<int:pk>",
        person_work_relation_views.PersonWorkUpdate.as_view(),
        name="personwork_edit",
    ),
    path(
        "person-person/",
        person_person_relation_views.PersonPersonListView.as_view(),
        name="personperson",
    ),
    path(
        "person-person/create/",
        person_person_relation_views.PersonPersonCreate.as_view(),
        name="personperson_create",
    ),
    path(
        "person-person/edit/<int:pk>",
        person_person_relation_views.PersonPersonUpdate.as_view(),
        name="personperson_edit",
    ),
    path(
        "delete/<int:relation_id>/",
        views.delete_relation_view,
        name="delete_relation",
    ),
    path("ajax/get/", views.get_form_ajax, name="get_form_ajax"),
    path(
        "ajax/save/<entity_type>/<kind_form>/<int:SiteID>/<int:ObjectID>/",
        views.save_ajax_form,
        name="save_ajax_form",
    ),
    path(
        "ajax/save/<entity_type>/<kind_form>/<int:SiteID>/",
        views.save_ajax_form,
        name="save_ajax_form",
    ),
]
