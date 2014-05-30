import os 
import sys 
app_root = os.path.dirname(__file__) 
sys.path.insert(0,os.path.join(app_root,'itimewall')) 

import django.core.handlers.wsgi 

import sae 

os.environ['DJANGO_SETTINGS_MODULE'] = 'itimewall.settings' 

application = sae.create_wsgi_app(django.core.handlers.wsgi.WSGIHandler()) 