from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, viewsets, status
from users.models import User
from users.serializers import UserSerializer
from rest_framework.decorators import action

# NOTE: when trying to login you need to use this format
'''
    {
        "username" : "nat@a.com", -> email
        "password": "123123" -> password
    }
'''


class UserRetrieveUpdateListView(
    viewsets.ModelViewSet
):
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
    lookup_field = 'pk'

    @action(detail=False, methods=["POST"], name="revoke_auth_token")
    def logout(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({ 'message' : 'User Logged out successfully' }, status=status.HTTP_200_OK)