from rest_framework import viewsets, mixins
from rest_framework.decorators import action, parser_classes
from rest_framework.response import Response
from django.forms import model_to_dict

from rest_framework.parsers import JSONParser

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

class OperationModelSet(viewsets.ModelViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

class OperationViewSet(viewsets.GenericViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    #@parser_classes([JSONParser])
    @action(detail=False, methods=['get','post'], url_path='(?P<name>[a-z]+)')
    def operation_list(self, request, name):
        if request.method == 'GET':
            res = self.queryset.filter(type=name)
            serializer = self.get_serializer(res, many=True)
            return Response(serializer.data)
        else:
            data = {}
            for k in request.data.keys():
                if k != 'csrfmiddlewaretoken':
                    data[k] = request.data[k]
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(model_to_dict(instance))

    @action(detail=False, methods=['get','put','delete'], url_path='(?P<name>[a-z]+)/(?P<pk>[^/.]+)')
    def operation_instance(self, request, name, pk=None):
        res = self.queryset.filter(type=name)
        try:
            res = res.get(pk=pk)
            serializer = self.get_serializer(res, many=False)
            return Response(serializer.data)
        except Operation.DoesNotExist:
            return Response({'detail': 'Not found'})
