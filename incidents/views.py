from django.shortcuts import render
from rest_framework import routers
from rest_framework.views import APIView


class AllIncidentsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass
