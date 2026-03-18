"""
Configuración central de URLs para el proyecto adcon_beta.

Incluye el panel de administración de Django y los routers REST de
las aplicaciones users y core bajo el prefijo /api/.

Los routers de cada app son responsables de registrar sus propios endpoints,
manteniendo esta configuración limpia y extensible (Open/Closed Principle).
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # API del sistema Adcon — Incluye autenticación y gestión de usuarios
    path('api/', include('users.urls')),
    path('api/core/', include('core.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/assets/', include('assets.urls')),
    path('api/parties/', include('parties.urls')),
    path('api/legal/', include('legal.urls')),
    path('api/instruments/', include('instruments.urls')),
    path('api/guarantees/', include('guarantees.urls')),

    # Navegador interactivo de la API (solo en DEBUG, habilitado por DRF)
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
