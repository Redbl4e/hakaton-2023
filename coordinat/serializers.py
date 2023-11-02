from datetime import datetime
from rest_framework import serializers

from users.models import Coordinate


class UpdateCoordinateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    def update(self, instance, validated_data):
        instance = Coordinate.objects.update(
            **validated_data, user_id=instance,
            last_online_data=datetime.now(),
        )
        return instance

    class Meta:
        model = Coordinate
        fields = ('user_id', 'latitude', 'longitude')
