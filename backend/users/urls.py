from django.urls import path, include
from users.views import UserRetrieveUpdateListView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", UserRetrieveUpdateListView)
urlpatterns = [
    path("",include(router.urls) , name="users"),
]