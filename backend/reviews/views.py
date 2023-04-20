from django.shortcuts import render
from rest_framework import viewsets
from reviews.models import Review

class ReviewView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = Review    