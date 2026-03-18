"""
Vistas para el app Legal de Adcon.

ViewSets para Notarios, Escrituras y documentos de personalidad jurídica,
aplicando la matriz RBAC para que solo los roles autorizados puedan
crear, modificar o eliminar instrumentos notariales.
"""

from rest_framework import viewsets
from legal.models.legal import Notario, Escritura, EscrituraPersonalidad, EscrituraFacultad
from legal.serializers.legal_serializers import (
    NotarioSerializer, EscrituraSerializer,
    EscrituraPersonalidadSerializer, EscrituraFacultadSerializer,
)
from core.permissions import AdconBasePermission


class NotarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Notarios y Corredores Públicos.
    Permisos: ADMIN/MANAGER = CRUD; EDITOR = lectura/edición; READER = solo lectura.
    """
    queryset = Notario.objects.all().select_related('tipo_notario')
    serializer_class = NotarioSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Registra el usuario que da de alta al fedatario."""
        serializer.save(creado_por=self.request.user)


class EscrituraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Escrituras Públicas y Pólizas Mercantiles.
    """
    queryset = Escritura.objects.all().select_related('notario', 'tipo_escritura', 'instrumento')
    serializer_class = EscrituraSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Asigna el usuario actual como registrador del instrumento notarial."""
        serializer.save(creado_por=self.request.user)


class EscrituraPersonalidadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Escrituras de Personalidad Jurídica (poderes notariales).
    """
    queryset = EscrituraPersonalidad.objects.all().select_related(
        'representante', 'representado', 'notario'
    ).prefetch_related('facultades')
    serializer_class = EscrituraPersonalidadSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Registra el usuario que captura el poder notarial."""
        serializer.save(creado_por=self.request.user)


class EscrituraFacultadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para las Facultades o atribuciones de una escritura de poder.
    """
    queryset = EscrituraFacultad.objects.all().select_related('facultad', 'escritura_personalidad')
    serializer_class = EscrituraFacultadSerializer
    permission_classes = [AdconBasePermission]
