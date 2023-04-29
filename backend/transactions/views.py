from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from transactions.serializers import TransactionSerializer
from transactions.models import Transaction
from users.permissions import CanStartTransaction
class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated, CanStartTransaction]