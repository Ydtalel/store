from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, TypeViewSet, PriceViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'types', TypeViewSet)
router.register(r'prices', PriceViewSet)

urlpatterns = router.urls
