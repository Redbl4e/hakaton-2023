from drf_yasg import openapi

longitude_param = openapi.Parameter('longitude', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER)
latitude_param = openapi.Parameter('latitude', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER)
radius_param = openapi.Parameter('radius', in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER)

incident_id = openapi.Parameter('incident_id', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
