from rest_framework import viewsets
from rest_framework.decorators import action

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation
from .serializers import (BarrelSetSerializer, BarrelSerializer,
                            OperationTypeSerializer, OperationSerializer)

class BarrelSetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BarrelSetSerializer
    queryset = BarrelSet.objects.all()


class BarrelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = BarrelSerializer
    queryset = Barrel.objects.all()


class OperationTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OperationTypeSerializer
    queryset = OperationType.objects.all()


class OperationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()
