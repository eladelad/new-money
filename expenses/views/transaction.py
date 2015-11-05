from expenses.models import *
from expenses.serializers import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
import logging

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
            lookup['account_id'] = self.kwargs['account_pk']
        else:
            lookup['user'] = self.request.user
        return Transaction.objects.filter(**lookup)

    def create(self, request, *args, **kwargs):
        if 'payments_no' in self.request.DATA:
            credit_no = self.request.DATA['payments_no']
            amount = self.request.DATA['amount'] / credit_no
            if 'comment' in self.request.DATA: comment = self.request.DATA['comment']
            else: comment = ""
            for i in range(1, credit_no):
                data = request.DATA.copy()
                data['amount'] = amount
                data['comment'] = comment + ' i'
                serializer = self.get_serializer(data=data)
                if serializer.is_valid():
                    self.object = serializer.save()
                    headers = self.get_success_headers(serializer.data)
            return super(TransactionViewSet, self).create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        # from pprint import pprint
        # logging.basicConfig()
        # logger = logging.getLogger(__name__)
        # logger.error(amount)
        cur_transaction = Transaction.objects.get(pk=kwargs['pk'])
        amount = cur_transaction.amount

        if amount != request.DATA['amount']:
            account = PaymentType.objects.get(pk=request.DATA['payment_type']).account
            calculate_transaction(account, cur_transaction, True)
            account.save()
        return super(TransactionViewSet, self).update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(paid=False)