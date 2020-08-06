from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (BarrelSetViewSet, BarrelViewSet,
                    OperationTypeViewSet, OperationViewSet)

router = DefaultRouter()
router.register(r'barrel_sets', BarrelSetViewSet, basename='barrel_sets')
router.register(r'barrels', BarrelViewSet, basename='barrels')
router.register(r'operation_type', OperationTypeViewSet, basename='operation_type')
router.register(r'operations', OperationViewSet, basename='operations')
urlpatterns = router.urls
