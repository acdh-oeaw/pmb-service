from django.urls import path

from .tei_ac import TeiEntAc, TeiCompleterAc

from apis_core.apis_tei import views

app_name = "apis_tei"

urlpatterns = [
    path(
        "autocomplete/(?P<entity>[a-zA-Z0-9-]+)/$",
        TeiEntAc.as_view(),
        name="generic_entities_autocomplete",
    ),
    path(
        "tei-completer/(?P<entity>[a-zA-Z0-9-]+)/$",
        TeiCompleterAc.as_view(),
        name="tei_completer_autocomplete",
    ),
    path("person/<int:pk>$", views.person_as_tei, name="person_as_tei"),
    path("place/<int:pk>$", views.place_as_tei, name="place_as_tei"),
    path("org/<int:pk>$", views.org_as_tei, name="org_as_tei"),
    path("institution/<int:pk>$", views.org_as_tei, name="org_as_tei"),
    path("work/<int:pk>$", views.work_as_tei, name="work_as_tei"),
    path("uri-to-tei", views.uri_to_tei, name="uri_to_tei"),
]
