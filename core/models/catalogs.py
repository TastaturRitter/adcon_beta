"""
Modelos de catálogos generales del sistema Adcon.

Estas tablas de referencia (lookup tables) proveen los valores controlados
que clasifican los instrumentos, partes, garantías, actividades y demás
entidades del CLM. Todos heredan de AuditModel para uniformidad de auditoría.

Regla de negocio: los catálogos son mantenidos exclusivamente por
administradores del sistema. No deben ser modificados desde la UI de usuarios.
"""

from django.db import models
from django.core.validators import MinValueValidator

from audit.models.base import AuditModel


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE TIPO (types_*)
# ─────────────────────────────────────────────────────────────────────────────

class TipoActividad(AuditModel):
    """
    Catálogo de tipos de actividad dentro del seguimiento de instrumentos.
    Ej: 'Revisión Jurídica', 'Notificación', 'Entrega de Documentos'.
    Mapea la tabla SQL: tipos_actividad
    """
    nombre = models.CharField(
        max_length=100, unique=True,
        verbose_name='Nombre',
        help_text='Nombre único del tipo de actividad.',
    )
    descripcion = models.TextField(
        null=True, blank=True,
        verbose_name='Descripción',
        help_text='Detalle adicional sobre el propósito de este tipo de actividad.',
    )

    class Meta:
        db_table = 'tipos_actividad'
        verbose_name = 'Tipo de Actividad'
        verbose_name_plural = 'Tipos de Actividad'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoAddendum(AuditModel):
    """
    Catálogo de clasificaciones para addenda contractuales.
    Ej: 'Técnico', 'Económico', 'Administrativo'.
    Mapea la tabla SQL: tipos_addendum
    """
    nombre = models.CharField(
        max_length=100, unique=True,
        verbose_name='Nombre',
    )
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_addendum'
        verbose_name = 'Tipo de Addendum'
        verbose_name_plural = 'Tipos de Addendum'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoAdminInstrumento(AuditModel):
    """
    Catálogo de formas de administración aplicables a un instrumento contractual.
    Ej: 'Administración Directa', 'Subcontratación'.
    Mapea la tabla SQL: tipos_admin_instrumento
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_admin_instrumento'
        verbose_name = 'Tipo de Administración de Instrumento'
        verbose_name_plural = 'Tipos de Administración de Instrumento'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoConcurso(AuditModel):
    """
    Catálogo de modalidades de concurso o licitación para la adjudicación de contratos.
    Ej: 'Licitación Pública Nacional', 'Invitación a 3', 'Adjudicación Directa'.
    Mapea la tabla SQL: tipos_concurso
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    clave_oficial = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name='Clave Oficial',
        help_text='Abreviatura oficial para reportes cortos. Ej: LPN, I3P, AD.',
    )
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_concurso'
        verbose_name = 'Tipo de Concurso'
        verbose_name_plural = 'Tipos de Concurso'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoContraprestacion(AuditModel):
    """
    Catálogo de formas de contraprestación pactada en un instrumento.
    Ej: 'Pago en Efectivo', 'Compensación en Especie', 'Gratuito'.
    Mapea la tabla SQL: tipos_contraprestacion
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_contraprestacion'
        verbose_name = 'Tipo de Contraprestación'
        verbose_name_plural = 'Tipos de Contraprestación'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoConvocatoria(AuditModel):
    """
    Catálogo de tipos de convocatoria para asambleas y reuniones de órganos de gobierno.
    Contiene las reglas de negocio sobre plazos mínimos de anticipación por tipo de sesión.
    Mapea la tabla SQL: tipos_convocatoria
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    # Reglas de negocio: días mínimos de anticipación requeridos por tipo de convocatoria
    plazo_previo_agoa_dias = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Plazo AGOA (días)',
        help_text='Días mínimos de anticipación para Asamblea General Ordinaria.',
    )
    plazo_previo_agea_dias = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Plazo AGEA (días)',
        help_text='Días mínimos de anticipación para Asamblea General Extraordinaria.',
    )
    plazo_previo_junta_consejo_dias = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Plazo Junta de Consejo (días)',
        help_text='Días mínimos de anticipación para Junta de Consejo de Administración.',
    )

    class Meta:
        db_table = 'tipos_convocatoria'
        verbose_name = 'Tipo de Convocatoria'
        verbose_name_plural = 'Tipos de Convocatoria'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoCopia(AuditModel):
    """
    Catálogo de validez legal de copias de documentos.
    Ej: 'Original', 'Copia Certificada', 'Copia Simple'.
    Mapea la tabla SQL: tipos_copia
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_copia'
        verbose_name = 'Tipo de Copia'
        verbose_name_plural = 'Tipos de Copia'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoDia(AuditModel):
    """
    Catálogo de clasificación de días para cómputo de plazos contractuales.
    Ej: 'Naturales', 'Hábiles'.
    Mapea la tabla SQL: tipos_dia
    """
    nombre = models.CharField(max_length=20, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_dia'
        verbose_name = 'Tipo de Día'
        verbose_name_plural = 'Tipos de Día'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoEntrega(AuditModel):
    """
    Catálogo de modalidades de entrega dentro de un contrato.
    Ej: 'Entrega Parcial', 'Entrega Total', 'Recepción Técnica'.
    Mapea la tabla SQL: tipos_entrega
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_entrega'
        verbose_name = 'Tipo de Entrega'
        verbose_name_plural = 'Tipos de Entrega'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoEscritura(AuditModel):
    """
    Catálogo de tipos de escritura pública notarial.
    Ej: 'Poder General', 'Poder Especial', 'Acta Constitutiva'.
    Mapea la tabla SQL: tipos_escritura
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_escritura'
        verbose_name = 'Tipo de Escritura'
        verbose_name_plural = 'Tipos de Escritura'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoEvidencia(AuditModel):
    """
    Catálogo de tipos de evidencia documental asociable a los instrumentos.
    Ej: 'Fotografía', 'Correo Electrónico', 'Minuta', 'Acta'.
    Mapea la tabla SQL: tipos_evidencia
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_evidencia'
        verbose_name = 'Tipo de Evidencia'
        verbose_name_plural = 'Tipos de Evidencia'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoFianza(AuditModel):
    """
    Catálogo de tipos de fianza o garantía que pueden caucionar un contrato.
    Ej: 'Fianza de Cumplimiento', 'Fianza de Anticipo', 'Fianza de Vicios Ocultos'.
    Mapea la tabla SQL: tipos_fianza
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_fianza'
        verbose_name = 'Tipo de Fianza'
        verbose_name_plural = 'Tipos de Fianza'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoFirma(AuditModel):
    """
    Catálogo de modalidades de firma de un instrumento legal.
    Ej: 'Firma Autógrafa', 'Firma Electrónica Avanzada (e.firma)'.
    Mapea la tabla SQL: tipos_firma
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_firma'
        verbose_name = 'Tipo de Firma'
        verbose_name_plural = 'Tipos de Firma'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoGarantiaArrendamiento(AuditModel):
    """
    Catálogo de tipos de garantía aplicables específicamente a contratos de arrendamiento.
    Ej: 'Depósito en Efectivo', 'Aval', 'Fianza'.
    Mapea la tabla SQL: tipos_garantia_arrendamiento
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_garantia_arrendamiento'
        verbose_name = 'Tipo de Garantía de Arrendamiento'
        verbose_name_plural = 'Tipos de Garantía de Arrendamiento'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoHito(AuditModel):
    """
    Catálogo de tipos de hito o evento clave dentro del ciclo de vida de un contrato.
    Ej: 'Pago', 'Entrega', 'Renovación', 'Vencimiento'.
    Mapea la tabla SQL: tipos_hito
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_hito'
        verbose_name = 'Tipo de Hito'
        verbose_name_plural = 'Tipos de Hito'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoIncidencia(AuditModel):
    """
    Catálogo de categorías de incidencias o desviaciones contractuales.
    Ej: 'Incumplimiento de Entrega', 'Defecto de Calidad', 'Retraso en Pago'.
    Mapea la tabla SQL: tipos_incidencia
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_incidencia'
        verbose_name = 'Tipo de Incidencia'
        verbose_name_plural = 'Tipos de Incidencia'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoInmueble(AuditModel):
    """
    Catálogo de clasificaciones de inmuebles gestionados como activos.
    Ej: 'Casa Habitación', 'Local Comercial', 'Terreno', 'Bodega'.
    Mapea la tabla SQL: tipos_inmueble
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_inmueble'
        verbose_name = 'Tipo de Inmueble'
        verbose_name_plural = 'Tipos de Inmueble'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoInstrumento(AuditModel):
    """
    Catálogo maestro de tipos de instrumento jurídico gestionados por Adcon.
    Ej: 'Contrato de Arrendamiento', 'Convenio de Colaboración', 'Contrato de Obra'.
    Mapea la tabla SQL: tipos_instrumento
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_instrumento'
        verbose_name = 'Tipo de Instrumento'
        verbose_name_plural = 'Tipos de Instrumento'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoModificatorio(AuditModel):
    """
    Catálogo de tipos de documentos modificatorios que pueden alterar un contrato.
    Ej: 'Convenio Modificatorio', 'Fe de Erratas', 'Prórroga', 'Terminación Anticipada'.
    Mapea la tabla SQL: tipos_modificatorio
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_modificatorio'
        verbose_name = 'Tipo de Modificatorio'
        verbose_name_plural = 'Tipos de Modificatorio'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoNotario(AuditModel):
    """
    Catálogo de los fedatarios públicos que pueden dar fe de los instrumentos.
    Ej: 'Notario Público', 'Corredor Público'.
    Mapea la tabla SQL: tipos_notario
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'tipos_notario'
        verbose_name = 'Tipo de Notario'
        verbose_name_plural = 'Tipos de Notario'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoObligacion(AuditModel):
    """
    Catálogo de clasificaciones de obligaciones caucionadas por una fianza.
    Ej: 'Cumplimiento', 'Anticipo', 'Buena Calidad'.
    Mapea la tabla SQL: tipos_obligacion
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_obligacion'
        verbose_name = 'Tipo de Obligación'
        verbose_name_plural = 'Tipos de Obligación'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class TipoParte(AuditModel):
    """
    Catálogo de figuras jurídicas que pueden ser partes en un instrumento.
    Ej: 'Persona Física', 'Persona Moral', 'Fideicomiso', 'Unidad Económica'.
    Mapea la tabla SQL: tipos_parte
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'tipos_parte'
        verbose_name = 'Tipo de Parte'
        verbose_name_plural = 'Tipos de Parte'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE ESTATUS (status_*)
# ─────────────────────────────────────────────────────────────────────────────

class EstatusActividad(AuditModel):
    """
    Catálogo de estados que puede tener una actividad de seguimiento.
    Ej: 'Pendiente', 'En Progreso', 'Completada', 'Cancelada'.
    Mapea la tabla SQL: estatus_actividades
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'estatus_actividades'
        verbose_name = 'Estatus de Actividad'
        verbose_name_plural = 'Estatus de Actividades'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class EstatusEntrega(AuditModel):
    """
    Catálogo de estados del proceso de entrega dentro de un contrato.
    Ej: 'Pendiente', 'Parcial', 'Completa', 'Rechazada'.
    Mapea la tabla SQL: estatus_entregas
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'estatus_entregas'
        verbose_name = 'Estatus de Entrega'
        verbose_name_plural = 'Estatus de Entregas'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class EstatusHito(AuditModel):
    """
    Catálogo de estados para los hitos o eventos clave del contrato.
    Ej: 'Pendiente', 'En Progreso', 'Completado', 'Vencido'.
    Mapea la tabla SQL: estatus_hitos
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'estatus_hitos'
        verbose_name = 'Estatus de Hito'
        verbose_name_plural = 'Estatus de Hitos'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class EstatusIncidencia(AuditModel):
    """
    Catálogo de estados del ciclo de vida de una incidencia contractual.
    Ej: 'Abierta', 'En Resolución', 'Resuelta', 'Cancelada'.
    Mapea la tabla SQL: estatus_incidencias
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'estatus_incidencias'
        verbose_name = 'Estatus de Incidencia'
        verbose_name_plural = 'Estatus de Incidencias'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class EstatusInstrumento(AuditModel):
    """
    Catálogo de estados del ciclo de vida de un instrumento jurídico.
    Ej: 'Borrador', 'Vigente', 'Vencido', 'Cancelado', 'En Firma'.
    Mapea la tabla SQL: estatus_instrumento
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'estatus_instrumento'
        verbose_name = 'Estatus de Instrumento'
        verbose_name_plural = 'Estatus de Instrumento'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE PRIORIDAD (priorities_*)
