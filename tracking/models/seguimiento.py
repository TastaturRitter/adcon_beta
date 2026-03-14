"""
Modelos del app Seguimientos (tracking): Hito, Actividad, Incidencia y Entrega.

Estas entidades implementan la gestión operativa del ciclo de vida contractual:
- Hito: evento clave con deadline y estatus dentro del contrato.
- Actividad: tarea concreta asignada a una parte para cumplir un hito.
- Incidencia: desviación o problema detectado durante la ejecución.
- Entrega: registro formal de las entregas parciales o totales del objeto del contrato.
"""

from django.db import models
from django.core.validators import MinValueValidator

from audit.models.base import AuditModel


class Hito(AuditModel):
    """
    Evento contractual clave con una fecha límite (deadline) definida en el contrato.

    Ej: 'Pago de Anticipo', 'Entrega de Reportes Mensuales', 'Renovación del Convenio'.
    El campo 'justificacion_atraso' documenta formalmente los incumplimientos
    para efectos de penalización o negociación contractual.

    Mapea la tabla SQL: hitos
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='hitos',
        verbose_name='Instrumento',
    )
    tipo_hito = models.ForeignKey(
        'core.TipoHito',
        on_delete=models.RESTRICT,
        related_name='hitos',
        verbose_name='Tipo de Hito',
    )
    estatus_hito = models.ForeignKey(
        'core.EstatusHito',
        on_delete=models.RESTRICT,
        related_name='hitos',
        verbose_name='Estatus',
    )
    prioridad_hito = models.ForeignKey(
        'core.PrioridadHito',
        on_delete=models.RESTRICT,
        related_name='hitos',
        verbose_name='Prioridad',
    )
    titulo = models.CharField(max_length=1024, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_meta = models.DateField(verbose_name='Fecha Límite (Deadline)', help_text='Fecha contractual en que debe cumplirse el hito.')
    fecha_cumplimiento = models.DateField(null=True, blank=True, verbose_name='Fecha Real de Cumplimiento')
    justificacion_atraso = models.TextField(null=True, blank=True, verbose_name='Justificación del Atraso')

    class Meta:
        db_table = 'hitos'
        verbose_name = 'Hito'
        verbose_name_plural = 'Hitos'
        ordering = ['fecha_meta']

    def __str__(self) -> str:
        return f'{self.titulo} — {self.instrumento.num_instrumento}'


class Actividad(AuditModel):
    """
    Tarea concreta asignada a un responsable para dar cumplimiento a un hito.

    Una actividad es la unidad operativa mínima del seguimiento contractual.
    Tiene un responsable directo (parte vinculada) y fechas de inicio y fin.

    Mapea la tabla SQL: actividades
    """

    hito = models.ForeignKey(
        Hito,
        on_delete=models.CASCADE,
        related_name='actividades',
        verbose_name='Hito',
    )
    tipo_actividad = models.ForeignKey(
        'core.TipoActividad',
        on_delete=models.RESTRICT,
        related_name='actividades',
        verbose_name='Tipo de Actividad',
    )
    estatus_actividad = models.ForeignKey(
        'core.EstatusActividad',
        on_delete=models.RESTRICT,
        related_name='actividades',
        verbose_name='Estatus',
    )
    responsable = models.ForeignKey(
        'parties.Parte',
        on_delete=models.RESTRICT,
        related_name='actividades_asignadas',
        verbose_name='Responsable',
        help_text='Parte (persona u organización) obligada a ejecutar esta actividad.',
    )
    prioridad_actividad = models.ForeignKey(
        'core.PrioridadActividad',
        on_delete=models.RESTRICT,
        related_name='actividades',
        verbose_name='Prioridad',
    )
    titulo = models.CharField(max_length=1024, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name='Fecha de Inicio')
    fecha_fin = models.DateField(null=True, blank=True, verbose_name='Fecha de Fin')

    class Meta:
        db_table = 'actividades'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['fecha_fin', 'titulo']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fecha_fin__isnull=True) | models.Q(fecha_inicio__isnull=True) | models.Q(fecha_fin__gte=models.F('fecha_inicio')),
                name='chk_fechas_actividad',
            )
        ]

    def __str__(self) -> str:
        return f'{self.titulo} — Hito: {self.hito}'


class Incidencia(AuditModel):
    """
    Desviación, problema o riesgo detectado durante la ejecución del contrato.

    Incluye valoración económica del impacto (monto_impacto) y del beneficio
    obtenido al resolverlo (monto_beneficio), permitiendo análisis costo-beneficio
    de la gestión contractual.

    Mapea la tabla SQL: incidencias
    """

    actividad = models.ForeignKey(
        Actividad,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='incidencias',
        verbose_name='Actividad Relacionada',
    )
    tipo_incidencia = models.ForeignKey(
        'core.TipoIncidencia',
        on_delete=models.RESTRICT,
        related_name='incidencias',
        verbose_name='Tipo de Incidencia',
    )
    estatus_incidencia = models.ForeignKey(
        'core.EstatusIncidencia',
        on_delete=models.RESTRICT,
        related_name='incidencias',
        verbose_name='Estatus',
    )
    gravedad_incidencia = models.ForeignKey(
        'core.GravedadIncidencia',
        on_delete=models.RESTRICT,
        related_name='incidencias',
        verbose_name='Gravedad',
    )
    titulo = models.CharField(max_length=1024, verbose_name='Título')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    nombre_archivo = models.CharField(max_length=1024, null=True, blank=True, verbose_name='Nombre de Archivo')
    ruta_archivo = models.FileField(upload_to='seguimiento/incidencias/', null=True, blank=True, verbose_name='Evidencia de Incidencia (S3)')
    monto_impacto = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Monto de Impacto', help_text='Costo o riesgo económico de la incidencia.')
    monto_beneficio = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name='Monto de Beneficio', help_text='Valor económico generado al resolver la incidencia.')
    fecha_ocurrencia = models.DateField(verbose_name='Fecha de Ocurrencia')
    fecha_solucion = models.DateField(null=True, blank=True, verbose_name='Fecha de Solución')

    class Meta:
        db_table = 'incidencias'
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'
        ordering = ['-fecha_ocurrencia']

    def __str__(self) -> str:
        return f'{self.titulo} [{self.gravedad_incidencia}]'


class Entrega(AuditModel):
    """
    Registro formal de una entrega parcial o total del objeto del contrato.

    Permite comparar la fecha programada (contractual) contra la fecha real
    de recepción, habilitando el cálculo automático de atrasos y la
    activación de penalizaciones correspondientes.

    Mapea la tabla SQL: entregas
    """

    instrumento = models.ForeignKey(
        'instruments.Instrumento',
        on_delete=models.CASCADE,
        related_name='entregas',
        verbose_name='Instrumento',
    )
    tipo_entrega = models.ForeignKey(
        'core.TipoEntrega',
        on_delete=models.RESTRICT,
        related_name='entregas',
        verbose_name='Tipo de Entrega',
    )
    estatus_entrega = models.ForeignKey(
        'core.EstatusEntrega',
        on_delete=models.RESTRICT,
        related_name='entregas',
        verbose_name='Estatus',
    )
    numero_entrega = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Número de Entrega')
    total_entregas_esperadas = models.IntegerField(null=True, blank=True, verbose_name='Total de Entregas Esperadas')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_programada = models.DateField(verbose_name='Fecha Programada (Contractual)')
    fecha_real = models.DateField(null=True, blank=True, verbose_name='Fecha Real de Recepción')

    class Meta:
        db_table = 'entregas'
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ['instrumento', 'numero_entrega']

    def __str__(self) -> str:
        return f'Entrega #{self.numero_entrega} — {self.instrumento.num_instrumento}'
