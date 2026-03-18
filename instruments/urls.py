"""
Rutas para el app de Instrumentos (núcleo CLM) de Adcon.
"""

from rest_framework.routers import DefaultRouter
from instruments.views.instrumento_views import (
    ConcursoViewSet, InstrumentoViewSet, InstrumentoParteViewSet,
    ArchivoFisicoViewSet, ArrendamientoViewSet,
    CompraventaInmuebleViewSet, ServicioPrestadoViewSet,
    SuministroMercanciaViewSet, ActoCorporativoViewSet,
)

router = DefaultRouter()
router.register(r'concursos', ConcursoViewSet, basename='concurso')
router.register(r'instrumentos', InstrumentoViewSet, basename='instrumento')
router.register(r'instrumento-parte', InstrumentoParteViewSet, basename='instrumento-parte')
router.register(r'archivos-fisicos', ArchivoFisicoViewSet, basename='archivo-fisico')
router.register(r'arrendamientos', ArrendamientoViewSet, basename='arrendamiento')
router.register(r'compraventas', CompraventaInmuebleViewSet, basename='compraventa')
router.register(r'servicios', ServicioPrestadoViewSet, basename='servicio')
router.register(r'suministros', SuministroMercanciaViewSet, basename='suministro')
router.register(r'actos-corporativos', ActoCorporativoViewSet, basename='acto-corporativo')

urlpatterns = router.urls
