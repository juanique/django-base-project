from django.conf.urls.defaults import patterns, include, url
from api.resources import Api
from jsonrpc import jsonrpc_site
import api.rpc

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
api = Api()

urlpatterns = patterns('',
        (r'^api/services/', include('api.urls')),
        (r'^api/rpc-browse/$', 'jsonrpc.views.browse'),
        (r'^api/rpc/$', jsonrpc_site.dispatch),
        (r'^api/',include(api.urls)),

    # Examples:
    # url(r'^$', 'adedo.views.home', name='home'),
    # url(r'^adedo/', include('adedo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
