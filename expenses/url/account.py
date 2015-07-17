from django.conf.urls import patterns, url, include
from expenses.views import AccountViewSet, PaymentTypeViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


account_router = routers.SimpleRouter()
account_router.register(r'account', AccountViewSet, base_name='account')

payment_type_router = routers.NestedSimpleRouter(account_router, r'account', lookup='account')
payment_type_router.register(r'payment_type', PaymentTypeViewSet, base_name='payment_type')

urlpatterns = patterns('',
                       url(r'^', include(account_router.urls)),
                       url(r'^', include(payment_type_router.urls)),
                       )