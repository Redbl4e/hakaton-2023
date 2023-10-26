from django.urls import path

from incidents.views import IncidentAPIView, DeactivateIncidentAPIView, IncidentDetailAPIView, CreateIncidentPostAPIView

app_name = 'incidents'

urlpatterns = [
    path('', IncidentAPIView.as_view(), name='all_incidents'),
    path('<int:pk>/', IncidentDetailAPIView.as_view(), name='detail'),
    path('<int:pk>/update/', DeactivateIncidentAPIView.as_view(), name='deactivate_incidents'),
    path('add-post/', CreateIncidentPostAPIView.as_view(), name='add_post'),
]
