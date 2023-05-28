from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from transactions.serializers import TransactionSerializer, TransactionTenantSerializer
from transactions.models import Transaction
from django_filters import rest_framework as filters
from rest_framework.decorators import action, api_view, permission_classes
from chapa.views import ChapaUtils
from transactions.utils import TRANSACTION_STATUS
from transactions.filters import TransactionFilter
from users.permissions import CanStartTransaction


class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionTenantSerializer
    queryset = Transaction.objects.all().prefetch_related("rent_detail")
    lookup_field = 'pk'
    permission_classes = [ AllowAny ]

    # Filters
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionFilter

    @action(detail=True, methods=["POST"], name="chapa_webhook")
    def chapa_webhook(self, request, pk=None):
        transaction = Transaction.objects.get(id=int(pk))
        response = ChapaUtils.initialize(transaction.amount, "se.natnael.abay@gmail.com", transaction.sender.first_name, transaction.sender.last_name, str(transaction.tx_ref))
        if response["status"] == "success":
            return Response(response, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=["GET"], name="chapa_webhook")
    def chapa_checkout_url(self, request, pk=None):
        transaction = Transaction.objects.get(id=int(pk))
        response = ChapaUtils.initialize(transaction.amount, "se.natnael.abay@gmail.com", transaction.sender.first_name, transaction.sender.last_name, str(transaction.tx_ref))
        if response["status"] == "success":
            transaction.checkout_url = response["data"]["checkout_url"]
            transaction.save()
            return Response(response, status=status.HTTP_200_OK)
        elif response["status"] == "failed" \
            and response["message"] == "Transaction reference has been used before" \
            and transaction.checkout_url and transaction.status != [TRANSACTION_STATUS.PAID, TRANSACTION_STATUS.WITHDRAWAL_REQUEST_DENIED]:
            return Response({"data" : {"checkout_url": transaction.checkout_url}}, status=status.HTTP_200_OK)
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)