from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action, api_view, permission_classes
from users.models import User, UserVerification, AccountBalance
from users.serializers import UserSerializer
from users.utilities import UserTypes, send_otp_to_phone, verify_otp
from users.permissions import *
from fcm_django.models import FCMDevice

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class UserRetrieveUpdateListView(
    viewsets.ModelViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'pk'

    def create(self, request, *args,**kwargs):
        response = super().create(request, *args,**kwargs)

        try:
            if not self.request.user.is_authenticated:
                request_id = send_otp_to_phone(request.data["phone"])
                usr_verification, created = UserVerification.objects.get_or_create(user=User.objects.get(id=response.data["id"]))
                usr_verification.request_id = request_id
                usr_verification.save()
        except Exception as e:
            logger.info("=================== otp sending failed=========================    ", e)
        return response

    @action(detail=False, methods=["POST"], name="current_user")
    def landlord(self, request, *args,**kwargs):
        request.data["role"] = UserTypes.LANDLORD
        response = super().create(request, *args,**kwargs)

        try:
            if not self.request.user.is_authenticated:
                request_id = send_otp_to_phone(request.data["phone"])
                usr_verification, created = UserVerification.objects.get_or_create(user=User.objects.get(id=response.data["id"]))
                usr_verification.request_id = request_id
                usr_verification.save()
        except Exception as e:
            logger.info("=================== otp sending failed =========================", e)
        return response


    @action(detail=True, methods=["POST"], name="current_user")
    def change_password(self, request, *args,**kwargs):
        user = self.get_object()
        if not user.check_password(self.request.data["oldPassword"]):
            return Response({"message": "password mismatch"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(self.request.data["newPassword"])
        user.save()

        return Response({"message": "successfully changed password"})

    @action(detail=False, methods=["POST"], name="current_user")
    def forgot_password(self, request, *args,**kwargs):
        user = User.objects.get(phone=self.request.data["phone_number"])
 
        user.set_password(self.request.data["new_password"])
        user.save()

        return Response({"message": "successfully changed password"})


    def get_permissions(self):
        if self.action == "landlord" or self.action == "forgot_password":
            return [AllowAny()]
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

    @action(detail=False, methods=["POST"], name="current_user")
    def fb_registration_token(self, request, pk=None):
        obj = request.user
        token = request.data.get("token")
        obj.fb_registration_token = token
        obj.save()
        data, _ = FCMDevice.objects.get_or_create(registration_id=token, type="android")
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    code = request.data["code"]
    try:
        verify_otp(user_ver.user.phone, code)
        user.is_verified = True 
        user.save()
        logger.info("============ deleting otp record ===========")
        user.otp_status.all().delete()
        return Response({"message": "Phone number verified!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "message": "Otp verification failed",}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):
    if "phone" not in request.data:
        return Response({"message" : "Phone number is required" }, status=status.HTTP_400_BAD_REQUEST)

    phone = request.data["phone"]
    
    try:
        user = User.objects.get(phone=phone)
        if user.is_verified:
            logger.info("============== delete otp record if any because it is already verified =================")
            user.otp_status.delete()
            return Response({"message" : "User is Already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        request_id = send_otp_to_phone(phone)
    except Exception as e:
        logger.info("================= resend verification ======= ", e)
        return Response({"message": "Unable to send verification code.", "error": e }, status=status.HTTP_400_BAD_REQUEST)
    
    user_verification, created = UserVerification.objects.get_or_create(user__phone=phone)
    user_verification.request_id = request_id
    user_verification.save()

    return Response({"message": "OTP resent"}, status=status.HTTP_200_OK)


class TenantAuthRoute(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        user = User.objects.filter(phone=request.data["username"])
        if user.exists() and user.first().check_password(request.data["password"]) and not user.first().is_active:
            return Response({"message": "Your account is under verification"}, status=status.HTTP_412_PRECONDITION_FAILED)


        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_verified:
            return Response({"message": "Phone number is not verified"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if user.role != UserTypes.TENANT:
            return Response({"message": "invalid login route"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user,)
        usr_data = UserSerializer(user).data
        usr_data["token"] = token.key

        return Response({
            'user': usr_data 
        }, status=status.HTTP_200_OK)


class LandlordAuthRoute(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        user = User.objects.filter(phone=request.data["username"])
        if user.exists() and user.first().check_password(request.data["password"]) and not user.first().is_active:
            return Response({"message": "Your account is under verification"}, status=status.HTTP_412_PRECONDITION_FAILED)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        if not user.is_verified:
            return Response({"message": "Phone number is not verified"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if user.role != UserTypes.LANDLORD:
            return Response({"message": "invalid login route"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user,)
        usr_data = UserSerializer(user).data
        usr_data["token"] = token.key

        account_balance = AccountBalance.objects.get_or_create(
            user=user,
        )        

        return Response({
            'user': usr_data 
        }, status=status.HTTP_200_OK)

class AdminAuthRoute(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if user.role not in [UserTypes.GENERAL_MANAGER, UserTypes.LISTING_MANAGER, UserTypes.FINANCIAL_MANAGER]:
            return Response({"message": "invalid login route"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user,)
        usr_data = UserSerializer(user).data
        usr_data["token"] = token.key
        
        return Response({
            'user': usr_data 
        }, status=status.HTTP_200_OK)
