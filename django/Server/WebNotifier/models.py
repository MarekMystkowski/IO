# -*- coding: utf-8 -*-
from Tools.scripts.objgraph import def2file
from django.db import models
from django.contrib.auth.models import User


AccountTypes = (
    ('1', 'Basic'),
    ('3', 'Advanced'),
    ('5', 'Premium'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_of_registration = models.DateTimeField()
    account_type = models.CharField(max_length=20, choices=AccountTypes)

class Device(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(UserProfile)
    priority = models.IntegerField()

class Page(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    page_data = models.TextField()
    interval = models.IntegerField(default=60) # w sekundach
    login_url = models.TextField(default='')
    login_data = models.TextField(default='')
    recent_state = models.TextField(default='')
    active = models.BooleanField(default=True)

class Change(models.Model):
    page = models.ForeignKey(Page)
    date = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    result = models.TextField()
