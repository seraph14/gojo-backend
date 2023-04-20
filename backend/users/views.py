from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import User
from .serializers import UserSerializer

class UserRetreiveUpdateListView(
    generics.RetrieveUpdateDestroyAPIView, 
    generics.ListCreateAPIView):
    '''
    This is how the data should be sent to the server.
        {
            "first_name" :"1",
            "last_name": "last",
            "email" : "e@e.com".
            "password": "123123"
        }
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return self.request.user