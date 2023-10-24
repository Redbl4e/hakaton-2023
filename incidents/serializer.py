from rest_framework import serializers


class InputGetIncidentsDataSerializer(serializers.Serializer):
    longitude = serializers.FloatField(required=True,
                                       write_only=True)
    latitude = serializers.FloatField(required=True,
                                      write_only=True)
    radius = serializers.FloatField(required=True,
                                    write_only=True)
