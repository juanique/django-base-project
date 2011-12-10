from django.conf.urls.defaults import patterns, include, url
from views import authenticate

urlpatterns = patterns('',
        (r'^authenticate/$', authenticate)
)
