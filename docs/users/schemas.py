from drf_yasg import openapi

from docs.schemas import OpenAPISchema, string_schema, email_schema, boolean_schema

user_schema = OpenAPISchema(
    title='User', description='Пользователь',
    type_=openapi.TYPE_OBJECT, properties={
        'first_name': string_schema,
        'last_name': string_schema,
        'patronymic': string_schema,
        'email': email_schema,
        'username': string_schema,
        'is_staff': boolean_schema,
    }
)
