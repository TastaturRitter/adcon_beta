"""
Modelos del app Instrumentos: núcleo del sistema de gestión de contratos Adcon.

Contiene el modelo Instrumento (corazón del CLM) y sus entidades relacionadas:
Concurso (proceso de adjudicación), InstrumentoParte (vínculos contractuales),
ArchivoFisico (archivo físico de contratos), y las especializaciones contractuales
(Arrendamiento, CompraventaInmueble, ServicioPrestado, SuministroMercancia)
que implementan el patrón de herencia 1:1.
"""

from django.db import models
from django.core.validators import MinValueValidator

from audit.models.base import AuditModel


class Concurso(AuditModel):
    """
    Proceso de adjudicación (licitación, concurso o adjudicación directa)
    que precede y respalda legalmente la firma de uno o más instrumentos.

    Vincula el instrumento con su fundamento legal de contratación,
    cumpliendo los requisitos de la Ley de Adquisiciones y normas internas.

    Mapea la tabla SQL: concursos
    """

    tipo_concurso = models.ForeignKey(
        'core.TipoConcurso',
        on_delete=models.RESTRICT,
        related_name='concursos',
        verbose_name='Tipo de Concurso',
        help_text='Modalidad de adjudicación: Licitación Pública, Invitación a 3, Adjudicación Directa.',
    )
    numero_concurso = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Número de Concurso',
        help_text='Clave oficial del proceso de contratación, único en el sistema.',
    )
    titulo = models.CharField(
        max_length=1024,
        verbose_name='Título',
        help_text='Nombre descriptivo del concurso tal como aparece en las bases.',
    )
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    fecha_publicacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Publicación')
    fecha_presentacion = models.DateField(null=True, blank=True, verbose_name='Fecha de Presentación')
    fecha_fallo = models.DateField(verbose_name='Fecha de Fallo / Adjudicación')
    presupuesto_base = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Presupuesto Base',
        help_text='Monto máximo presupuestal publicado en las bases del concurso.',
    )
    fundamento_legal = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Fundamento Legal',
        help_text='Artículo o ley que respalda la elección del tipo de concurso.',
    )

    class Meta:
        db_table = 'concursos'
        verbose_name = 'Concurso'
        verbose_name_plural = 'Concursos'
        ordering = ['-fecha_fallo']

    def __str__(self) -> str:
        return f'[{self.numero_concurso}] {self.titulo}'


