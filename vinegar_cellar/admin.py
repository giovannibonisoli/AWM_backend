from django.contrib import admin
from .models import BarrelSet, Barrel, OperationType, Operation


admin.site.register(BarrelSet)
admin.site.register(Barrel)
admin.site.register(OperationType)
admin.site.register(Operation)
