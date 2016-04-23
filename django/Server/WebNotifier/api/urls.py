from django.conf.urls import url
from WebNotifier.api.views import *

urlpatterns = [
    url(r'^page_list/$', page_list),
]
