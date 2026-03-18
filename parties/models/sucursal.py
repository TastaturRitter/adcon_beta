"""
Modelo de Sucursal para el app de parties de Adcon.

Gestiona las ubicaciones operativas adicionales de una Parte (empresa).
"""

import uuid
from django.db import models
from .parte import Parte


class Sucursal(models.Model):
    """
    Representa una sucursal o sede física de una parte.

    Mapea la tabla SQL: sucursales.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID Único',
    )
    parte = models.ForeignKey(
        Parte,
        on_delete=models.CASCADE,
        related_name='sucursales',
        verbose_name='Entidad Principal',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        related_name='sucursales',
        verbose_name='Dirección de la Sucursal',
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre de la Sucursal',
    )
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Teléfono Sucursal',
    )
    email = models.EmailField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Correo Sucursal',
    )

    class Meta:
        db_table = 'sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['parte', 'nombre']

    def __str__(self) -> str:
        return f"{self.nombre} ({self.parte})"
