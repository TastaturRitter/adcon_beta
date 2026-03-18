"""
Vistas para la gestión documental en Adcon.

Implementa los ViewSets para manejar el ciclo de vida de los archivos,
aplicando la matriz de permisos RBAC para asegurar que solo los usuarios
con roles autorizados puedan crear, editar o eliminar evidencia legal.
"""

from typing import Any
from rest_framework import viewsets
from documents.models.document import Document
from documents.serializers.document import DocumentSerializer
from core.permissions import AdconBasePermission


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el almacenamiento de documentos.

    Aplica AdconBasePermission para cumplir con la matriz RBAC:
    - ADMIN/MANAGER: CRUD completo.
    - EDITOR: Lectura y edición de metadatos (pero no borrado).
    - READER: Solo lectura (list/retrieve).
    """
    queryset = Document.objects.all().select_related('uploaded_by', 'creado_por')
    serializer_class = DocumentSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """
        Asigna automáticamente el usuario actual a los campos de auditoría y carga.

        Este paso es crítico para mantener la validez legal y la trazabilidad
        de quién introdujo el archivo al sistema.
        """
        serializer.save(
            uploaded_by=self.request.user,
            creado_por=self.request.user
        )
