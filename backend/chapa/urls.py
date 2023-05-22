from django.urls import path, include
from rest_framework import routers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# TODO: REF: this is to test endpoint setup only! remove ASAP
 
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(self, request, *args, **kwargs):
    request.user.auth_token.delete()
    return Response({'message': 'User Logged out successfully'}, status=status.HTTP_200_OK)


urlpatterns = [
    path("chatting/", logout, name="test_chapa_endpoint"),
]