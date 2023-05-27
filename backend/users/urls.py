from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserRetrieveUpdateListView, logout, CustomAuthToken, verify_otp_view, resend_otp

router = routers.DefaultRouter()
router.register(r"", UserRetrieveUpdateListView)

urlpatterns = [
    path("logout/", logout, name="invalidate_token"),
    path("login/", CustomAuthToken.as_view(), name="obtain_token"),
    path("verify_otp/", verify_otp_view, name="verify_otp"),
    path("resend_otp/", resend_otp, name="resend_otp"),
    path("",include(router.urls) , name="users"),
]