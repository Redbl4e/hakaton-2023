from django.urls import path

from incidents.views import IncidentAPIView, DeactivateIncidentAPIView, IncidentDetailAPIView

app_name = 'incidents'

urlpatterns = [
    path("", IncidentAPIView.as_view(), name="all_incidents"),
    path("detail", IncidentDetailAPIView.as_view(), name="detail_incidents"),
    path("<int:pk>/update/", DeactivateIncidentAPIView.as_view(), name="deactivate_incidents"),
]
