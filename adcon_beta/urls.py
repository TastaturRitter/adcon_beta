"""
Configuración central de URLs para el proyecto adcon_beta.

Incluye el panel de administración de Django y los routers REST de
las aplicaciones users y core bajo el prefijo /api/.

Los routers de cada app son responsables de registrar sus propios endpoints,
manteniendo esta configuración limpia y extensible (Open/Closed Principle).
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # API del sistema Adcon — namespaced bajo /api/
    path('api/', include('users.urls')),
    path('api/core/', include('core.urls')),

    # Navegador interactivo de la API (solo en DEBUG, habilitado por DRF)
    path('api-auth/', include('rest_framework.urls')),
]
