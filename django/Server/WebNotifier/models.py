# -*- coding: utf-8 -*-
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
    active_device = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.user.username


class Device(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=50)
    user = models.ForeignKey(UserProfile)
    priority = models.IntegerField()
    active = models.BooleanField(default=False)
    buffer = models.TextField(default='')

    def __str__(self):
        return self.name


class Page(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    page_url = models.TextField(default='')
    title = models.TextField(default='')
    page_data = models.TextField(default='')
    interval = models.IntegerField(default=60) # w sekundach
    login_url = models.TextField(default='', blank=True)
    login_data = models.TextField(default='')
    recent_state = models.TextField(default='', blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title + ' (' + self.page_url + ')'


class Change(models.Model):
    page = models.ForeignKey(Page)
    date = models.DateTimeField()
    displayed = models.BooleanField(default=False)
    old_value = models.TextField(default='', blank=True)
    new_value = models.TextField(default='', blank=True)

    def __str__(self):
        return self.page.page_url + ': ' + self.old_value + ' -> ' + self.new_value