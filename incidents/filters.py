from django.db.models import QuerySet
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request

from exceptions import ValidationError


class RadiusFilter(BaseFilterBackend):

    def get_search_terms(self, request: Request, view) -> tuple[float, float, float]:
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        radius = request.query_params.get('radius')
        return longitude, latitude, radius

    def get_search_fields(self, view) -> tuple[str, str]:
        return getattr(view, 'search_fields')

    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        longitude, latitude, radius = self.get_search_terms(request, view)
        if not all((longitude, latitude, radius)):
            raise ValidationError('Все три поля обязательные')

        longitude, latitude = self.get_search_fields(view)

        # query = f'''SELECT * FROM incidents_incident as i
        #        LEFT JOIN incidents_category AS c
        #        ON i.category_id = c.id
        #        WHERE (ST_DistanceSphere(
        #          ST_MakePoint(i.longitude, i.latitude),
        #          ST_MakePoint({longitude}, {latitude})
        #        ) <= {radius}) AND (i.is_active = True OR i.is_predictive = True);'''
        # filtered_queryset = queryset.filter()


class IncidentDetailFilter(BaseFilterBackend):
    def get_search_terms(self, request: Request, view) -> int:
        incedent_id = request.query_params.get('incident_id')
        return incedent_id

    def get_search_fields(self, view) -> int:
        return getattr(view, 'search_fields')

    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        incident_id = self.get_search_terms(request, view)
        if incident_id is None:
            raise ValidationError('Поле обязательные')

        filtered_queryset = queryset.filter(incident_id=incident_id)
        return filtered_queryset


class HistoryFilter(BaseFilterBackend):
    def get_search_terms(self, request: Request, view) -> tuple:
        longitude = request.query_params.get('longitude')
        latitude = request.query_params.get('latitude')
        return longitude, latitude

    def get_search_fields(self, view) -> int:
        return getattr(view, 'search_fields')

    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        longitude, latitude = self.get_search_terms(request, view)
        if not all((longitude, latitude)):
            raise ValidationError('Поля обязательные')
        filtered_queryset = queryset.filter(
            longitude=longitude, latitude=latitude)

        return filtered_queryset


class UserHistoryFilter(BaseFilterBackend):
    def get_search_terms(self, request: Request, view) -> tuple:
        user_id = request.query_params.get('user_id')
        return user_id

    def get_search_fields(self, view) -> int:
        return getattr(view, 'search_fields')

    def filter_queryset(self, request: Request, queryset: QuerySet, view):
        user_id= self.get_search_terms(request, view)
        if user_id is None:
            raise ValidationError('Поля обязательные')
        filtered_queryset = queryset.filter(
            user=user_id)
        return filtered_queryset
