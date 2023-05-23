from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
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
                int(self.request.data.get("role", UserTypes.TENANT)) in [UserTypes.TENANT, UserTypes.LANDLORD]:
            return [AllowAny(),]
        if self.action == "create" and \
                int(self.request.data.get("role", None)) in [UserTypes.LISTING_MANAGER, UserTypes.FINANCIAL_MANAGER]:
            return [IsAuthenticated(), IsGeneralManager()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["GET"], name="current_user")
    def me(self, request):
        serializer = self.get_serializer_class()
        user = get_object_or_404(User,id=self.request.user.id)
        return Response({ "user" : serializer(user).data})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'User Logged out successfully'}, status=status.HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)
        usr_data = UserSerializer(user).data
        usr_data["token"] = token.key
        return Response({
            # 'token': token.key,
            'user': usr_data 
        }, status=status.HTTP_200_OK)

