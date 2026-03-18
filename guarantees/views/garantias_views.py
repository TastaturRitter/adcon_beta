"""
Vistas para el app de Garantías de Adcon.

ViewSets para Penas Convencionales y Fianzas (pólizas de garantía),
aplicando la matriz RBAC para el control de acceso a los documentos
de garantía contractual.
"""

from rest_framework import viewsets
from guarantees.models.garantias import Pena, Fianza
from guarantees.serializers.garantias_serializers import PenaSerializer, FianzaSerializer
from core.permissions import AdconBasePermission


class PenaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Penas Convencionales por incumplimiento contractual.
    Permisos: ADMIN/MANAGER = CRUD; EDITOR = lectura/edición; READER = solo lectura.
    """
    queryset = Pena.objects.all().select_related(
        'instrumento', 'tipo_dia', 'addendum', 'modificatorio', 'anexo', 'partida'
    )
    serializer_class = PenaSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Registra el usuario que captura la pena convencional."""
        serializer.save(creado_por=self.request.user)


class FianzaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Fianzas (pólizas de garantía de cumplimiento).
    """
    queryset = Fianza.objects.all().select_related(
        'instrumento', 'tipo_fianza', 'tipo_obligacion', 'afianzadora', 'pena'
    )
    serializer_class = FianzaSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Registra el usuario que sube la póliza de fianza."""
        serializer.save(creado_por=self.request.user)
