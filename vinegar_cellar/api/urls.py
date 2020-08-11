from rest_framework.routers import DefaultRouter


from .views import (BarrelSetViewSet, BarrelViewSet, BarrelModelSet,
                    OperationTypeViewSet, OperationViewSet, OperationModelSet)

router = DefaultRouter()
router.register(r'barrel_set', BarrelSetViewSet, basename='barrel_set')
router.register(r'barrel', BarrelViewSet, basename='barrel')
router.register(r'barmodel', BarrelModelSet, basename='barmodel')
router.register(r'operation_type', OperationTypeViewSet,
                basename='operation_type')
router.register(r'operation', OperationViewSet, basename='operation')
router.register(r'opmodel', OperationModelSet, basename='opmodel')
urlpatterns = router.urls
