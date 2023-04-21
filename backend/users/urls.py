from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from users.views import UserRetrieveUpdateListView

router = routers.DefaultRouter()
router.register(r"", UserRetrieveUpdateListView)

urlpatterns = [
    path("login/", obtain_auth_token, name="obtain_token"),
    path("",include(router.urls) , name="users"),
]