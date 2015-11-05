from expenses.models import *
from expenses.serializers import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = AccountSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()
        else:
            accounts = Account.objects.filter(user=self.request.user)
            for account in accounts:
                calculate_balance(account)
            return accounts


class PaymentTypeViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = PaymentTypeSerializer

    def get_queryset(self):
        if 'account_pk' in self.kwargs:
            return PaymentType.objects.filter(account=self.kwargs['account_pk'])
        else:
            return PaymentType.objects.filter(user=self.request.user)
