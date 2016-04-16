from django.contrib import admin
from WebNotifier import  models

@admin.register(models.Appliances, models.PageToObserve, models.RegisteredChanges, models.UserProfile)
class Model(admin.ModelAdmin): pass