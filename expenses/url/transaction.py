from django.conf.urls import patterns, url, include
from expenses.url.account import account_router, payment_type_router
from expenses.views import TransactionViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


transaction_router = routers.NestedSimpleRouter(account_router, r'account', lookup='account')
transaction_router.register(r'transaction', TransactionViewSet, base_name='transaction')

transaction_pt_router = routers.NestedSimpleRouter(payment_type_router, r'payment_type', lookup='payment_type')
transaction_pt_router.register(r'transaction', TransactionViewSet, base_name='transaction')

urlpatterns = patterns('',
                       url(r'^', include(transaction_router.urls)),
                       url(r'^', include(transaction_pt_router.urls)),
                       )