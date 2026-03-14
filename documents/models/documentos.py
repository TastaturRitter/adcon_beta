"""
Modelos del app Documentos: Anexo, Partida, Modificatorio, Addendum y Evidencia.

Los documentos son los archivos digitales vinculados a un instrumento jurídico.
Todos los archivos se almacenan en AWS S3 con cifrado AES256 mediante el campo
FileField con upload_to dinámico por contrato.

Regla clave: los campos de cálculo automático del SQL (GENERATED ALWAYS AS)
se implementan como @property en Python, ya que Django no los soporta nativamente.
"""

from django.db import models
from django.core.validators import MinValueValidator

from audit.models.base import AuditModel


class Anexo(AuditModel):
    """
    Documento de soporte anexado a un instrumento contractual.

    Puede ser de naturaleza técnica, económica, legal o administrativa.
    La restricción UNIQUE (instrumento, nombre_documento) evita duplicados
    dentro del mismo contrato para no confundir al usuario final.

    Mapea la tabla SQL: anexos
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='anexos',
        verbose_name='Instrumento',
    )
    categoria_anexo = models.ForeignKey(
        'core.CategoriaAnexo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='anexos',
        verbose_name='Categoría del Anexo',
    )
    entrega = models.ForeignKey(
        'tracking.Entrega',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='anexos',
        verbose_name='Entrega Asociada',
    )
    nombre_documento = models.CharField(max_length=512, verbose_name='Nombre del Documento')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre del Archivo')
    ruta_archivo = models.FileField(
        upload_to='documentos/anexos/',
        null=True, blank=True,
        verbose_name='Archivo Digital (S3)',
        help_text='PDF o documento del anexo. Almacenado cifrado en AWS S3 con AES256.',
    )

    class Meta:
        db_table = 'anexos'
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        unique_together = [('instrumento', 'nombre_documento')]
        ordering = ['instrumento', 'nombre_documento']

    def __str__(self) -> str:
        return f'{self.nombre_documento} — {self.instrumento.num_instrumento}'


class Partida(AuditModel):
    """
    Ítem o línea de detalle dentro de un anexo contractual.

    Representa un bien, servicio o entregable específico con su precio
    unitario, cantidad y tasa de IVA. Los importes se calculan como
    propiedades de Python (equivalente a las columnas GENERATED ALWAYS AS del SQL).

    Mapea la tabla SQL: partidas
    """

    anexo = models.ForeignKey(
        Anexo,
        on_delete=models.CASCADE,
        related_name='partidas',
        verbose_name='Anexo',
    )
    nombre_partida = models.CharField(max_length=255, verbose_name='Nombre de la Partida', help_text='Ej: "Laptop Dell Latitude", "Hora de Consultoría".')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Especificaciones Técnicas')
    unidad_medida = models.CharField(max_length=50, verbose_name='Unidad de Medida', help_text='Ej: Piezas, Horas, Licencias, Metros.')
    cantidad = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Cantidad',
    )
    precio_unitario = models.DecimalField(
        max_digits=15, decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Precio Unitario',
    )
    tasa_iva = models.DecimalField(
        max_digits=5, decimal_places=2,
        default='0.16',
        verbose_name='Tasa de IVA',
        help_text='Expresado como decimal. Ej: 0.16 para 16%, 0.00 para exento.',
    )

    # ── CAMPOS CALCULADOS (equivale al GENERATED ALWAYS AS del SQL) ───────────
    @property
    def importe_subtotal(self) -> 'Decimal':
        """Subtotal antes de IVA: cantidad × precio_unitario."""
        return self.cantidad * self.precio_unitario

    @property
    def monto_iva(self) -> 'Decimal':
        """IVA calculado sobre el subtotal."""
        return self.importe_subtotal * self.tasa_iva

    @property
    def importe_total(self) -> 'Decimal':
        """Total final con IVA incluido."""
        return self.importe_subtotal * (1 + self.tasa_iva)

    class Meta:
        db_table = 'partidas'
        verbose_name = 'Partida'
        verbose_name_plural = 'Partidas'
        unique_together = [('anexo', 'nombre_partida')]
        ordering = ['anexo', 'nombre_partida']

    def __str__(self) -> str:
        return f'{self.nombre_partida} (Anexo: {self.anexo})'


class Modificatorio(AuditModel):
    """
    Documento modificatorio que altera una o más cláusulas de un contrato vigente.

    Ej: Convenio Modificatorio No. 1, Fe de Erratas, Prórroga.
    La restricción UNIQUE (instrumento, numero_modificatorio) garantiza que
    no existan dos 'Convenios No. 1' en el mismo contrato.

    Mapea la tabla SQL: modificatorios
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='modificatorios',
        verbose_name='Instrumento',
    )
    tipo_modificatorio = models.ForeignKey(
        'core.TipoModificatorio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='modificatorios',
        verbose_name='Tipo de Modificatorio',
    )
    numero_modificatorio = models.IntegerField(verbose_name='Número de Modificatorio', help_text='Secuencial por contrato. Ej: 1 para "Convenio No. 1".')
    titulo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción / Resumen Ejecutivo')
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión', help_text='Fecha de firma o entrada en vigor del modificatorio.')
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre del Archivo')
    ruta_archivo = models.FileField(upload_to='documentos/modificatorios/', null=True, blank=True, verbose_name='Modificatorio Digital (S3)')

    class Meta:
        db_table = 'modificatorios'
        verbose_name = 'Modificatorio'
        verbose_name_plural = 'Modificatorios'
        unique_together = [('instrumento', 'numero_modificatorio')]
        ordering = ['instrumento', 'numero_modificatorio']

    def __str__(self) -> str:
        return f'Modificatorio No. {self.numero_modificatorio} — {self.instrumento.num_instrumento}'


