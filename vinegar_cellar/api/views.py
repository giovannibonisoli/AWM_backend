from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation
from .serializers import (BarrelSetSerializer, BarrelSerializer,
                            OperationTypeSerializer, OperationSerializer)

class BarrelSetViewSet(viewsets.ModelViewSet):
    serializer_class = BarrelSetSerializer
    queryset = BarrelSet.objects.all()


class BarrelViewSet(viewsets.ModelViewSet):
    serializer_class = BarrelSerializer
    queryset = Barrel.objects.all()


class OperationTypeViewSet(viewsets.ModelViewSet):
    serializer_class = OperationTypeSerializer
    queryset = OperationType.objects.all()


#class OperationViewSet(viewsets.ModelViewSet):
class OperationViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):

    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    @action(detail=False, url_path='(?P<name>[a-z]+)')
    def get_operations_by_type(self, request, name):
        res = self.queryset.filter(type=name)
        page = self.paginate_queryset(res)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(res, many=True)
        return Response(serializer.data)
