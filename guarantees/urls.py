"""
Rutas para el app de Garantías de Adcon.
"""

from rest_framework.routers import DefaultRouter
from guarantees.views.garantias_views import PenaViewSet, FianzaViewSet

router = DefaultRouter()
router.register(r'penas', PenaViewSet, basename='pena')
router.register(r'fianzas', FianzaViewSet, basename='fianza')

urlpatterns = router.urls
