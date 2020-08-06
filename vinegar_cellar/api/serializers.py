from rest_framework import serializers

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation

class BarrelSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarrelSet
        fields = ('id', 'year')


class BarrelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barrel
        fields = ('id', 'barrel_set', 'wood_type', 'capability')


class OperationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationType
        fields = ('name', 'schema')


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('id', 'type', 'barrel', 'date', 'values')
