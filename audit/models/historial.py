"""
Modelo para el historial de auditoría inmutable de todas las operaciones
realizadas dentro del sistema Adcon (Regla IMMUTABLE AUDIT RULE).

Utiliza el framework de tipos de contenido de Django para asociar
dinámicamente un registro de auditoría a cualquier objeto del sistema,
implementando el patrón GenericForeignKey (Maker-Checker).
"""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class HistorialRegistro(models.Model):
    """
    Registro inmutable de cada acción realizada sobre cualquier entidad
    del sistema. Soporta el flujo Maker-Checker: quien propone (pre_registro)
    y quien aprueba (autorizador).

    Mapea la tabla SQL: historial_registros
    """

    # ── 1. IDENTIFICADOR DE ENTIDAD (GenericForeignKey) ───────────────────────
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Tipo de contenido',
        help_text='Referencia al modelo afectado (ej: instrumentos, partes).',
    )
    object_id = models.CharField(
        max_length=50,
        verbose_name='ID del objeto',
        help_text='Identificador primario del registro afectado.',
    )
    # Acceso Python conveniente sin columna adicional en BD
    objeto_afectado = GenericForeignKey('content_type', 'object_id')

    # ── 2. DETALLE DEL CAMBIO ─────────────────────────────────────────────────
    atributo_modificado = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Atributo modificado',
        help_text='Snapshot JSON con el estado "antes" y "después" del cambio.',
    )

    # ── 3. TIPO DE ACCIÓN ─────────────────────────────────────────────────────
    tipo_accion = models.CharField(
        max_length=20,
        verbose_name='Tipo de acción',
        help_text='Código de la operación realizada: CREACION, EDICION, VALIDACION, etc.',
    )

    # ── 4. ACTORES ────────────────────────────────────────────────────────────
    usuario_pre_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historial_propuestos',
        verbose_name='Usuario Maker',
        help_text='Usuario que propuso o ejecutó la acción (Maker).',
    )
    usuario_autorizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='historial_autorizados',
        verbose_name='Usuario Checker',
        help_text='Usuario que aprobó o validó la acción (Checker).',
    )

    # ── 5. CONTEXTO ───────────────────────────────────────────────────────────
    comentario = models.TextField(
        null=True,
        blank=True,
        verbose_name='Comentario',
        help_text='Justificación o descripción textual del cambio aplicado.',
    )
    fecha_evento = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del evento',
        help_text='Marca de tiempo inmutable del momento exacto de la acción.',
    )

    class Meta:
        db_table = 'historial_registros'
        verbose_name = 'Historial de Registro'
        verbose_name_plural = 'Historial de Registros'
        ordering = ['-fecha_evento']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

    def __str__(self) -> str:
        return f'[{self.tipo_accion}] {self.content_type} #{self.object_id} — {self.fecha_evento:%Y-%m-%d %H:%M}'
