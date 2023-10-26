from rest_framework import serializers

from incidents.models import Incident, Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class IncidentSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Incident
        fields = ['id', 'latitude', 'longitude', 'address', 'is_predictive', 'is_active', 'category', 'created_at']


class IncidentCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Incident
        fields = ['latitude', 'longitude', 'address', 'category']
