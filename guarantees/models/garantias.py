"""
Modelos del app Garantías: Fianza y Pena convencional.

Fianza: póliza de garantía emitida por una afianzadora para caucionar
el cumplimiento de las obligaciones del contrato.

Pena: penalización económica calculada por incumplimiento en tiempo o
calidad de las obligaciones pactadas en el instrumento.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from audit.models.base import AuditModel


class Pena(AuditModel):
    """
    Penalización convencional aplicada por incumplimiento de una obligación
    contractual. Permite calcular el monto penalizado con base en el porcentaje
    pactado sobre el monto de referencia.

    El campo 'monto_penalizado' se calcula como:
        monto_a_penalizar × (valor_pena_porcentaje / 100)

    Mapea la tabla SQL: penas
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='penas',
        verbose_name='Instrumento',
    )

    # ── ORIGEN DE LA PENA ─────────────────────────────────────────────────────
    addendum = models.ForeignKey(
        'documents.Addendum',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='penas',
        verbose_name='Addendum de Origen',
    )
    modificatorio = models.ForeignKey(
        'documents.Modificatorio',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='penas',
        verbose_name='Modificatorio de Origen',
    )
    anexo = models.ForeignKey(
        'documents.Anexo',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='penas',
        verbose_name='Anexo de Origen',
    )
    partida = models.ForeignKey(
        'documents.Partida',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='penas',
        verbose_name='Partida Penalizada',
    )

    # ── GRANULARIDAD ──────────────────────────────────────────────────────────
    unidad_medida_penalizada = models.CharField(max_length=50, null=True, blank=True, verbose_name='Unidad de Medida Penalizada')
    cantidad_unidad_medida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Cantidad de Unidad')

    # ── CÁLCULO DE TIEMPO ─────────────────────────────────────────────────────
    dias_atraso = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Días de Atraso',
    )
    tipo_dia = models.ForeignKey(
        'core.TipoDia',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='penas',
        verbose_name='Tipo de Día',
    )
    periodo_pena = models.CharField(max_length=100, null=True, blank=True, verbose_name='Período de Pena', help_text='Ej: Diario, Semanal, Único.')

    # ── CÁLCULO MONETARIO ─────────────────────────────────────────────────────
    monto_a_penalizar = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto Base a Penalizar',
    )
    valor_pena_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Porcentaje de Pena (%)',
    )
    monto_penalizado = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Monto Penalizado (resultado)')

    # ── EVIDENCIA ─────────────────────────────────────────────────────────────
    comentario = models.TextField(null=True, blank=True, verbose_name='Comentario')
    link_factura = models.CharField(max_length=512, null=True, blank=True, verbose_name='Link / Nota de Crédito')

    class Meta:
        db_table = 'penas'
        verbose_name = 'Pena Convencional'
        verbose_name_plural = 'Penas Convencionales'
        ordering = ['-fecha_creacion']

    def __str__(self) -> str:
        return f'Pena {self.valor_pena_porcentaje}% — {self.instrumento.num_instrumento}'


class Fianza(AuditModel):
    """
    Póliza de fianza emitida por una afianzadora para garantizar el cumplimiento
    de las obligaciones contractuales de una de las partes.

    Incluye vigencia (fecha_inicio y fecha_fin) para habilitar alertas
    de vencimiento de garantías y la ruta al documento digital de la póliza.

    Mapea la tabla SQL: fianzas
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='fianzas',
        verbose_name='Instrumento',
    )
    tipo_fianza = models.ForeignKey(
        'core.TipoFianza',
        on_delete=models.RESTRICT,
        related_name='fianzas',
        verbose_name='Tipo de Fianza',
    )
    tipo_obligacion = models.ForeignKey(
        'core.TipoObligacion',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fianzas',
        verbose_name='Tipo de Obligación',
    )
    afianzadora = models.ForeignKey(
        'parties.Parte',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fianzas_emitidas',
        verbose_name='Afianzadora (Fiador)',
        help_text='Empresa afianzadora o aseguradora que emitió la póliza.',
    )
    pena = models.ForeignKey(
        Pena,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='fianzas',
        verbose_name='Pena Garantizada',
    )

    # ── DATOS DE LA PÓLIZA ────────────────────────────────────────────────────
    numero_poliza = models.CharField(max_length=100, verbose_name='Número de Póliza')
    monto = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Monto Afianzado',
    )
    descripcion_obligacion = models.TextField(null=True, blank=True, verbose_name='Descripción de la Obligación')
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name='Inicio de Vigencia')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fin de Vigencia')

    # ── ARCHIVO DIGITAL ───────────────────────────────────────────────────────
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre de Archivo')
    ruta_archivo = models.FileField(
        upload_to='garantias/fianzas/',
        null=True, blank=True,
        verbose_name='Póliza Digital (S3)',
        help_text='PDF del documento de la póliza. Se almacena cifrado en AWS S3 con AES256.',
    )

    class Meta:
        db_table = 'fianzas'
        verbose_name = 'Fianza'
        verbose_name_plural = 'Fianzas'
        ordering = ['fecha_fin']

    def __str__(self) -> str:
        return f'Póliza {self.numero_poliza} — {self.instrumento.num_instrumento}'
