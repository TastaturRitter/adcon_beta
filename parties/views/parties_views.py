"""
Vistas para la gestión de Partes (Personas Físicas, Morales y Sucursales) en Adcon.

Implementa ViewSets con permisos RBAC para asegurar el control sobre las entidades
legales del sistema.
"""

from rest_framework import viewsets
from parties.models import PersonaFisica, PersonaMoral, Sucursal
from parties.serializers.parties_serializers import (
    PersonaFisicaSerializer, PersonaMoralSerializer, SucursalSerializer
)
from core.permissions import AdconBasePermission


class PersonaFisicaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Personas Físicas.
    """
    queryset = PersonaFisica.objects.all().select_related('parte', 'parte__tipo_parte', 'parte__domicilio')
    serializer_class = PersonaFisicaSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer):
        # Asigna el usuario actual como creador de la Parte base
        serializer.save(parte={'creado_por': self.request.user})


class PersonaMoralViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Personas Morales (Empresas).
    """
    queryset = PersonaMoral.objects.all().select_related('parte', 'parte__tipo_parte', 'parte__domicilio')
    serializer_class = PersonaMoralSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer):
        serializer.save(parte={'creado_por': self.request.user})


class SucursalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Sucursales.
    """
    queryset = Sucursal.objects.all().select_related('parte', 'domicilio')
    serializer_class = SucursalSerializer
    permission_classes = [AdconBasePermission]