class Instrumento(AuditModel):
    """
    Modelo central del sistema CLM Adcon. Representa un instrumento jurídico
    (contrato, convenio, acuerdo, etc.) en su ciclo de vida completo.

    Es el eje de todas las relaciones del sistema: partes, documentos,
    anexos, garantías, hitos de seguimiento y auditoría convergen aquí.
    La clave 'num_instrumento' lo identifica de forma única en el sistema.

    Mapea la tabla SQL: instrumentos
    """

    num_instrumento = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de Instrumento',
        help_text='Clave única que identifica al instrumento en el CLM. Ej: CONT-2025-001.',
    )
    titulo = models.CharField(
        max_length=1024,
        verbose_name='Título',
        help_text='Nombre oficial completo del instrumento jurídico.',
    )
    dato_maestro_cliente = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Dato Maestro (Cliente)',
        help_text='Identificador en sistemas externos del cliente (SAP, ERP) para conciliación.',
    )

    # ── CLASIFICACIÓN ─────────────────────────────────────────────────────────
    tipo_instrumento = models.ForeignKey(
        'core.TipoInstrumento',
        on_delete=models.RESTRICT,
        related_name='instrumentos',
        verbose_name='Tipo de Instrumento',
    )
    estatus_instrumento = models.ForeignKey(
        'core.EstatusInstrumento',
        on_delete=models.RESTRICT,
        related_name='instrumentos',
        verbose_name='Estatus',
        help_text='Estado actual del ciclo de vida: Borrador, Vigente, Vencido, Cancelado.',
    )
    prioridad_instrumento = models.ForeignKey(
        'core.PrioridadInstrumento',
        on_delete=models.RESTRICT,
        related_name='instrumentos',
        verbose_name='Prioridad',
    )
    tipo_firma = models.ForeignKey(
        'core.TipoFirma',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instrumentos',
        verbose_name='Tipo de Firma',
    )
    tipo_contraprestacion = models.ForeignKey(
        'core.TipoContraprestacion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instrumentos',
        verbose_name='Tipo de Contraprestación',
    )

    # ── VINCULACIÓN ───────────────────────────────────────────────────────────
    concurso = models.ForeignKey(
        Concurso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instrumentos',
        verbose_name='Concurso de Origen',
        help_text='Proceso de adjudicación que originó este contrato. Puede ser nulo en contratos privados.',
    )
    es_renovacion_automatica = models.BooleanField(
        default=False,
        verbose_name='¿Renovación Automática?',
        help_text='Si True, el sistema generará alertas de vencimiento para tramitar la renovación.',
    )
    instrumento_vinculado = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='instrumentos_dependientes',
        verbose_name='Instrumento Vinculado',
        help_text='Contrato principal al que este instrumento está subordinado (ej: un Anexo del principal).',
    )

    # ── FECHAS CLAVE ──────────────────────────────────────────────────────────
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio',
        help_text='Fecha a partir de la cual el instrumento produce efectos jurídicos.',
    )
    fecha_termino = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Término',
        help_text='Fecha de vencimiento pactada. NULL indica vigencia indefinida.',
    )
    fecha_firma = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Firma',
    )

    # ── FACTURACIÓN ───────────────────────────────────────────────────────────
    rfc_facturacion = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        verbose_name='RFC de Facturación',
        help_text='RFC al que se deben emitir las facturas electrónicas de este contrato.',
    )
    comentarios = models.TextField(
        null=True,
        blank=True,
        verbose_name='Comentarios',
    )

    # AuditModel provee: creado_por, fecha_creacion
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización',
    )

    class Meta:
        db_table = 'instrumentos'
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'
        ordering = ['-fecha_creacion']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(fecha_termino__isnull=True) | models.Q(fecha_termino__gte=models.F('fecha_inicio')),
                name='chk_fechas_instrumento',
            )
        ]

    def __str__(self) -> str:
        return f'[{self.num_instrumento}] {self.titulo}'


class InstrumentoParte(AuditModel):
    """
    Tabla de vinculación entre un instrumento y las partes que intervienen en él.

    Implementa el patrón de Rol: una misma parte puede ser 'Arrendador' en un
    contrato y 'Contratista' en otro. La restricción UNIQUE (instrumento, parte, rol)
    evita duplicar el mismo rol para la misma parte en el mismo contrato.

    Mapea la tabla SQL: instrumento_parte
    """

    instrumento = models.ForeignKey(
        Instrumento,
        on_delete=models.CASCADE,
        related_name='partes_vinculadas',
        verbose_name='Instrumento',
    )
    parte = models.ForeignKey(
        'parties.Parte',
        on_delete=models.CASCADE,
        related_name='instrumentos_vinculados',
        verbose_name='Parte',
    )
    rol = models.ForeignKey(
        'core.Rol',
        on_delete=models.RESTRICT,
        related_name='vinculos',
        verbose_name='Rol en el Instrumento',
        help_text='Papel jurídico de la parte en este contrato: Arrendador, Contratista, Garante, etc.',
    )
    domicilio_notificaciones = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vinculos_instrumento',
        verbose_name='Domicilio para Notificaciones',
        help_text='Domicilio convencional pactado en este contrato para recibir notificaciones.',
    )
    es_principal_para_rol = models.BooleanField(
        default=False,
        verbose_name='¿Principal para el Rol?',
        help_text='Indica si esta parte es la principal dentro de este rol (ej: Arrendatario Principal).',
    )
    fecha_asociacion = models.DateField(
        verbose_name='Fecha de Asociación',
        help_text='Fecha en que esta parte se vinculó formalmente al instrumento.',
    )

    class Meta:
        db_table = 'instrumento_parte'
        verbose_name = 'Instrumento-Parte'
        verbose_name_plural = 'Instrumentos-Partes'
        unique_together = [('instrumento', 'parte', 'rol')]

    def __str__(self) -> str:
        return f'{self.parte} — {self.rol} en {self.instrumento.num_instrumento}'


