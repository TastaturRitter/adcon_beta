"""
Modelo de Persona Física para el app de parties de Adcon.

Extiende la información de una Parte para individuos humanos.
"""

from django.db import models
from .parte import Parte


class PersonaFisica(models.Model):
    """
    Representa a una persona humana dentro del sistema.

    Mapea la tabla SQL: personas_fisicas.
    Relación 1:1 con el modelo base Parte.
    """

    parte = models.OneToOneField(
        Parte,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='persona_fisica',
        verbose_name='Parte Base',
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre(s)',
    )
    apellido_paterno = models.CharField(
        max_length=100,
        verbose_name='Apellido Paterno',
    )
    apellido_materno = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Apellido Materno',
    )
    rfc = models.CharField(
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        verbose_name='RFC',
    )
    curp = models.CharField(
        max_length=18,
        unique=True,
        null=True,
        blank=True,
        verbose_name='CURP',
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Nacimiento',
    )
    nacionalidad = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Nacionalidad',
    )

    class Meta:
        db_table = 'personas_fisicas'
        verbose_name = 'Persona Física'
        verbose_name_plural = 'Personas Físicas'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombre']

    def __str__(self) -> str:
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno or ''}".strip()
