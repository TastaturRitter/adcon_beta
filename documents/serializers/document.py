"""
Serializers para el app de documentos del sistema Adcon.

Gestiona la transformación de los modelos de documentos a JSON y viceversa,
asegurando que los archivos físicos sean manejados bajo los estándares
de seguridad requeridos.
"""

from typing import Any, Dict
from rest_framework import serializers
from documents.models.document import Document


class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Document.

    Garantiza la trazabilidad del archivo al marcar 'uploaded_by' como
    solo lectura, permitiendo que el sistema lo asigne automáticamente.
    """

    # El campo uploaded_by es de solo lectura para evitar suplantaciones
    uploaded_by_name: str = serializers.CharField(
        source='uploaded_by.username',
        read_only=True,
    )

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'file',
            'uploaded_by',
            'uploaded_by_name',
            'fecha_creacion',
            'creado_por',
        ]
        read_only_fields = ['id', 'uploaded_by', 'fecha_creacion', 'creado_por']

    def validate_file(self, value: Any) -> Any:
        """
        Validación adicional de seguridad para los archivos cargados.
        (E.g. extensiones permitidas, tamaño máximo).
        """
        # Aquí se podrían añadir validaciones de tipo de archivo si es necesario
        return value
