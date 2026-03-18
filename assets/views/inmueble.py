"""
Vistas para la gestión de activos (Assets) en Adcon.

Implementa el ViewSet de Inmuebles aplicando la matriz de permisos RBAC
para asegurar la integridad de los datos patrimoniales.
"""

from rest_framework import viewsets
from assets.models.inmueble import Inmueble
from assets.serializers.inmueble import InmuebleSerializer
from core.permissions import AdconBasePermission


class InmuebleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de Inmuebles.

    Permisos:
    - ADMIN/MANAGER: CRUD Completo.
    - EDITOR: Lectura y Edición (no borrado/creado).
    - READER: Solo Lectura.
    """
    queryset = Inmueble.objects.all().select_related('tipo_inmueble', 'propietario', 'domicilio')
    serializer_class = InmuebleSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """
        Asigna el usuario actual como creador del registro del inmueble.
        """
        serializer.save(creado_por=self.request.user)
