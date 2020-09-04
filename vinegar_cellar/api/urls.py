from rest_framework.routers import DefaultRouter


from .views import (BarrelSetViewSet, BarrelViewSet, OperationTypeViewSet,
                    OperationViewSet)

router = DefaultRouter()
router.register(r'barrel_set', BarrelSetViewSet, basename='barrel_set')
router.register(r'barrel', BarrelViewSet, basename='barrel')
router.register(r'operation_type', OperationTypeViewSet,
                basename='operation_type')
router.register(r'operation', OperationViewSet, basename='operation')
urlpatterns = router.urls
