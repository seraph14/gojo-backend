import uuid
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from transactions.serializers import TransactionSerializer, TransactionTenantSerializer, TransactionLandlordSerializer
from transactions.models import Transaction
from django_filters import rest_framework as filters
from rest_framework.decorators import action, api_view, permission_classes
from chapa.views import ChapaUtils
from transactions.utils import TRANSACTION_STATUS, TRANSACTION_TYPE
from transactions.filters import TransactionFilter
from users.permissions import CanStartTransaction, UserTypes
from django.db.models import Q
from users.serializers import AccountBalanceSerializer
from users.models import AccountBalance

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionTenantSerializer
    queryset = Transaction.objects.all().prefetch_related("rent_detail")
    lookup_field = 'pk'
    permission_classes = [ AllowAny ]

    # Filters
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionFilter

    def list(self, request):
        if self.request.user.role == UserTypes.LANDLORD:
            data = self.get_queryset().filter(Q(receiver=self.request.user) | Q(sender=self.request.user))
            return Response({"balance": AccountBalanceSerializer(AccountBalance.objects.get(user=self.request.user)).data, "transactions" : TransactionLandlordSerializer(data, many=True).data})
        if self.request.user.role == UserTypes.TENANT:
            data = self.get_queryset().filter(Q(sender=self.request.user))
            return Response(TransactionTenantSerializer(data, many=True).data)
        
        return super().list(request)
    
    def create(self, request):
        if self.request.user.role == UserTypes.LANDLORD:
            return Response(TransactionSerializer(Transaction.objects.create(
                sender=self.request.user,
                amount=self.request.data["amount"],
                type=TRANSACTION_TYPE.WITHDRAWAL
            )).data, status=status.HTTP_200_OK)
        return super().create(request)    

    @action(detail=False, methods=["POST"], name="chapa_webhook", )
    def verify_payment_status(self, request, pk=None):
        # TODO: tj
        data = request.data

        transaction = Transaction.objects.get(tx_ref=(data["tx_ref"]))
        if data["status"] == "success":
            transaction.status = TRANSACTION_STATUS.PAID
            transaction.save()
        else:
            print("======================= payment status is not success =======================")
        return Response(data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=["GET"], name="chapa_webhook")
    def chapa_checkout_url(self, request, pk=None):
        transaction = Transaction.objects.get(id=int(pk))
        if transaction.status == TRANSACTION_STATUS.PAID:
            return Response({"message": "Payment already made!"})
        response = ChapaUtils.initialize(transaction.amount, "se.natnael.abay@gmail.com", transaction.sender.first_name, transaction.sender.last_name, str(transaction.tx_ref))
        if response["status"] == "success":
            transaction.checkout_url = response["data"]["checkout_url"]
            transaction.save()
            return Response(response, status=status.HTTP_200_OK)
        elif response["status"] == "failed" \
            and response["message"] == "Transaction reference has been used before" \
            and transaction.checkout_url and transaction.status != [TRANSACTION_STATUS.PAID, TRANSACTION_STATUS.WITHDRAWAL_REQUEST_DENIED]:
            return Response({"data" : {"checkout_url": transaction.checkout_url}}, status=status.HTTP_200_OK)
        
        elif response["status"] == "failed" \
            and response["message"] == "Transaction reference has been used before" and transaction.status == TRANSACTION_STATUS.PENDING:
            transaction.tx_ref = uuid.uuid4()
            transaction.save()
            response = ChapaUtils.initialize(transaction.amount, "se.natnael.abay@gmail.com", 
                transaction.sender.first_name, 
                transaction.sender.last_name, 
                str(transaction.tx_ref)
            )
            return Response(response, status=status.HTTP_200_OK)
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["POST"], name="chapa_webhook", )
    def release_fund(self, request, pk=None):
        
        return Response(data, status=status.HTTP_200_OK)
    
