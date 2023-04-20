from django.shortcuts import render
from rest_framework import generics, mixins 
from .serializers import PropertySerializer
from .models import Property
from rest_framework.permissions import AllowAny, IsAuthenticated

class PropertyView(
    mixins.CreateModelMixin, 
    # mixins.UpdateModelMixin, 
    mixins.ListModelMixin, 
    # mixins.RetrieveModelMixin
):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [AllowAny,]