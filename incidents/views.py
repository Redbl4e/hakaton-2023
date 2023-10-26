from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from docs.incidents.params import latitude_param, radius_param, longitude_param
from docs.incidents.schemas import incident_schema, detail_incident_schema
from docs.schemas import error_schema
from exceptions import ValidationError
from incidents.models import Incident
from incidents.serializers import IncidentSerializer, IncidentCreateSerializer, IncidentPostSerializer


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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fields'] = [
            'id', 'longitude', 'latitude', 'address', 'is_predictive', 'is_active', 'created_at', 'category'
        ]
        return context


class DeactivateIncidentAPIView(GenericAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        tags=['Incident'], operation_summary='Отключить инцидент', responses={
            status.HTTP_201_CREATED: incident_schema,
            status.HTTP_400_BAD_REQUEST: error_schema
        }, )
    def get(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.deactivate(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class IncidentDetailAPIView(GenericAPIView):
    serializer_class = IncidentSerializer
    lookup_url_kwarg = 'pk'

    @swagger_auto_schema(
        tags=['Incident'], operation_summary='Детали инцидента', responses={
            status.HTTP_200_OK: detail_incident_schema,
            status.HTTP_400_BAD_REQUEST: error_schema
        }
    )
    def get(self, request, *args, **kwargs):
        incident = self.get_object()
        serializer = self.get_serializer(incident)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Incident.objects.prefetch_related('posts')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['fields'] = ['id', 'posts']
        return context


class CreateIncidentPostAPIView(CreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentPostSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Incident'], operation_summary='Добавить пост к инциденту', responses={
            status.HTTP_400_BAD_REQUEST: error_schema
        }
    )
    def post(self, request: Request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
