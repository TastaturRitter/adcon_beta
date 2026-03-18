"""
Modelo de Inmueble para el app de activos (Assets) de Adcon.

Gestiona la información técnica, legal y de ubicación de los bienes 
inmuebles que forman parte del patrimonio o garantía del sistema.
"""

import uuid
from django.db import models
from audit.models.base import AuditModel


class Inmueble(AuditModel):
    """
    Representa un bien raíz dentro del sistema Adcon.

    Mapea la tabla SQL: inmuebles.
    Hereda de AuditModel para trazabilidad completa.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='ID Único',
    )
    clave_catastral = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Clave Catastral',
        help_text='Identificador oficial ante el catastro.',
    )
    tipo_inmueble = models.ForeignKey(
        'core.TipoInmueble',
        on_delete=models.RESTRICT,
        related_name='inmuebles',
        verbose_name='Tipo de Inmueble',
    )
    propietario = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='propiedades',
        verbose_name='Propietario',
        help_text='Dueño actual del inmueble.',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        related_name='inmuebles',
        verbose_name='Ubicación',
        help_text='Dirección física del inmueble.',
    )
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción',
        help_text='Detalles adicionales del inmueble.',
    )
    superficie_terreno_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Superficie Terreno (m2)',
    )
    superficie_construccion_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Superficie Construcción (m2)',
    )

    class Meta:
        db_table = 'inmuebles'
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'
        ordering = ['clave_catastral']

    def __str__(self) -> str:
        return f"{self.clave_catastral} - {self.tipo_inmueble}"
