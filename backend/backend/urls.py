"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})

urlpatterns = [
    path("", hello_world, name="testing"),
    path("api/v1/users/", include('users.urls')),
    path("api/v1/properties/", include('properties.urls')),
    path("api/v1/applications", include('applications.urls')),
    path("api/v1/reviews", include('reviews.urls')),
    path("api/v1/transactions", include('transactions.urls')),
]
