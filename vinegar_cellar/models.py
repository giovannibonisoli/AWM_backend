from django.db import models
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class BarrelSet(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    year = models.IntegerField(('year'), validators=[MinValueValidator(1984),
                                                     max_value_current_year])


class Barrel(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    barrel_set = models.ForeignKey(BarrelSet, on_delete=models.CASCADE)
    wood_type = models.CharField(max_length=50)
    capability = models.PositiveIntegerField()


class OperationType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    schema = JSONField(default=[])


class Operation(models.Model):
    type = models.ForeignKey(OperationType, on_delete=models.CASCADE)
    barrel = models.ForeignKey(Barrel, on_delete=models.CASCADE)
    date = models.DateField()
    values = JSONField(default=[])
