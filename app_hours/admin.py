from django.contrib import admin

from .models import WorkPlaces, WorkingHours

# Register your models here.
admin.site.register(WorkPlaces)
admin.site.register(WorkingHours)
