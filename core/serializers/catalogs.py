"""
Serializers de catálogos del sistema Adcon.

Los catálogos son tablas de referencia (lookup tables) que proveen valores
controlados para clasificar las entidades del CLM. La estructura es uniforme:
todos exponen los campos id, nombre, descripción y auditoría.

Todos heredan de ModelSerializer para aprovechar la introspección automática
de campos y la validación basada en las restricciones del modelo.
"""

from rest_framework import serializers

from core.models import (
    # tipos_*
    TipoActividad, TipoAddendum, TipoAdminInstrumento, TipoConcurso,
    TipoContraprestacion, TipoConvocatoria, TipoCopia, TipoDia,
    TipoEntrega, TipoEscritura, TipoEvidencia, TipoFianza, TipoFirma,
    TipoGarantiaArrendamiento, TipoHito, TipoIncidencia, TipoInmueble,
    TipoInstrumento, TipoModificatorio, TipoNotario, TipoObligacion, TipoParte,
    # estatus_*
    EstatusActividad, EstatusEntrega, EstatusHito, EstatusIncidencia, EstatusInstrumento,
    # prioridades_*
    PrioridadActividad, PrioridadHito, PrioridadInstrumento,
    # misceláneos
    CategoriaAnexo, CatFacultad, GravedadIncidencia, OrganoAdministracion, Rol,
)


# ─────────────────────────────────────────────────────────────────────────────
# MIXIN BASE: campos de auditoría comunes a todos los catálogos
# ─────────────────────────────────────────────────────────────────────────────

class _CatalogoBaseMixin:
    """
    Mixin interno que define los campos de auditoría comunes a todos los catálogos.
    Solo para uso interno de este módulo — no instanciar directamente.
    """

    AUDIT_FIELDS: list[str] = ['creado_por', 'fecha_creacion']

    class Meta:
        """Meta base sobreescrita por cada subclase."""
        read_only_fields = ['id', 'creado_por', 'fecha_creacion']


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE TIPO (tipos_*)
# ─────────────────────────────────────────────────────────────────────────────

class TipoActividadSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de actividad contractual."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoActividad
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoAddendumSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de addendum contractual."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoAddendum
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoAdminInstrumentoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de administración de instrumento."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoAdminInstrumento
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoConcursoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de modalidades de concurso o licitación."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoConcurso
        fields = ['id', 'nombre', 'clave_oficial', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoContraprestacionSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de contraprestación contractual."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoContraprestacion
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoConvocatoriaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de convocatoria a órganos de gobierno."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoConvocatoria
        fields = [
            'id', 'nombre', 'descripcion',
            'plazo_previo_agoa_dias', 'plazo_previo_agea_dias',
            'plazo_previo_junta_consejo_dias',
            'creado_por', 'fecha_creacion',
        ]


class TipoCopiaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de validez legal de copias de documentos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoCopia
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoDiaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de día en cómputo de plazos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoDia
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoEntregaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de modalidades de entrega contractual."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoEntrega
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoEscrituraSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de escritura pública notarial."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoEscritura
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoEvidenciaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de evidencia documental."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoEvidencia
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoFianzaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de fianza o garantía contractual."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoFianza
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoFirmaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de modalidades de firma de instrumentos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoFirma
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoGarantiaArrendamientoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de garantía en arrendamientos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoGarantiaArrendamiento
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoHitoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de hito o evento contractual clave."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoHito
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoIncidenciaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de categorías de incidencias contractuales."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoIncidencia
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoInmuebleSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de clasificaciones de inmuebles."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoInmueble
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoInstrumentoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo maestro de tipos de instrumento jurídico."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoInstrumento
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoModificatorioSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de documento modificatorio."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoModificatorio
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoNotarioSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de fedatario público (Notario/Corredor)."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoNotario
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class TipoObligacionSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de tipos de obligación caucionada por fianza."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoObligacion
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class TipoParteSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de figuras jurídicas que pueden ser partes."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = TipoParte
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE ESTATUS (estatus_*)
# ─────────────────────────────────────────────────────────────────────────────

class EstatusActividadSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de estados de actividades de seguimiento."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = EstatusActividad
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class EstatusEntregaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de estados del proceso de entrega."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = EstatusEntrega
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class EstatusHitoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de estados de hitos contractuales."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = EstatusHito
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class EstatusIncidenciaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de estados del ciclo de vida de incidencias."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = EstatusIncidencia
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class EstatusInstrumentoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de estados del ciclo de vida de instrumentos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = EstatusInstrumento
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE PRIORIDAD (prioridades_*)
# ─────────────────────────────────────────────────────────────────────────────

class PrioridadActividadSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de prioridades de actividades."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = PrioridadActividad
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class PrioridadHitoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de prioridades de hitos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = PrioridadHito
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class PrioridadInstrumentoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de prioridades estratégicas de instrumentos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = PrioridadInstrumento
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS MISCELÁNEOS
# ─────────────────────────────────────────────────────────────────────────────

class CategoriaAnexoSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de categorías de anexos contractuales."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = CategoriaAnexo
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class CatFacultadSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de facultades jurídicas de representantes."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = CatFacultad
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']


class GravedadIncidenciaSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de niveles de gravedad de incidencias."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = GravedadIncidencia
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class OrganoAdministracionSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de órganos de gobierno corporativo."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = OrganoAdministracion
        fields = ['id', 'nombre', 'creado_por', 'fecha_creacion']


class RolSerializer(_CatalogoBaseMixin, serializers.ModelSerializer):
    """Serializer para el catálogo de roles de partes dentro de instrumentos."""
    class Meta(_CatalogoBaseMixin.Meta):
        model = Rol
        fields = ['id', 'nombre', 'descripcion', 'creado_por', 'fecha_creacion']
