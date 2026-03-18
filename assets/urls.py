"""
Rutas para el app de activos (Assets).
"""

from rest_framework.routers import DefaultRouter
from assets.views.inmueble import InmuebleViewSet

router = DefaultRouter()
router.register(r'', InmuebleViewSet, basename='inmueble')

urlpatterns = router.urls
