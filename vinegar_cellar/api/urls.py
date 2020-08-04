from rest_framework.routers import DefaultRouter

from .views import BarrelSetViewSet

router = DefaultRouter()
router.register(r'barrel_set', BarrelSetViewSet, basename='barrel_set')
urlpatterns = router.urls
