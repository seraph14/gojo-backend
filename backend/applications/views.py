from django.shortcuts import render
from rest_framework import viewsets

from .serializers import *

class ApplicationView(viewsets.ModelViewSet):
    queryset =  Application.objects.all()
    serializer_class =  ApplicationSerializer