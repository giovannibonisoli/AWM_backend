from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.forms import model_to_dict

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation
from .serializers import (BarrelSetSerializer, BarrelSerializer,
                          OperationTypeSerializer, OperationSerializer)


class BarrelSetViewSet(viewsets.ModelViewSet):
    serializer_class = BarrelSetSerializer
    queryset = BarrelSet.objects.all()


class BarrelViewSet(mixins.ListModelMixin,
                    mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = BarrelSerializer
    queryset = Barrel.objects.all()

    def create(self, request):
        res = self.queryset.filter(barrel_set=request.data['barrel_set']).last()
        item = request.data
        if res is None:
            item['id'] = ('BAR' + str(request.data['barrel_set']).zfill(2) +
                          '01')
        else:
            item['id'] = ('BAR' + str(request.data['barrel_set']).zfill(2) +
                          str(int(res.id[5:]) + 1).zfill(2))

        serializer = self.get_serializer(data=item)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=model_to_dict(instance),
                        status=status.HTTP_201_CREATED)

    @action(detail=False, url_path='set/(?P<pk>[^/.]+)')
    def filtered_list(self, request, pk):
        res = Barrel.objects.filter(barrel_set=pk)
        serializer = self.get_serializer(res, many=True)
        return Response(serializer.data)


class OperationTypeViewSet(viewsets.ModelViewSet):
    serializer_class = OperationTypeSerializer
    queryset = OperationType.objects.all()


class OperationViewSet(viewsets.GenericViewSet):
    serializer_class = OperationSerializer
    queryset = Operation.objects.all()

    @action(detail=False, methods=['get', 'post'], url_path='(?P<name>[a-z]+)')
    def operation_list(self, request, name):
        if request.method == 'GET':
            res = self.queryset.filter(type=name)
            serializer = self.get_serializer(res, many=True)
            return Response(data=serializer.data)

        else:
            if name != request.data['type']:
                return Response(data={'detail': ('Only "' + name + '" are ' +
                                      'accepted at this endpoint')},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(data=model_to_dict(instance),
                            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get', 'put', 'delete'],
            url_path='(?P<name>[a-z]+)/(?P<pk>[^/.]+)')
    def operation_instance(self, request, name, pk=None):
        set = self.queryset.filter(type=name)
        try:
            operation = set.get(pk=pk)
        except Operation.DoesNotExist:
            return Response(data={'detail': 'Not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            serializer = self.get_serializer(operation, many=False)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = self.get_serializer(operation, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            return Response(model_to_dict(instance))

        elif request.method == 'DELETE':
            operation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
