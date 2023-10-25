from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_NUMBER, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from incidents.models import Incident, Category
from incidents.serializer import InputGetIncidentsDataSerializer, ReadGetIncidentDataSerializer
from incidents.service.query_all_incedents import get_query_for_all_incedents_by_radius


class AllIncidentsAPIView(APIView):

    @swagger_auto_schema(tags=['Incidents'],
                         operation_summary='get all incidents',
                         responses={
                         },
                         manual_parameters=[
                             Parameter('longitude', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True),
                             Parameter('latitude', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True),
                             Parameter('radius', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True)
                         ]
                         )
    def get(self, request, *args, **kwargs):
        serializer = InputGetIncidentsDataSerializer(data=
                                                     request.query_params)
        serializer.is_valid(raise_exception=True)
        raw_query = get_query_for_all_incedents_by_radius(serializer.data)
        incedents = Incident.objects.prefetch_related("category")
        incedents_row = incedents.raw(raw_query)
        serializer_response = ReadGetIncidentDataSerializer(incedents_row, many=True)
        return Response(serializer_response.data, status=status.HTTP_200_OK)


class DeactivateIncident(APIView):
    @swagger_auto_schema(tags=['Deactive.Incident'],
                         operation_summary='get all incidents',
                         responses={
                         },
                         manual_parameters=[
                             Parameter('incident_id', in_=IN_QUERY,
                                       type=TYPE_INTEGER, required=True),
                             Parameter('latitude', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True),
                             Parameter('radius', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True)
                         ]
                         )
    def deactivate_incident(self):
        pass