class ArchivoFisico(AuditModel):
    """
    Registro del expediente físico de un instrumento: carpetas, fojas y cajas
    almacenadas en el archivo institucional.

    Permite localizar rápidamente la documentación tangible del contrato
    cuando se requiere una consulta in situ o una diligencia legal.

    Mapea la tabla SQL: archivos_fisicos
    """

    instrumento = models.ForeignKey(
        Instrumento,
        on_delete=models.CASCADE,
        related_name='archivos_fisicos',
        verbose_name='Instrumento',
    )
    nombre = models.CharField(
        max_length=255,
        verbose_name='Nombre del Paquete Físico',
        help_text='Ej: "Carpeta Arrendamiento 2025" o "Foja 10 del Libro de Actas".',
    )
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    cantidad = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad',
        help_text='Número de fojas, carpetas u hojas contenidas en el paquete.',
    )
    ubicacion = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Ubicación Física',
        help_text='Referencia de localización en el archivo. Ej: "Pasillo B, Estante 4".',
    )
    caja = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Caja',
        help_text='Identificador de la caja de archivo. Ej: "Caja-2025-001".',
    )
    fecha_ingreso = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Ingreso al Archivo',
    )

    class Meta:
        db_table = 'archivos_fisicos'
        verbose_name = 'Archivo Físico'
        verbose_name_plural = 'Archivos Físicos'
        ordering = ['instrumento', 'nombre']

    def __str__(self) -> str:
        return f'{self.nombre} — {self.instrumento.num_instrumento}'


class Arrendamiento(AuditModel):
    """
    Especialización 1:1 de Instrumento para contratos de arrendamiento inmobiliario.

    Extiende el instrumento base con las condiciones particulares del arrendamiento:
    inmueble objeto del contrato, monto de renta, depósito, duración y cláusulas
    específicas como actualización por INPC y póliza de responsabilidad civil.

    Mapea la tabla SQL: arrendamientos
    """

    instrumento = models.OneToOneField(
        Instrumento,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='arrendamiento',
        verbose_name='Instrumento Base',
    )
    inmueble = models.ForeignKey(
        'assets.Inmueble',
        on_delete=models.RESTRICT,
        related_name='arrendamientos',
        verbose_name='Inmueble',
        help_text='Bien inmueble que es objeto del contrato de arrendamiento.',
    )
    tipo_garantia = models.ForeignKey(
        'core.TipoGarantiaArrendamiento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arrendamientos',
        verbose_name='Tipo de Garantía',
    )
    meses_arrendamiento = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Duración (meses)',
        help_text='Plazo total del arrendamiento expresado en meses.',
    )
    fecha_pago_renta = models.DateField(
        verbose_name='Fecha de Pago de Renta',
        help_text='Día del mes en que debe cubrirse la renta. Ej: 5 de cada mes.',
    )
    monto_renta_sin_iva = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Monto de Renta (sin IVA)',
    )
    monto_deposito = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Depósito en Garantía',
    )
    actualizacion_renta_inpc = models.BooleanField(
        default=False,
        verbose_name='¿Actualización por INPC?',
        help_text='Si True, la renta se actualiza anualmente con base en el Índice Nacional de Precios al Consumidor.',
    )
    poliza_responsabilidad_civil = models.BooleanField(
        default=False,
        verbose_name='¿Requiere Póliza RC?',
        help_text='Si True, el arrendatario debe contratar y mantener vigente una póliza de responsabilidad civil.',
    )

    class Meta:
        db_table = 'arrendamientos'
        verbose_name = 'Arrendamiento'
        verbose_name_plural = 'Arrendamientos'

    def __str__(self) -> str:
        return f'Arrendamiento — {self.instrumento.num_instrumento}'


