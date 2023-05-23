from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserRetrieveUpdateListView, logout, CustomAuthToken

router = routers.DefaultRouter()
router.register(r"", UserRetrieveUpdateListView)

urlpatterns = [
    path("logout/", logout, name="invalidate_token"),
    path("login/", CustomAuthToken.as_view(), name="obtain_token"),
    path("",include(router.urls) , name="users"),
]