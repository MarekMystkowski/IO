# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_of_registration = models.DateTimeField()
    account_type = models.IntegerField()


class Appliances(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(UserProfile)
    priority = models.IntegerField()

class PageToObserve(models.Model):
    user = models.ForeignKey(UserProfile)
    url_to_login = models.TextField()
    login_data = models.TextField()
    data_to_observer = models.TextField()
    last_page_content = models.TextField()
    currently_observed = models.BooleanField(default=True)
    refresh_period = models.TimeField()

class RegisteredChanges(models.Model):
    page = models.ForeignKey(PageToObserve)
    date = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    result = models.TextField()
