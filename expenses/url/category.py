from django.conf.urls import patterns, url, include
from expenses.views import CategoryViewSet, SubCategoryViewSet
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

category_router = routers.SimpleRouter()
category_router.register(r'category', CategoryViewSet, base_name='category')

all_sub_category_router = routers.SimpleRouter()
all_sub_category_router.register(r'sub_category', SubCategoryViewSet, base_name='sub_category')

sub_category_router = routers.NestedSimpleRouter(category_router, r'category', lookup='category')
sub_category_router.register(r'sub_category', SubCategoryViewSet, base_name='sub_category')

urlpatterns = patterns('',
                       url(r'^', include(category_router.urls)),
                       url(r'^', include(sub_category_router.urls)),
                       url(r'^', include(all_sub_category_router.urls)),
                       )