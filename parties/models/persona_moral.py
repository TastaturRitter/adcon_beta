"""
Modelos de especialización para Persona Moral dentro del sistema Adcon.

Implementa el patrón de herencia concreta 1:1 con la tabla 'partes'.
Contiene los datos corporativos: razón social, RFC, constitución,
estructura de administración y representación legal.
"""

from django.db import models


class PersonaMoral(models.Model):
    """
    Perfil de datos exclusivo para personas morales (empresas, sociedades,
    asociaciones) que participan como partes en los instrumentos del sistema.

    Relación 1:1 con Parte — comparte la misma PK que la parte base.
    Se accede vía: parte.personamoral

    Mapea la tabla SQL: personas_morales
    """

    parte = models.OneToOneField(
        'parties.Parte',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='personamoral',
        verbose_name='Parte Base',
        help_text='Registro base en la tabla partes al que pertenece este perfil corporativo.',
    )

    # ── DATOS CORPORATIVOS ───────────────────────────────────────────────────
    razon_social = models.CharField(
        max_length=255,
        verbose_name='Razón Social',
        help_text='Denominación o razón social completa tal como aparece en el acta constitutiva.',
    )
    rfc = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        unique=True,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes (12 caracteres para persona moral).',
    )
    fecha_constitucion = models.DateField(
        verbose_name='Fecha de Constitución',
        help_text='Fecha en que se protocolizó el acta constitutiva ante notario.',
    )
    objeto_social = models.TextField(
        null=True,
        blank=True,
        verbose_name='Objeto Social',
        help_text='Descripción de las actividades y propósitos autorizados para la sociedad.',
    )

    # ── ESTRUCTURA ADMINISTRATIVA ─────────────────────────────────────────────
    organo_administracion = models.ForeignKey(
        'core.OrganoAdministracion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personas_morales',
        verbose_name='Órgano de Administración',
        help_text='Tipo de órgano directivo: Administrador Único, Consejo de Administración, etc.',
    )

    # ── REPRESENTACIÓN LEGAL (Recursividad) ───────────────────────────────────
    representante_legal = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representante_legal_de',
        verbose_name='Representante Legal',
        help_text='Persona física que firma por default en nombre de la empresa.',
    )
    apoderado_general = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='apoderado_general_de',
        verbose_name='Apoderado General',
        help_text='Apoderado con facultades generales distintas al representante legal.',
    )

    class Meta:
        db_table = 'personas_morales'
        verbose_name = 'Persona Moral'
        verbose_name_plural = 'Personas Morales'

    def __str__(self) -> str:
        return self.razon_social
