from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = patterns('backend.views',
                       url(r'', include('expenses.url.account')),
                       url(r'', include('expenses.url.category')),
                       url(r'', include('expenses.url.transaction')),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('', url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'))
urlpatterns += patterns('', url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),)
urlpatterns = format_suffix_patterns(urlpatterns)