class CompraventaInmueble(AuditModel):
    """
    Especialización 1:1 de Instrumento para contratos de compraventa inmobiliaria.

    Incluye tanto promesas de compraventa como contratos definitivos,
    diferenciados por el campo es_promesa_contrato.

    Mapea la tabla SQL: compraventas_inmuebles
    """

    instrumento = models.OneToOneField(
        Instrumento,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='compraventa',
        verbose_name='Instrumento Base',
    )
    inmueble = models.ForeignKey(
        'assets.Inmueble',
        on_delete=models.RESTRICT,
        related_name='compraventas',
        verbose_name='Inmueble',
    )
    precio_sin_iva = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio de Venta (sin IVA)',
    )
    deposito_garantia = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
        verbose_name='Depósito en Garantía',
    )
    es_promesa_contrato = models.BooleanField(
        default=False,
        verbose_name='¿Es Promesa de Contrato?',
        help_text='True = Promesa de compraventa (pre-contrato). False = Contrato definitivo de compraventa.',
    )
    plazo_pago_dias = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Plazo de Pago (días)',
    )
    fecha_firma_contrato_previo = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Firma de la Promesa',
        help_text='Si es promesa, fecha en que se firmó. Importante para calcular plazos de formalización.',
    )

    class Meta:
        db_table = 'compraventas_inmuebles'
        verbose_name = 'Compraventa de Inmueble'
        verbose_name_plural = 'Compraventas de Inmuebles'

    def __str__(self) -> str:
        return f'Compraventa — {self.instrumento.num_instrumento}'


class ServicioPrestado(AuditModel):
    """
    Especialización 1:1 de Instrumento para contratos de prestación de servicios.

    Captura las condiciones financieras y operativas del servicio:
    honorarios, frecuencia de pago, entregables y cumplimiento del REPSE
    (Registro de Prestadoras de Servicios u Obras Especializadas).

    Mapea la tabla SQL: servicios_prestados
    """

    instrumento = models.OneToOneField(
        Instrumento,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='servicio_prestado',
        verbose_name='Instrumento Base',
    )
    honorarios_monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Monto de Honorarios',
    )
    frecuencia_pago = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Frecuencia de Pago',
        help_text='Ej: Mensual, Quincenal, Por Entregable.',
    )
    contraprestacion_total_monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Contraprestación Total (Techo)',
        help_text='Monto máximo presupuestado para la vigencia total del contrato.',
    )
    tipo_entregable = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Tipo de Entregable',
        help_text='Ej: "Reporte Mensual", "Consultoría Estratégica", "Auditoría".',
    )
    fecha_entregable = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Entregable',
    )
    requiere_repse = models.BooleanField(
        default=False,
        verbose_name='¿Requiere REPSE?',
        help_text='Si True, el contratista debe estar registrado en el REPSE conforme a la reforma LSS 2021.',
    )
    numero_registro_repse = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Número de Registro REPSE',
    )

    class Meta:
        db_table = 'servicios_prestados'
        verbose_name = 'Servicio Prestado'
        verbose_name_plural = 'Servicios Prestados'

    def __str__(self) -> str:
        return f'Servicio — {self.instrumento.num_instrumento}'


class SuministroMercancia(AuditModel):
    """
    Especialización 1:1 de Instrumento para contratos de suministro de bienes o mercancías.

    Soporta tanto contratos cerrados (monto fijo) como contratos abiertos
    (presupuesto con piso y techo), siguiendo la lógica de adquisiciones públicas
    y privadas.

    Mapea la tabla SQL: suministros_mercancias
    """

    instrumento = models.OneToOneField(
        Instrumento,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='suministro',
        verbose_name='Instrumento Base',
    )
    domicilio_entrega = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        related_name='suministros',
        verbose_name='Domicilio de Entrega',
        help_text='Dirección a la que deben entregarse los bienes objeto del contrato.',
    )

    # ── CONTRATO CERRADO ──────────────────────────────────────────────────────
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Subtotal Fijo')
    monto_iva = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='IVA Fijo')
    monto_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Total Fijo')

    # ── CONTRATO ABIERTO — TECHO ──────────────────────────────────────────────
    maximo_subtotal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Máximo Subtotal')
    maximo_iva = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Máximo IVA')
    maximo_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Máximo Total (Techo)')

    # ── CONTRATO ABIERTO — PISO ───────────────────────────────────────────────
    minimo_subtotal = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Mínimo Subtotal')
    minimo_iva = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Mínimo IVA')
    minimo_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Mínimo Total (Piso)')

    # ── CONDICIONES ───────────────────────────────────────────────────────────
    anticipo_monto = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0, verbose_name='Anticipo')
    fecha_entrega = models.DateField(null=True, blank=True, verbose_name='Fecha de Entrega Pactada')

    class Meta:
        db_table = 'suministros_mercancias'
        verbose_name = 'Suministro de Mercancía'
        verbose_name_plural = 'Suministros de Mercancías'
        constraints = [
            models.CheckConstraint(
                condition=models.Q(maximo_total__isnull=True) | models.Q(minimo_total__isnull=True) | models.Q(maximo_total__gte=models.F('minimo_total')),
                name='chk_presupuesto_min_max',
            ),
        ]

    def __str__(self) -> str:
        return f'Suministro — {self.instrumento.num_instrumento}'


