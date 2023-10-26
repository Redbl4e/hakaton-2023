from django.contrib import admin
from django.urls import path

from incidents.views import AllIncidentsAPIView, DeactivateIncidentAPIView, IncedentsDetailAPIView, \
    CreateIncidentAPIView

app_name = 'incidents'

urlpatterns = [
    path("get/all/incidents/by/radius", AllIncidentsAPIView.as_view(),
         name="all_incidents"),
    path("put/deactivate/incedents", DeactivateIncidentAPIView.as_view(),
         name="deactivate_incidents"),
    path("get/incedents/detail", IncedentsDetailAPIView.as_view(),
         name="detail_incidents"),
    path("post/create_incident", CreateIncidentAPIView.as_view(),
         name="create_incident"),
]
