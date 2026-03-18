"""
Modelo de Persona Moral para el app de parties de Adcon.

Extiende la información de una Parte para entidades corporativas.
"""

from django.db import models
from .parte import Parte


class PersonaMoral(models.Model):
    """
    Representa a una empresa o institución dentro del sistema.

    Mapea la tabla SQL: personas_morales.
    Relación 1:1 con el modelo base Parte.
    """

    parte = models.OneToOneField(
        Parte,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='persona_moral',
        verbose_name='Parte Base',
    )
    razon_social = models.CharField(
        max_length=255,
        verbose_name='Razón Social',
    )
    rfc = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        verbose_name='RFC',
    )
    fecha_constitucion = models.DateField(
        verbose_name='Fecha de Constitución',
    )
    objeto_social = models.TextField(
        null=True,
        blank=True,
        verbose_name='Objeto Social',
    )
    organo_administracion = models.ForeignKey(
        'core.OrganoAdministracion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='empresas',
        verbose_name='Órgano de Administración',
    )
    representante_legal = models.ForeignKey(
        Parte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representaciones_legales',
        verbose_name='Representante Legal',
    )
    apoderado_general = models.ForeignKey(
        Parte,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='poderes_generales',
        verbose_name='Apoderado General',
    )

    class Meta:
        db_table = 'personas_morales'
        verbose_name = 'Persona Moral'
        verbose_name_plural = 'Personas Morales'
        ordering = ['razon_social']

    def __str__(self) -> str:
        return self.razon_social
