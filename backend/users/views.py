from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from users.models import User
from users.serializers import UserSerializer
from users.utilities import UserTypes
from users.permissions import *

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

    def get_permissions(self):
        if self.action == "create" and \
                self.request.data.get("role", UserTypes.TENANT) in [UserTypes.TENANT, UserTypes.LANDLORD]:
            return [AllowAny(),]       
        user_id = self.kwargs.get("pk", None)
        if (self.action == "partial_update" or self.action == "update") and self.request.user.role != UserTypes.GENERAL_MANAGER and int(user_id) == self.request.user.id:
            return [IsAuthenticated(), ]
        return [IsAuthenticated(),IsGeneralManager()]

    @action(detail=False, methods=["POST"], name="revoke_auth_token", permission_classes=[IsAuthenticated])
    def logout(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({'message': 'User Logged out successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], name="current_user")
    def me(self, request):
        serializer = self.get_serializer_class()
        user = get_object_or_404(User,id=self.request.user.id)
        return Response({ "user" : serializer(user).data})
