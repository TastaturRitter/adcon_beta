"""
Modelos del app Legal: Notario, Escritura pública, Escritura de personalidad
y Escritura de facultades.

Este módulo gestiona el universo notarial: los fedatarios públicos que dan
fe de los actos jurídicos y los instrumentos notariales (escrituras, poderes)
que acreditan la representación legal de las partes en los contratos.
"""

from django.db import models

from audit.models.base import AuditModel


class Notario(AuditModel):
    """
    Fedatario público (Notario o Corredor Público) registrado en el sistema.

    La combinación (distrito, numero_notaria) es única, evitando duplicar
    la misma notaría. El RFC permite identificarlo para efectos fiscales
    y de facturación de honorarios notariales.

    Mapea la tabla SQL: notarios
    """

    tipo_notario = models.ForeignKey(
        'core.TipoNotario',
        on_delete=models.RESTRICT,
        related_name='notarios',
        verbose_name='Tipo de Fedatario',
        help_text='Ej: Notario Público, Corredor Público.',
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre(s)')
    apellido_paterno = models.CharField(max_length=100, verbose_name='Apellido Paterno')
    apellido_materno = models.CharField(max_length=100, null=True, blank=True, verbose_name='Apellido Materno')
    numero_notaria = models.IntegerField(verbose_name='Número de Notaría')
    distrito = models.CharField(max_length=100, verbose_name='Distrito / Entidad', help_text='Ej: Ciudad de México, Estado de Morelos.')
    rfc = models.CharField(max_length=13, null=True, blank=True, unique=True, verbose_name='RFC')
    email = models.EmailField(null=True, blank=True, verbose_name='Correo Electrónico')

    class Meta:
        db_table = 'notarios'
        verbose_name = 'Notario / Fedatario'
        verbose_name_plural = 'Notarios / Fedatarios'
        unique_together = [('distrito', 'numero_notaria')]
        ordering = ['distrito', 'numero_notaria']

    def __str__(self) -> str:
        return f'Not. {self.numero_notaria} {self.distrito} — {self.apellido_paterno} {self.nombre}'


class Escritura(AuditModel):
    """
    Instrumento notarial (escritura pública o póliza mercantil) que da fe
    de los actos jurídicos relacionados con un instrumento del CLM.

    Incluye datos de localización en el Registro Público de la Propiedad o
    del Comercio (RPP/RPC) para facilitar búsquedas registrales.

    Mapea la tabla SQL: escrituras
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='escrituras',
        verbose_name='Instrumento',
    )
    notario = models.ForeignKey(
        Notario,
        on_delete=models.RESTRICT,
        related_name='escrituras',
        verbose_name='Notario',
    )
    tipo_escritura = models.ForeignKey(
        'core.TipoEscritura',
        on_delete=models.RESTRICT,
        related_name='escrituras',
        verbose_name='Tipo de Escritura',
    )
    titulo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Título')
    numero_escritura = models.CharField(max_length=50, verbose_name='Número de Escritura')
    numero_testimonio = models.CharField(max_length=50, null=True, blank=True, verbose_name='Número de Testimonio')
    datos_registro_publico = models.CharField(max_length=100, null=True, blank=True, verbose_name='Datos Registro Público', help_text='Ej: "Libro 1, Foja 10" o "RPC 2025/12345".')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre de Archivo')
    ruta_archivo = models.FileField(
        upload_to='legal/escrituras/',
        null=True, blank=True,
        verbose_name='Escritura Digital (S3)',
        help_text='PDF de la escritura. Almacenado cifrado en AWS S3 con AES256.',
    )
    fecha_otorgamiento = models.DateField(verbose_name='Fecha de Otorgamiento')

    class Meta:
        db_table = 'escrituras'
        verbose_name = 'Escritura'
        verbose_name_plural = 'Escrituras'
        ordering = ['-fecha_otorgamiento']

    def __str__(self) -> str:
        return f'Escritura {self.numero_escritura} — Not. {self.notario}'


class EscrituraPersonalidad(AuditModel):
    """
    Escritura de poder o acreditación de personalidad jurídica.

    Vincula a un representante (persona física) con la entidad que representa
    (persona moral), definiendo la escritura que acredita su facultad de actuar
    en nombre de ella. Soporta restricciones de monto u objeto.

    Mapea la tabla SQL: escrituras_personalidad
    """

    representante = models.ForeignKey(
        'parties.Parte',
        on_delete=models.RESTRICT,
        related_name='poderes_como_representante',
        verbose_name='Representante (Delegado)',
        help_text='Persona física que actúa en nombre de la persona moral.',
    )
    representado = models.ForeignKey(
        'parties.Parte',
        on_delete=models.RESTRICT,
        related_name='poderes_como_representado',
        verbose_name='Representado (Empresa)',
        help_text='Persona moral en cuyo nombre actúa el representante.',
    )
    notario = models.ForeignKey(
        Notario,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='escrituras_personalidad',
        verbose_name='Notario',
    )
    instrumento_origen = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='escrituras_personalidad',
        verbose_name='Instrumento de Origen',
    )
    numero_escritura = models.CharField(max_length=100, verbose_name='Número de Escritura')
    fecha_otorgamiento = models.DateField(verbose_name='Fecha de Otorgamiento')
    lugar_otorgamiento = models.CharField(max_length=255, null=True, blank=True, verbose_name='Lugar de Otorgamiento')
    comentarios = models.TextField(null=True, blank=True, verbose_name='Comentarios / Limitaciones', help_text='Ej: "Poder limitado a $500,000 MXN".')
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre de Archivo')
    ruta_archivo = models.FileField(
        upload_to='legal/poderes/',
        null=True, blank=True,
        verbose_name='PDF del Poder (S3)',
    )

    class Meta:
        db_table = 'escrituras_personalidad'
        verbose_name = 'Escritura de Personalidad / Poder'
        verbose_name_plural = 'Escrituras de Personalidad / Poderes'
        unique_together = [('representante', 'representado', 'numero_escritura')]

    def __str__(self) -> str:
        return f'Poder {self.numero_escritura}: {self.representante} por {self.representado}'


class EscrituraFacultad(models.Model):
    """
    Facultad específica otorgada en una escritura de personalidad.

    Permite granularizar los poderes: una escritura puede otorgar múltiples
    facultades, cada una con sus propias limitaciones de monto u objeto.

    Mapea la tabla SQL: escrituras_facultades
    """

    escritura_personalidad = models.ForeignKey(
        EscrituraPersonalidad,
        on_delete=models.CASCADE,
        related_name='facultades',
        verbose_name='Escritura de Personalidad',
    )
    facultad = models.ForeignKey(
        'core.CatFacultad',
        on_delete=models.RESTRICT,
        related_name='escrituras',
        verbose_name='Facultad',
    )
    limitacion_descripcion = models.TextField(
        null=True, blank=True,
        verbose_name='Limitación',
        help_text='Descripción de la restricción a la facultad otorgada. Ej: "Solo hasta $500,000".',
    )

    class Meta:
        db_table = 'escrituras_facultades'
        verbose_name = 'Escritura Facultad'
        verbose_name_plural = 'Escrituras Facultades'
        unique_together = [('escritura_personalidad', 'facultad')]

    def __str__(self) -> str:
        return f'{self.facultad} — {self.escritura_personalidad}'
