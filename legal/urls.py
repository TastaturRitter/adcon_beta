"""
Rutas para el app Legal de Adcon.
"""

from rest_framework.routers import DefaultRouter
from legal.views.legal_views import (
    NotarioViewSet, EscrituraViewSet,
    EscrituraPersonalidadViewSet, EscrituraFacultadViewSet,
)

router = DefaultRouter()
router.register(r'notarios', NotarioViewSet, basename='notario')
router.register(r'escrituras', EscrituraViewSet, basename='escritura')
router.register(r'escrituras-personalidad', EscrituraPersonalidadViewSet, basename='escritura-personalidad')
router.register(r'escrituras-facultades', EscrituraFacultadViewSet, basename='escritura-facultad')

urlpatterns = router.urls