class ActoCorporativo(AuditModel):
    """
    Registro de un acto corporativo (asamblea, junta de consejo) relacionado
    con un instrumento del sistema. Incluye datos registrales de libros
    corporativos y la composición del capital en ese momento histórico.

    Mapea la tabla SQL: actos_corporativos
    """

    instrumento = models.ForeignKey(
        Instrumento,
        on_delete=models.CASCADE,
        related_name='actos_corporativos',
        verbose_name='Instrumento',
    )
    tipo_convocatoria = models.ForeignKey(
        'core.TipoConvocatoria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actos',
        verbose_name='Tipo de Convocatoria',
    )
    organo_administracion = models.ForeignKey(
        'core.OrganoAdministracion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actos',
        verbose_name='Órgano de Administración',
    )
    domicilio_social = models.ForeignKey(
        'addresses.Domicilio',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='actos_corporativos',
        verbose_name='Domicilio Social',
    )

    # ── LIBROS CORPORATIVOS ───────────────────────────────────────────────────
    libro_asambleas_foja = models.CharField(max_length=100, null=True, blank=True, verbose_name='Foja Libro de Asambleas')
    libro_var_capital_foja = models.CharField(max_length=100, null=True, blank=True, verbose_name='Foja Libro de Variaciones de Capital')
    libro_reg_acc_foja = models.CharField(max_length=100, null=True, blank=True, verbose_name='Foja Libro Registro de Acciones')

    # ── DETALLES DEL ACTO ─────────────────────────────────────────────────────
    fecha_acto = models.DateField(verbose_name='Fecha del Acto')
    contenido = models.TextField(verbose_name='Contenido', help_text='Resumen o texto de los acuerdos tomados en el acto.')
    capital_social_fijo = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0, verbose_name='Capital Social Fijo')
    capital_social_variable = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, default=0, verbose_name='Capital Social Variable')
    clausula_extranjeros = models.BooleanField(default=False, verbose_name='¿Cláusula de Extranjeros?', help_text='Indica si se adoptó la cláusula de admisión de extranjeros (Cláusula Calvo).')
    restricciones_venta_acciones = models.TextField(null=True, blank=True, verbose_name='Restricciones de Venta de Acciones')

    class Meta:
        db_table = 'actos_corporativos'
        verbose_name = 'Acto Corporativo'
        verbose_name_plural = 'Actos Corporativos'
        ordering = ['-fecha_acto']

    def __str__(self) -> str:
        return f'Acto {self.fecha_acto} — {self.instrumento.num_instrumento}'


class AccionistaEnActo(models.Model):
    """
    Registro histórico de la participación accionaria de cada socio
    en un acto corporativo específico (snapshot al momento del acto).

    Permite reconstruir el quórum y la distribución del capital
    en cualquier asamblea pasada con fidelidad histórica.

    Mapea la tabla SQL: accionistas_en_acto
    """

    acto_corporativo = models.ForeignKey(
        ActoCorporativo,
        on_delete=models.CASCADE,
        related_name='accionistas',
        verbose_name='Acto Corporativo',
    )
    socio = models.ForeignKey(
        'parties.Parte',
        on_delete=models.RESTRICT,
        related_name='actos_como_socio',
        verbose_name='Socio',
    )
    total_acciones = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Total de Acciones')
    acciones_capital_fijo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Acciones Capital Fijo')
    acciones_capital_variable = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Acciones Capital Variable')
    acciones_otro_tipo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Acciones Otro Tipo')
    rfc_socio_momentaneo = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        verbose_name='RFC del Socio (histórico)',
        help_text='Captura histórica del RFC tal como estaba al momento del acto.',
    )

    class Meta:
        db_table = 'accionistas_en_acto'
        verbose_name = 'Accionista en Acto'
        verbose_name_plural = 'Accionistas en Acto'

    def __str__(self) -> str:
        return f'{self.socio} en acto {self.acto_corporativo_id}'