# ─────────────────────────────────────────────────────────────────────────────

class PrioridadActividad(AuditModel):
    """
    Catálogo de niveles de prioridad asignables a las actividades de seguimiento.
    Ej: 'Alta', 'Media', 'Baja', 'Urgente'.
    Mapea la tabla SQL: prioridades_actividad
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'prioridades_actividad'
        verbose_name = 'Prioridad de Actividad'
        verbose_name_plural = 'Prioridades de Actividad'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class PrioridadHito(AuditModel):
    """
    Catálogo de niveles de relevancia para los hitos del contrato.
    Ej: 'Alta', 'Media', 'Baja'.
    Mapea la tabla SQL: prioridades_hito
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'prioridades_hito'
        verbose_name = 'Prioridad de Hito'
        verbose_name_plural = 'Prioridades de Hito'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class PrioridadInstrumento(AuditModel):
    """
    Catálogo de niveles de prioridad estratégica de un instrumento jurídico.
    Determina el nivel de atención y alerta que el sistema debe aplicar.
    Ej: 'Alta', 'Media', 'Baja'.
    Mapea la tabla SQL: prioridades_instrumento
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'prioridades_instrumento'
        verbose_name = 'Prioridad de Instrumento'
        verbose_name_plural = 'Prioridades de Instrumento'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS MISCELÁNEOS
# ─────────────────────────────────────────────────────────────────────────────

class CategoriaAnexo(AuditModel):
    """
    Catálogo de categorías para clasificar los anexos de un instrumento.
    Ej: 'Técnico', 'Económico', 'Legal', 'Administrativo'.
    Mapea la tabla SQL: categorias_anexo
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'categorias_anexo'
        verbose_name = 'Categoría de Anexo'
        verbose_name_plural = 'Categorías de Anexo'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class CatFacultad(AuditModel):
    """
    Catálogo de facultades o atribuciones jurídicas que puede tener un representante.
    Ej: 'Poderes de Administración', 'Poderes de Dominio'.
    Mapea la tabla SQL: cat_facultades
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'cat_facultades'
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class GravedadIncidencia(AuditModel):
    """
    Catálogo de niveles de gravedad de una incidencia o desviación contractual.
    Ej: 'Crítica', 'Mayor', 'Menor'.
    Mapea la tabla SQL: gravedades_incidencia
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'gravedades_incidencia'
        verbose_name = 'Gravedad de Incidencia'
        verbose_name_plural = 'Gravedades de Incidencia'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class OrganoAdministracion(AuditModel):
    """
    Catálogo de órganos de gobierno corporativo que pueden ser convocados.
    Ej: 'Administrador Único', 'Consejo de Administración', 'Asamblea de Socios'.
    Mapea la tabla SQL: organos_administracion
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')

    class Meta:
        db_table = 'organos_administracion'
        verbose_name = 'Órgano de Administración'
        verbose_name_plural = 'Órganos de Administración'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre


class Rol(AuditModel):
    """
    Catálogo de roles que pueden adoptar las partes dentro de un instrumento contractual.
    Ej: 'Arrendador', 'Arrendatario', 'Contratante', 'Contratista', 'Garante'.
    Mapea la tabla SQL: roles
    """
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']

    def __str__(self) -> str:
        return self.nombre
