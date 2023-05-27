from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from users.models import User, UserVerification
from users.serializers import UserSerializer
from users.utilities import UserTypes, send_otp_to_phone, verify_otp
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

    def create(self, request, *args,**kwargs):
        response = super().create(request, *args,**kwargs)
        try:
            request_id = send_otp_to_phone(request.data["phone"])
            usr_verification, created = UserVerification.objects.get_or_create(user=User.objects.get(id=response.data["id"]))
            usr_verification.request_id = request_id
            usr_verification.save()
        except Exception as e:
            print("===================otp sending failed=========================    ", e)
        return response

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

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_otp_view(request):
    if "phone" not in request.data:
        return Response({"message": "Phone number is required!"}, status=status.HTTP_400_BAD_REQUEST)
    if "code" not in request.data:
        return Response({"message": "Verification code is required!"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(phone=request.data["phone"])
    user_ver, created = UserVerification.objects.get_or_create(user=user)
    code = request.data["code"] # code sent from the otp provider!
    try:
        verify_otp(user_ver.request_id, code) # to verify we need the otp and the request_id [this could be specific to vonage]
        user.is_verified = True 
        user.save()
        # TODO: delete otp verification
        return Response({"message": "Phone number verified!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "message": "Otp verification failed" }, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):
    if "phone" not in request.data:
        return Response({"message" : "Phone number is required" }, status=status.HTTP_400_BAD_REQUEST)

    phone = request.data["phone"]
    
    try:
        request_id = send_otp_to_phone(phone)
    except Exception as e:
        print("================= resend verification ======= ", e)
        return Response({"message": "Unable to send verification code.", "error": e }, status=status.HTTP_400_BAD_REQUEST)
    
    user_verification, created = UserVerification.objects.get_or_create(user__phone=phone)
    user_verification.request_id = request_id
    user_verification.save()

    return Response({"message": "OTP resent"}, status=status.HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user,)
        usr_data = UserSerializer(user).data
        usr_data["token"] = token.key
        return Response({
            'user': usr_data 
        }, status=status.HTTP_200_OK)
