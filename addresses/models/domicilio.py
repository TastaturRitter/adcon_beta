"""
Modelo de Domicilio: dirección postal asociable a partes e inmuebles.
"""

from django.db import models
from audit.models.base import AuditModel


class Domicilio(AuditModel):
    """
    Dirección postal completa utilizada para la ubicación de inmuebles
    y como domicilio legal de las partes en los instrumentos.

    Esta es la definición mínima viable (stub) para satisfacer las
    relaciones de clave foránea del bloque actual.
    Se ampliará en el bloque de modelado de APP DOMICILIOS.

    Mapea la tabla SQL: domicilios
    """

    calle = models.CharField(max_length=255, null=True, blank=True, verbose_name='Calle')
    no_exterior = models.CharField(max_length=50, null=True, blank=True, verbose_name='Núm. Exterior')
    no_interior = models.CharField(max_length=50, null=True, blank=True, verbose_name='Núm. Interior')
    colonia = models.CharField(max_length=100, null=True, blank=True, verbose_name='Colonia')
    codigo_postal = models.CharField(max_length=10, null=True, blank=True, verbose_name='Código Postal')
    municipio = models.CharField(max_length=100, null=True, blank=True, verbose_name='Municipio')
    estado = models.CharField(
        max_length=100,
        verbose_name='Estado',
        help_text='Estado o entidad federativa. Campo obligatorio.',
    )
    referencia_adicional = models.TextField(
        null=True, blank=True,
        verbose_name='Referencia Adicional',
        help_text='Indicaciones extra para localización del domicilio.',
    )

    class Meta:
        db_table = 'domicilios'
        verbose_name = 'Domicilio'
        verbose_name_plural = 'Domicilios'
        ordering = ['estado', 'municipio']

    def __str__(self) -> str:
        partes = filter(None, [self.calle, self.no_exterior, self.colonia, self.municipio, self.estado])
        return ', '.join(partes)
