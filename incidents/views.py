from datetime import datetime

from django.contrib.auth.decorators import login_required
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_NUMBER, TYPE_INTEGER, FORMAT_INT32, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.incidents.params import latitude_param, radius_param, longitude_param, incident_id
from docs.incidents.schemas import incident_schema, detail_incident_schema
from docs.schemas import error_schema
from exceptions import ValidationError
from incidents.filters import IncidentDetailFilter
from incidents.serializer import IncidentSerializer, IncidentCreateSerializer, IncidentDetailSerializer

from incidents.models import Incident, Category, PostIncident


class IncidentAPIView(GenericAPIView):
    queryset = Incident.objects.all()

    @swagger_auto_schema(
        tags=['Incident'], operation_summary='Получить все инциденты', manual_parameters=[
            longitude_param, latitude_param, radius_param
        ], responses={
            status.HTTP_400_BAD_REQUEST: error_schema
        })
    def get(self, request: Request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Incident'], operation_summary='Добавить инцидент', responses={
            status.HTTP_201_CREATED: incident_schema,
            status.HTTP_400_BAD_REQUEST: error_schema
        }
    )
    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        incident = serializer.save()
        response_serializer = IncidentSerializer(incident)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IncidentCreateSerializer
        return IncidentSerializer

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        radius = self.request.query_params.get('radius')
        if not all((longitude, latitude, radius)):
            raise ValidationError('Обязательно нужно указать все 3 параметра')

        query = f'''SELECT i.id, i.longitude, i.latitude, i.address, i.is_active, i.is_predictive, i.created_at, c.id, c.name
                FROM incidents_incident as i
                LEFT JOIN incidents_category AS c
                ON i.category_id = c.id
                WHERE (ST_DistanceSphere(
                    ST_MakePoint(i.longitude, i.latitude),
                    ST_MakePoint({longitude}, {latitude})
                ) <= {radius}) AND (i.is_active = True OR i.is_predictive = True);'''
        incidents = Incident.objects.raw(query)
        return incidents


class DeactivateIncidentAPIView(GenericAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=['Incidents'], operation_summary='Отключить инцедент', responses={
            status.HTTP_201_CREATED: incident_schema,
            status.HTTP_400_BAD_REQUEST: error_schema
        }, )
    def get(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.deactivate(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class IncidentDetailAPIView(GenericAPIView):
    queryset = PostIncident.objects.all()
    serializer_class = IncidentDetailSerializer
    filter_backends = [IncidentDetailFilter]

    @swagger_auto_schema(
        tags=['Incidents'], operation_summary='Детали инцидента', responses={
            status.HTTP_200_OK: detail_incident_schema,
            status.HTTP_400_BAD_REQUEST: error_schema
        },
        manual_parameters=[
            incident_id
        ]
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