class Addendum(AuditModel):
    """
    Documento addendum que agrega o complementa cláusulas sin modificar
    el instrumento original. Clasificado por tipo (Técnico, Económico, etc.).

    La restricción UNIQUE (instrumento, numero_addendum) garantiza orden
    cronológico sin duplicados dentro del mismo contrato.

    Mapea la tabla SQL: addenda
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='addenda',
        verbose_name='Instrumento',
    )
    tipo_addendum = models.ForeignKey(
        'core.TipoAddendum',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='addenda',
        verbose_name='Tipo de Addendum',
    )
    numero_addendum = models.IntegerField(verbose_name='Número de Addendum')
    titulo = models.CharField(max_length=1024, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_emision = models.DateField(verbose_name='Fecha de Emisión')
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nombre del Archivo')
    ruta_archivo = models.FileField(upload_to='documentos/addenda/', null=True, blank=True, verbose_name='Addendum Digital (S3)')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        db_table = 'addenda'
        verbose_name = 'Addendum'
        verbose_name_plural = 'Addenda'
        unique_together = [('instrumento', 'numero_addendum')]
        ordering = ['instrumento', 'numero_addendum']

    def __str__(self) -> str:
        return f'Addendum No. {self.numero_addendum} — {self.instrumento.num_instrumento}'


class Evidencia(AuditModel):
    """
    Archivo de evidencia documental asociado a un instrumento.

    Puede acreditar hechos, comunicaciones o acuerdos relevantes:
    fotografías, correos, minutas, etc. Vinculable opcionalmente a
    una parte específica o a una escritura de poder.

    Mapea la tabla SQL: evidencias
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='evidencias',
        verbose_name='Instrumento',
    )
    archivo_fisico_origen = models.ForeignKey(
        'instruments.ArchivoFisico',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='evidencias',
        verbose_name='Archivo Físico de Origen',
    )
    tipo_evidencia = models.ForeignKey(
        'core.TipoEvidencia',
        on_delete=models.RESTRICT,
        related_name='evidencias',
        verbose_name='Tipo de Evidencia',
    )
    tipo_copia = models.ForeignKey(
        'core.TipoCopia',
        on_delete=models.RESTRICT,
        related_name='evidencias',
        verbose_name='Tipo de Copia / Validez Legal',
    )
    parte = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='evidencias',
        verbose_name='Parte Emisora',
        help_text='Parte que generó o remitió esta evidencia.',
    )
    escritura = models.ForeignKey(
        'legal.Escritura',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='evidencias',
        verbose_name='Escritura Relacionada',
    )
    nombre_archivo = models.CharField(max_length=1024, verbose_name='Nombre del Archivo')
    ruta_archivo = models.FileField(
        upload_to='documentos/evidencias/',
        verbose_name='Evidencia Digital (S3)',
        help_text='Archivo de evidencia. Almacenado cifrado en AWS S3 con AES256.',
    )
    comentario = models.TextField(verbose_name='Comentario', help_text='Contexto o descripción del contenido de la evidencia.')

    class Meta:
        db_table = 'evidencias'
        verbose_name = 'Evidencia'
        verbose_name_plural = 'Evidencias'
        ordering = ['-fecha_creacion']

    def __str__(self) -> str:
        return f'{self.tipo_evidencia} — {self.instrumento.num_instrumento}'
