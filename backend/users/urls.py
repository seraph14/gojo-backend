from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from users.views import (
    UserRetrieveUpdateListView, 
    logout, 
    verify_otp_view, 
    resend_otp,
    AdminAuthRoute,
    TenantAuthRoute,
    LandlordAuthRoute,
)
router = routers.DefaultRouter()
router.register(r"", UserRetrieveUpdateListView)

urlpatterns = [
    path("logout/", logout, name="invalidate_token"),
    path("admin_login/", AdminAuthRoute.as_view(), name="obtain_admin_token"),
    path("tenant_login/", TenantAuthRoute.as_view(), name="obtain_tenant_token"),
    path("landlord_login/", LandlordAuthRoute.as_view(), name="obtain_landlord_token"),
    path("verify_otp/", verify_otp_view, name="verify_otp"),
    path("resend_otp/", resend_otp, name="resend_otp"),
    path("",include(router.urls) , name="users"),
]