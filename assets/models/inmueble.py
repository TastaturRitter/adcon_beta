"""
Modelo de Inmueble: activo de bienes raíces gestionado por el sistema Adcon.

Representa propiedades físicas (casas, locales, terrenos, bodegas) que pueden
ser objeto de uno o más instrumentos contractuales (arrendamiento, compraventa,
comodato). Vincula el activo con su tipo, propietario actual y domicilio.
"""

from django.db import models
from django.core.validators import MinValueValidator

from audit.models.base import AuditModel


class Inmueble(AuditModel):
    """
    Activo inmobiliario registrado en el sistema como unidad gestionable.

    Un inmueble puede participar como objeto de contrato en múltiples
    instrumentos a lo largo del tiempo (histórico de arrendamientos, ventas, etc.).
    La clave catastral lo identifica de forma única ante el registro público.

    Mapea la tabla SQL: inmuebles
    """

    # ── IDENTIFICACIÓN ────────────────────────────────────────────────────────
    clave_catastral = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Clave Catastral',
        help_text='Identificador único ante el registro público de la propiedad.',
    )
    tipo_inmueble = models.ForeignKey(
        'core.TipoInmueble',
        on_delete=models.RESTRICT,
        related_name='inmuebles',
        verbose_name='Tipo de Inmueble',
        help_text='Clasificación del activo: Casa, Local, Terreno, Bodega, etc.',
    )

    # ── PROPIEDAD ─────────────────────────────────────────────────────────────
    propietario = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inmuebles_propietario',
        verbose_name='Propietario',
        help_text='Parte que ostenta la titularidad del inmueble al momento del registro.',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        related_name='inmuebles',
        verbose_name='Domicilio',
        help_text='Ubicación física del inmueble según el registro catastral.',
    )

    # ── CARACTERÍSTICAS ───────────────────────────────────────────────────────
    descripcion = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción',
        help_text='Descripción libre del inmueble: materiales, estado, instalaciones especiales.',
    )
    superficie_terreno_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Superficie de Terreno (m²)',
        help_text='Área total del terreno en metros cuadrados. Debe ser >= 0.',
    )
    superficie_construccion_m2 = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Superficie de Construcción (m²)',
        help_text='Área construida del inmueble en metros cuadrados. Debe ser >= 0.',
    )

    class Meta:
        db_table = 'inmuebles'
        verbose_name = 'Inmueble'
        verbose_name_plural = 'Inmuebles'
        ordering = ['clave_catastral']

    def __str__(self) -> str:
        return f'{self.clave_catastral} — {self.tipo_inmueble}'
