from rest_framework import viewsets
from transactions.serializers import TransactionSerializer
from transactions.models import Transaction

class TransactionView(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()