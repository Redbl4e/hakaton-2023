from rest_framework import serializers


class Category(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class InputGetIncidentsDataSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    radius = serializers.FloatField()


class ReadGetIncidentDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    address = serializers.CharField()
    is_predictive = serializers.BooleanField()
    is_active = serializers.BooleanField()
    category = Category(read_only=True)
    created_at = serializers.DateTimeField()


class InputPutDeactivateIncident(serializers.Serializer):
    incident_id = serializers.IntegerField()


class InputGetIncidentDeatail(serializers.Serializer):
    incident_id = serializers.IntegerField()


class ReadGetIncidentDeatail(serializers.Serializer):
    user_id = serializers.IntegerField()
    title = serializers.CharField()
    media_path = serializers.CharField()
    created_at = serializers.DateTimeField()
