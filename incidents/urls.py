from django.contrib import admin
from django.urls import path, include

from incidents.views import AllIncidentsAPIView

app_name = 'incidents'

urlpatterns = [
    path("get/all/incidents/", AllIncidentsAPIView.as_view(),
         name="all_incidents")
]
