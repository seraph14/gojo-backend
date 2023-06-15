import uuid
from decimal import Decimal
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from transactions.serializers import (
    TransactionSerializer,
    TransactionTenantSerializer,
    TransactionLandlordSerializer,
)
from transactions.models import Transaction
from django_filters import rest_framework as filters
from rest_framework.decorators import action, api_view, permission_classes
from chapa.views import ChapaUtils
from transactions.utils import (
    TRANSACTION_STATUS,
    TRANSACTION_TYPE,
    validate_withdrawal_request,
)
from transactions.filters import TransactionFilter
from users.permissions import CanStartTransaction, UserTypes
from django.db.models import Q
from users.serializers import AccountBalanceSerializer
from users.models import AccountBalance
from backend.utilities import payment_arrived


class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionTenantSerializer
    queryset = Transaction.objects.all().prefetch_related("rent_detail")
    lookup_field = "pk"
    permission_classes = [AllowAny]

    # Filters
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = TransactionFilter

    def list(self, request):
        if self.request.user.is_authenticated:
            if self.request.user.role == UserTypes.LANDLORD:
                data = self.get_queryset().filter(
                    Q(receiver=self.request.user) | Q(sender=self.request.user)
                )
                return Response(
                    {
                        "balance": AccountBalanceSerializer(
                            AccountBalance.objects.get(user=self.request.user)
                        ).data,
                        "transactions": TransactionLandlordSerializer(
                            data, many=True
                        ).data,
                    }
                )
            if self.request.user.role == UserTypes.TENANT:
                data = self.get_queryset().filter(Q(sender=self.request.user))
                # return Response(TransactionTenantSerializer(data, many=True).data)

        return super().list(request)

    def get_queryset(self):
        queryset = Transaction.objects.all().prefetch_related("rent_detail")
        if self.request.user.is_authenticated:
            if self.request.user.role in [
                UserTypes.FINANCIAL_MANAGER,
                UserTypes.GENERAL_MANAGER,
            ]:
                queryset = queryset.filter(type=TRANSACTION_TYPE.WITHDRAWAL)

        return queryset

    # def create(self, request):
    #     if self.request.user.role == UserTypes.LANDLORD:
    #         return Response(TransactionSerializer(Transaction.objects.create(
    #             sender=self.request.user,
    #             amount=self.request.data["amount"],
    #             type=TRANSACTION_TYPE.WITHDRAWAL
    #         )).data, status=status.HTTP_200_OK)
    #     return super().create(request)

    @action(detail=True, methods=["GET"], name="chapa_webhook")
    def chapa_checkout_url(self, request, pk=None):
        transaction = Transaction.objects.get(id=int(pk))
        if transaction.status == TRANSACTION_STATUS.PAID:
            return Response({"message": "Payment already made!"})
        response = ChapaUtils.initialize(
            transaction.amount,
            "se.natnael.abay@gmail.com",
            transaction.sender.first_name,
            transaction.sender.last_name,
            str(transaction.tx_ref),
        )
        if response["status"] == "success":
            transaction.checkout_url = response["data"]["checkout_url"]
            transaction.save()
            return Response(response, status=status.HTTP_200_OK)
        elif (
            response["status"] == "failed"
            and response["message"] == "Transaction reference has been used before"
            and transaction.checkout_url
            and transaction.status
            != [TRANSACTION_STATUS.PAID, TRANSACTION_STATUS.WITHDRAWAL_REQUEST_DENIED]
        ):
            return Response(
                {"data": {"checkout_url": transaction.checkout_url}},
                status=status.HTTP_200_OK,
            )

        elif (
            response["status"] == "failed"
            and response["message"] == "Transaction reference has been used before"
            and transaction.status == TRANSACTION_STATUS.PENDING
        ):
            transaction.tx_ref = uuid.uuid4()
            transaction.save()
            response = ChapaUtils.initialize(
                transaction.amount,
                "se.natnael.abay@gmail.com",
                transaction.sender.first_name,
                transaction.sender.last_name,
                str(transaction.tx_ref),
            )
            return Response(response, status=status.HTTP_200_OK)

        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=["POST"],
        name="release_fund",
    )
    def release_fund(self, request, pk=None):
        from backend.utilities import withdrawal_request_approved

        # if not validate_withdrawal_request(withdrawal_request):
        #     return Response({"message": "Unable to approve request!"}, status=status.HTTP_400_BAD_REQUEST)

        # response = ChapaUtils.transfer(
        #     withdrawal_request
        # )
        # if response["status"] == "success":
        # return Response(response, status=status.HTTP_200_OK)
        # return Response(response, status=status.HTTP_400_BAD_REQUEST)

        account_balance = AccountBalance.objects.get(user=self.get_object().receiver)

        transaction = self.get_object()
        transaction.status = TRANSACTION_STATUS.WITHDRAWAL_REQUEST_APPROVED
        transaction.save()

        current_balance = account_balance.amount
        account_balance.amount = current_balance - transaction.amount
        account_balance.save()

        try:
            withdrawal_request_approved(
                self.get_object().receiver.fb_registration_token,
            )
        except:
            pass
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        name="request_withdraw",
    )
    def withdraw(self, request, pk=None):
        balance = AccountBalance.objects.get(user=self.request.user)
        if balance.amount < self.request.data.get("amount", 0):
            return Response(
                {"message": "Insufficient balance!"}, status=status.HTTP_400_BAD_REQUEST
            )

        transaction = Transaction.objects.create(
            receiver=self.request.user,
            amount=Decimal(self.request.data["amount"]),
            status=TRANSACTION_STATUS.PENDING,
            type=TRANSACTION_TYPE.WITHDRAWAL,
            bank_detail=self.request.data["bank"],
        )

        balance.amount -= Decimal(self.request.data["amount"])
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET"],
        name="transaction_report",
    )
    def report(self, request, pk=None):
        from django.db.models import Sum

        released_amount = Transaction.objects.filter(
            status=TRANSACTION_STATUS.WITHDRAWAL_REQUEST_APPROVED, type=TRANSACTION_TYPE.WITHDRAWAL
        ).aggregate(total=Sum("amount"))["total"]

        total_cash_flow = Transaction.objects.filter(
            status=TRANSACTION_STATUS.PAID, type=TRANSACTION_TYPE.RENT_PAYMENT
        ).aggregate(total=Sum("amount"))["total"]

        if total_cash_flow is None:
            total_cash_flow = 0
        if released_amount is None:
            released_amount = 0

        current_balance = total_cash_flow - released_amount

        return Response(
            {
                "cash_flow": total_cash_flow,
                "released_amount": released_amount,
                "current_balance": current_balance,
            },
            status=status.HTTP_200_OK,
        )


@api_view(["POST"])
def verify_payment_status(request):
    data = request.data

    transaction = Transaction.objects.get(tx_ref=(data["tx_ref"]))
    if data["status"] == "success":
        transaction.status = TRANSACTION_STATUS.PAID
        transaction.save()
        payment_arrived(transaction.rent_detail.property.owner.fb_registration_token)
    else:
        print(
            "======================= payment status is not success ======================="
        )
    return Response(data, status=status.HTTP_200_OK)
