from WebNotifier.log.views import register, user_login, user_logout, index
from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', register),
    url(r'^login/$', user_login),
    url(r'^logout/$', user_logout),
    url(r'^$', index),
]
