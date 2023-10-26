from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_NUMBER, TYPE_INTEGER
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from docs.incidents.params import latitude_param, radius_param, longitude_param
from docs.incidents.schemas import incident_schema
from docs.schemas import error_schema
from exceptions import ValidationError
from incidents.models import Incident, PostIncident
from incidents.serializer import IncidentSerializer, IncidentCreateSerializer


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
