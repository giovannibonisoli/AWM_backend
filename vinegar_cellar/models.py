from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class BarrelSet(models.Model):
    year = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])

class Barrel(models.Model):
    barrel_set = models.ForeignKey(BarrelSet, on_delete=models.CASCADE)
    wood_type = models.CharField(max_length=50)
    capability = models.PositiveIntegerField()
