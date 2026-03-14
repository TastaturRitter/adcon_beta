"""
Modelos de especialización para Persona Física dentro del sistema Adcon.

Implementa el patrón de herencia concreta 1:1 con la tabla 'partes'.
Contiene los datos exclusivos de una persona física: datos personales,
identificaciones fiscales (RFC, CURP) y fecha de nacimiento.
"""

from django.db import models


class PersonaFisica(models.Model):
    """
    Perfil de datos exclusivo para personas físicas (seres humanos)
    que participan como partes en los instrumentos del sistema.

    Relación 1:1 con Parte — comparte la misma PK que la parte base.
    Se accede vía: parte.personafisica

    Mapea la tabla SQL: personas_fisicas
    """

    parte = models.OneToOneField(
        'parties.Parte',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='personafisica',
        verbose_name='Parte Base',
        help_text='Registro base en la tabla partes al que pertenece este perfil.',
    )

    # ── DATOS PERSONALES ──────────────────────────────────────────────────────
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre(s)',
        help_text='Nombre o nombres de pila de la persona física.',
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

    # ── IDENTIFICACIÓN ────────────────────────────────────────────────────────
    rfc = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        unique=True,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes (13 caracteres para persona física).',
    )
    curp = models.CharField(
        max_length=18,
        null=True,
        blank=True,
        unique=True,
        verbose_name='CURP',
        help_text='Clave Única de Registro de Población (18 caracteres).',
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

    def __str__(self) -> str:
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno or ""}'.strip()
