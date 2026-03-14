"""
Modelo base abstracto para auditoria de todos los registros del sistema Adcon.

Provee campos reutilizables de auditoría (quién creó, cuándo) que deben
heredarse en todos los modelos concretos del ecosistema. Sigue el principio
DRY: un solo lugar para definir el comportamiento de auditoría.
"""

from django.db import models
from django.conf import settings


class AuditModel(models.Model):
    """
    Clase base abstracta que encapsula los campos de auditoría
    estándar requeridos por todos los modelos del sistema CLM.

    Al ser abstracta, Django no crea tabla para ella en la base
    de datos; solo transfiere sus campos a los modelos hijos.
    """

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(app_label)s_%(class)s_creados',
        verbose_name='Creado por',
        help_text='Usuario del sistema que registró este objeto.',
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        help_text='Marca de tiempo automática al momento de la inserción.',
    )

    class Meta:
        abstract = True
