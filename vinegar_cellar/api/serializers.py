from rest_framework import serializers

from vinegar_cellar.models import BarrelSet, Barrel

class BarrelSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarrelSet
        fields = ('id', 'year')


class BarrelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrel
        fields = ('id', 'barrel_set', 'wood_type', 'capability')
