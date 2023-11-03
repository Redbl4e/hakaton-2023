from rest_framework import serializers

from incidents.models import Incident, Category, PostIncident
from utils.serializers import DynamicFieldsModelSerializer


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class IncidentPostSerializer(serializers.ModelSerializer):
    incident = serializers.PrimaryKeyRelatedField(queryset=Incident.objects.all(), write_only=True)

    def create(self, validated_data):
        validated_data['user_id'] = self.context['request'].user.pk
        return super().create(validated_data)

    class Meta:
        model = PostIncident
        fields = ['id', 'title', 'photo', 'incident', 'created_at', 'user_id']


class IncidentSerializer(DynamicFieldsModelSerializer):
    category = CategorySerializer()
    posts = IncidentPostSerializer(many=True)

    def deactivate(self, instance: Incident) -> Incident:
        instance.is_active = False
        instance.save()
        return instance

    class Meta:
        model = Incident
        fields = [
            'id', 'latitude', 'longitude', 'address', 'is_predictive', 'is_active', 'category', 'created_at', 'posts'
        ]


class IncidentCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Incident
        fields = ['latitude', 'longitude', 'address', 'category']


class UsersIncidentSerializer(serializers.ModelSerializer):
    incident = IncidentSerializer()

    class Meta:
        model = PostIncident
        fields = ('id', 'title', 'photo', 'created_at', "user",
                  'incident')
