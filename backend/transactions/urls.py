from django.urls import path, include
from rest_framework import routers
from transactions.views import TransactionView

router = routers.DefaultRouter()
router.register(r"", TransactionView)

urlpatterns = [
    path("", include(router.urls)),
]