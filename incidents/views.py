from django.shortcuts import render
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from incidents.serializer import InputGetIncidentsDataSerializer


class AllIncidentsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = InputGetIncidentsDataSerializer(data=request.query_params)
        if serializer.is_valid():
            length = serializer.validated_data['length']
            width = serializer.validated_data['width']
            radius = serializer.validated_data['radius']

            context = {
                "length": length,
                "width": width,
                "radius": radius
            }
            return Response(context, status=status.HTTP_200_OK)
