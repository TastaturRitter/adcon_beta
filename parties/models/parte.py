"""
Modelo completo de Parte: actor jurídico que interviene en instrumentos contractuales.

Representa la entidad base que puede ser una Persona Física, Persona Moral
o cualquier otra figura jurídica reconocida. Las especializaciones se modelan
mediante relaciones 1:1 en sus propias tablas (personas_fisicas, personas_morales).
"""

from django.db import models

from audit.models.base import AuditModel


class Parte(AuditModel):
    """
    Entidad base que representa a cualquier actor jurídico del sistema:
    persona física, persona moral, fideicomiso u otra figura.

    Sigue un patrón de herencia por clase concreta (1:1 con sub-entidades)
    para mantener la flexibilidad del modelo de datos relacional original.

    Mapea la tabla SQL: partes
    """

    tipo_parte = models.ForeignKey(
        'core.TipoParte',
        on_delete=models.RESTRICT,
        related_name='partes',
        verbose_name='Tipo de Parte',
        help_text='Clasificación jurídica: Persona Física, Moral, Fideicomiso, etc.',
    )
    domicilio = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='partes',
        verbose_name='Domicilio Fiscal / Principal',
        help_text='Dirección principal o fiscal registrada en el sistema.',
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Correo Electrónico',
        help_text='Dirección de correo para notificaciones y comunicaciones formales.',
    )
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Teléfono',
        help_text='Número de contacto principal.',
    )

    class Meta:
        db_table = 'partes'
        verbose_name = 'Parte'
        verbose_name_plural = 'Partes'
        ordering = ['id']

    def __str__(self) -> str:
        # Intenta devolver la razón social o nombre completo desde la sub-entidad
        if hasattr(self, 'personamoral'):
            return self.personamoral.razon_social
        if hasattr(self, 'personafisica'):
            pf = self.personafisica
            return f'{pf.nombre} {pf.apellido_paterno} {pf.apellido_materno or ""}'.strip()
        return f'Parte #{self.pk}'
