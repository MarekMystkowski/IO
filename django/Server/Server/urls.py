"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from WebNotifier.views import add_page, edit_page, index, add_device, edit_device
from WebNotifier.user.views import index as login
from WebNotifier.user.views import user_logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('WebNotifier.api.urls')),
    url(r'^add_page/', add_page),     # techniczny dla wtyczki
    url(r'^edit_page/', edit_page),   # do wprowadzenie pierwszych danych
    url(r'^add_device/', add_device), # techniczny dla odświerzaczki
    url(r'^edit_device/', edit_device),  # do wprowadzenie pierwszych danych
    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^logout/$', user_logout)
]
