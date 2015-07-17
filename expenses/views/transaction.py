from expenses.models import *
from expenses.serializers import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication


class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = TransactionSerializer

    def get_queryset(self):
        lookup = dict()
        if 'year' in self.request.query_params:
            lookup['tran_date__year'] = self.request.query_params['year']
            if 'month' in self.request.query_params:
                lookup['tran_date__month'] = self.request.query_params['month']
        if 'payment_type_pk' in self.kwargs:
            lookup['payment_type'] = self.kwargs['payment_type_pk']
        elif 'account_pk' in self.kwargs:
            lookup['account_pk'] = self.kwargs['account_pk']
        else:
            lookup['user'] = self.request.user
        return Transaction.objects.filter(**lookup)