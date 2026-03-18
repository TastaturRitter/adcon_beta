"""
Modelo base de Partes para el app de parties de Adcon.

Representa a cualquier entidad (persona o empresa) que interviene 
en los instrumentos jurídicos gestionados por el sistema.
"""

import uuid
from django.db import models
from audit.models.base import AuditModel


class Parte(AuditModel):
    """
    Representa una entidad externa involucrada en contratos.

    Mapea la tabla SQL: partes.
    Actúa como base para tipos especializados (Persona Física/Moral).
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID Único',
    )
    tipo_parte = models.ForeignKey(
        'core.TipoParte',
        on_delete=models.RESTRICT,
        related_name='partes',
        verbose_name='Tipo de Parte',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partes',
        verbose_name='Domicilio Fiscal',
        help_text='Domicilio principal de la parte.',
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Correo Electrónico',
    )
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Teléfono',
    )

    class Meta:
        db_table = 'partes'
        verbose_name = 'Parte'
        verbose_name_plural = 'Partes'
        ordering = ['tipo_parte', 'email']

    def __str__(self) -> str:
        # Intenta obtener el nombre de la sub-clase si existe
        if hasattr(self, 'persona_fisica'):
            return str(self.persona_fisica)
        if hasattr(self, 'persona_moral'):
            return str(self.persona_moral)
        return f"Parte {self.id} ({self.tipo_parte})"
