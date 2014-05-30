from django.conf.urls.defaults import *
from itimewall.views import ihomepage, rdrct, newspage
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^home/$', ihomepage),
    (r'^$', rdrct),
    (r'^news/$', newspage),
    # Example:
    # (r'^itimewall/', include('itimewall.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
