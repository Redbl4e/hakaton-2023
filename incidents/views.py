from datetime import datetime

from django.contrib.auth.decorators import login_required
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_NUMBER, TYPE_INTEGER, FORMAT_INT32, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from incidents.models import Incident, Category, PostIncident
from incidents.serializer import InputGetIncidentsDataSerializer, ReadGetIncidentDataSerializer, \
    InputPutDeactivateIncident, InputGetIncidentDeatail, ReadGetIncidentDeatail, InputPostIncidentDataSerializer
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
                                       type=TYPE_NUMBER, required=True)],
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


class DeactivateIncidentAPIView(APIView):
    @swagger_auto_schema(tags=['Incidents'],
                         operation_summary='deactive incidents',
                         responses={
                         },
                         manual_parameters=[
                             Parameter('incident_id', in_=IN_QUERY,
                                       type=TYPE_INTEGER, required=True)
                         ])
    def put(self, request):
        serializer = InputPutDeactivateIncident(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        # # user = request.user
        # # print(user)
        # # if user.is_superuser:
        incedents_id = serializer.validated_data.get("incident_id")
        if True:
            Incident.objects.filter(id=incedents_id). \
                update(is_active=False)

        return Response(status=status.HTTP_204_NO_CONTENT)


class IncedentsDetailAPIView(APIView):
    @swagger_auto_schema(tags=['Incidents'],
                         operation_summary='deactive incidents',
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
    def get(self, request):
        serializer = InputGetIncidentDeatail(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        incedents_id = serializer.validated_data.get("incident_id")
        data = PostIncident.objects.filter(incedents_id=incedents_id)
        serializer_response = ReadGetIncidentDeatail(data)
        return Response(serializer_response.validated_data, status=status.HTTP_200_OK)


class CreateIncidentAPIView(APIView):
    @swagger_auto_schema(tags=['Incidents'],
                         operation_summary='create incident',
                         responses={
                         },
                         manual_parameters=[
                             Parameter('longitude', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True),
                             Parameter('latitude', in_=IN_QUERY,
                                       type=TYPE_NUMBER, required=True),
                             Parameter('address', in_=IN_QUERY,
                                       type=TYPE_STRING, required=True),
                             Parameter('category_id', in_=IN_QUERY,
                                       type=TYPE_INTEGER, required=True)
                         ]
                         )
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            serializer = InputPostIncidentDataSerializer(data=request.query_params)

            if serializer.is_valid():
                longitude = serializer.validated_data['longitude']
                latitude = serializer.validated_data['latitude']
                address = serializer.validated_data['address']
                incident = Incident(longitude=longitude, latitude=latitude, address=address, created_at=datetime)
                incident.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Метод не поддерживается'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
