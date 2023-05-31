from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from reviews.models import Review
from reviews.serializers import ReviewSerializer

class ReviewView(viewsets.ModelViewSet):
    # TODO: crete review. filter by property
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer