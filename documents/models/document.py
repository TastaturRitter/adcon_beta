"""
Modelo de documento del sistema Adcon.

Representa los archivos físicos (PDFs, imágenes, etc.) que se asocian
a los instrumentos jurídicos, anexos o evidencias. Hereda de AuditModel
para garantizar la trazabilidad de quién subió el archivo y cuándo.

La integridad de estos archivos es crítica para la validez legal
de los contratos gestionados en la plataforma.
"""

import uuid
from django.db import models
from django.conf import settings
from audit.models.base import AuditModel


class Document(AuditModel):
    """
    Entidad que gestiona el almacenamiento y metadatos de archivos legales.

    Campos heredados de AuditModel:
    - creado_por: Usuario que registró el metadato (SET_NULL).
    - fecha_creacion: Marca de tiempo de la creación del registro.

    Campos específicos:
    - id: Identificador único universal (UUID).
    - title: Nombre o título descriptivo del documento.
    - file: Referencia al archivo físico almacenado (e.g. en AWS S3).
    - uploaded_by: El usuario responsable legal de la carga del archivo.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID Único',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Título del Documento',
        help_text='Nombre descriptivo para identificar el archivo en el sistema.',
    )
    file = models.FileField(
        upload_to='contracts/%Y/%m/%d/',
        verbose_name='Archivo',
        help_text='Archivo físico (PDF, imagen) cargado en el almacenamiento seguro.',
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='documentos_cargados',
        verbose_name='Cargado por',
        help_text='Usuario que realizó la carga física del documento al sistema.',
    )

    class Meta:
        db_table = 'documentos_gestion'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_creacion']

    def __str__(self) -> str:
        """Representación textual del documento."""
        return self.title
