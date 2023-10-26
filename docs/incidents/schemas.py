from drf_yasg import openapi

from docs.schemas import OpenAPISchema, int32_schema, number_schema, string_schema, boolean_schema, datetime_schema

category_schema = OpenAPISchema(
    title='Category', type_=openapi.TYPE_OBJECT, properties={
        'id': int32_schema,
        'name': string_schema
    }
)

incident_schema = OpenAPISchema(
    title='Incident', type_=openapi.TYPE_OBJECT, properties={
        'id': int32_schema,
        'latitude': number_schema,
        'longitude': number_schema,
        'address': string_schema,
        'is_active': boolean_schema,
        'is_predictive': boolean_schema,
        'category': category_schema,
        'created_at': datetime_schema
    }
)
