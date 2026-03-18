"""
Rutas para el app de partes (Parties).
"""

from rest_framework.routers import DefaultRouter
from parties.views.parties_views import (
    PersonaFisicaViewSet, PersonaMoralViewSet, SucursalViewSet
)

router = DefaultRouter()
router.register(r'personas-fisicas', PersonaFisicaViewSet, basename='persona-fisica')
router.register(r'personas-morales', PersonaMoralViewSet, basename='persona-moral')
router.register(r'sucursales', SucursalViewSet, basename='sucursal')

urlpatterns = router.urls
