from rest_framework import serializers

from incidents.models import Incident, Category, PostIncident


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class IncidentSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    def deactivate(self, instance: Incident) -> Incident:
        instance.is_active = False
        instance.save()
        return instance

    class Meta:
        model = Incident
        fields = ['id', 'latitude', 'longitude', 'address', 'is_predictive', 'is_active', 'category', 'created_at']


class IncidentCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Incident
        fields = ['latitude', 'longitude', 'address', 'category']


class IncidentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostIncident
        fields = ['id', 'title', 'media_path', 'created_at', 'user_id']
