from WebNotifier.log.views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', register),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^$', index),
]
