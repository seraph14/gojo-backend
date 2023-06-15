from django.urls import path, include
from rest_framework import routers
from transactions.views import TransactionView, verify_payment_status

router = routers.DefaultRouter()
router.register(r"", TransactionView)

urlpatterns = [
    path("verify_payment_status/", verify_payment_status),
    path("", include(router.urls)),
]