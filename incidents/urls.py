from django.urls import path

from incidents.views import IncidentAPIView, DeactivateIncidentAPIView, IncedentsDetailAPIView

app_name = 'incidents'

urlpatterns = [
    path("", IncidentAPIView.as_view(), name="all_incidents"),
    path("update/", DeactivateIncidentAPIView.as_view(), name="deactivate_incidents"),
    path("<int:pk>/", IncedentsDetailAPIView.as_view(), name="detail_incidents"),
]
