# from expenses.models import *
from expenses.serializers import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from django.db.models import Q


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(Q(user=None) | Q(user=self.request.user)).distinct()


class SubCategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if 'category_pk' in self.kwargs:
            return SubCategory.objects.filter(Q(category=self.kwargs['category_pk']), Q(user=None) | Q(user=self.request.user)).distinct()
        else:
            return SubCategory.objects.filter(Q(user=None) | Q(user=self.request.user)).distinct()