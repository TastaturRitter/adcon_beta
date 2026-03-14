"""
Modelos adicionales del app Partes: Sucursal y AccionistaSocio.

Sucursal: establecimientos físicos dependientes de una parte.
AccionistaSocio: estructura de capital accionario entre partes del sistema.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from audit.models.base import AuditModel


class Sucursal(AuditModel):
    """
    Establecimiento físico adicional (sucursal u oficina) perteneciente a una parte.

    Permite registrar múltiples sedes de una misma entidad, vinculadas
    a distintos domicilios, siendo útil para operaciones multi-sede.

    Mapea la tabla SQL: sucursales
    """

    parte = models.ForeignKey(
        'parties.Parte',
        on_delete=models.CASCADE,
        related_name='sucursales',
        verbose_name='Parte',
        help_text='Entidad propietaria o responsable de esta sucursal.',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        related_name='sucursales',
        verbose_name='Domicilio',
        help_text='Dirección física de la sucursal.',
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre de Sucursal',
        help_text='Nombre o identificador interno de la sucursal. Único por parte.',
    )
    telefono = models.CharField(max_length=30, null=True, blank=True, verbose_name='Teléfono')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo Electrónico')

    class Meta:
        db_table = 'sucursales'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        unique_together = [('parte', 'nombre')]
        ordering = ['parte', 'nombre']

    def __str__(self) -> str:
        return f'{self.nombre} ({self.parte})'


class AccionistaSocio(AuditModel):
    """
    Registro de la participación accionaria de una parte (accionista)
    dentro del capital social de otra parte (sociedad).

    Permite trazar la estructura corporativa completa de las partes
    y detectar relaciones de control o vinculación entre entidades.

    Mapea la tabla SQL: accionistas_socios
    """

    sociedad = models.ForeignKey(
        'parties.Parte',
        on_delete=models.CASCADE,
        related_name='accionistas',
        verbose_name='Sociedad',
        help_text='Persona moral cuyo capital se está distribuyendo.',
    )
    accionista = models.ForeignKey(
        'parties.Parte',
        on_delete=models.CASCADE,
        related_name='participaciones',
        verbose_name='Accionista',
        help_text='Parte que posee acciones o participación en la sociedad.',
    )
    porcentaje_participacion = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(100)],
        verbose_name='Porcentaje de Participación (%)',
        help_text='Porcentaje del capital social que posee el accionista. Rango: 0.01 – 100.',
    )
    fecha_adquisicion = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Adquisición',
        help_text='Fecha en que se adquirió esta participación accionaria.',
    )
    tipo_participacion = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Tipo de Participación',
        help_text='Serie o clase de acciones. Ej: Serie A, Capital Variable.',
    )

    class Meta:
        db_table = 'accionistas_socios'
        verbose_name = 'Accionista / Socio'
        verbose_name_plural = 'Accionistas / Socios'
        unique_together = [('sociedad', 'accionista')]
        ordering = ['-porcentaje_participacion']

    def __str__(self) -> str:
        return f'{self.accionista} → {self.sociedad} ({self.porcentaje_participacion}%)'
