"""
ViewSets de catálogos del sistema Adcon.

Expone todos los catálogos (lookup tables) como endpoints REST con la
siguiente política de permisos RBAC:

    Lectura  (GET/HEAD/OPTIONS): cualquier usuario autenticado (todos los roles).
    Creación (POST):             ADMIN y MANAGER únicamente.
    Edición  (PUT/PATCH):        ADMIN, MANAGER y EDITOR.
    Borrado  (DELETE):           ADMIN y MANAGER únicamente.

Los catálogos son datos de referencia controlados por el administrador.
Modificarlos incorrectamente puede corromper la integridad referencial
del sistema CLM, por lo que se aplica AdconBasePermission estrictamente.

Optimización: todos los querysets usan select_related('creado_por')
para evitar N+1 queries en el campo de auditoría.
"""

from django.db.models import QuerySet
from rest_framework import viewsets

from core.permissions import AdconBasePermission
from core.models import (
    TipoActividad, TipoAddendum, TipoAdminInstrumento, TipoConcurso,
    TipoContraprestacion, TipoConvocatoria, TipoCopia, TipoDia,
    TipoEntrega, TipoEscritura, TipoEvidencia, TipoFianza, TipoFirma,
    TipoGarantiaArrendamiento, TipoHito, TipoIncidencia, TipoInmueble,
    TipoInstrumento, TipoModificatorio, TipoNotario, TipoObligacion, TipoParte,
    EstatusActividad, EstatusEntrega, EstatusHito, EstatusIncidencia, EstatusInstrumento,
    PrioridadActividad, PrioridadHito, PrioridadInstrumento,
    CategoriaAnexo, CatFacultad, GravedadIncidencia, OrganoAdministracion, Rol,
)
from core.serializers.catalogs import (
    TipoActividadSerializer, TipoAddendumSerializer, TipoAdminInstrumentoSerializer,
    TipoConcursoSerializer, TipoContraprestacionSerializer, TipoConvocatoriaSerializer,
    TipoCopiaSerializer, TipoDiaSerializer, TipoEntregaSerializer,
    TipoEscrituraSerializer, TipoEvidenciaSerializer, TipoFianzaSerializer,
    TipoFirmaSerializer, TipoGarantiaArrendamientoSerializer, TipoHitoSerializer,
    TipoIncidenciaSerializer, TipoInmuebleSerializer, TipoInstrumentoSerializer,
    TipoModificatorioSerializer, TipoNotarioSerializer, TipoObligacionSerializer,
    TipoParteSerializer,
    EstatusActividadSerializer, EstatusEntregaSerializer, EstatusHitoSerializer,
    EstatusIncidenciaSerializer, EstatusInstrumentoSerializer,
    PrioridadActividadSerializer, PrioridadHitoSerializer, PrioridadInstrumentoSerializer,
    CategoriaAnexoSerializer, CatFacultadSerializer, GravedadIncidenciaSerializer,
    OrganoAdministracionSerializer, RolSerializer,
)


class _CatalogoBaseViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para todos los catálogos del sistema Adcon.

    Aplica AdconBasePermission a todas las acciones, delegando la evaluación
    de permisos por método HTTP a la clase centralizada de RBAC.

    Las subclases solo necesitan declarar `queryset` y `serializer_class`.
    """
    permission_classes = [AdconBasePermission]


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE TIPO (tipos_*)
# ─────────────────────────────────────────────────────────────────────────────

class TipoActividadViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Actividad."""
    queryset: QuerySet = TipoActividad.objects.select_related('creado_por')
    serializer_class = TipoActividadSerializer


class TipoAddendumViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Addendum."""
    queryset: QuerySet = TipoAddendum.objects.select_related('creado_por')
    serializer_class = TipoAddendumSerializer


class TipoAdminInstrumentoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Administración de Instrumento."""
    queryset: QuerySet = TipoAdminInstrumento.objects.select_related('creado_por')
    serializer_class = TipoAdminInstrumentoSerializer


class TipoConcursoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Concurso / Licitación."""
    queryset: QuerySet = TipoConcurso.objects.select_related('creado_por')
    serializer_class = TipoConcursoSerializer


class TipoContraprestacionViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Contraprestación."""
    queryset: QuerySet = TipoContraprestacion.objects.select_related('creado_por')
    serializer_class = TipoContraprestacionSerializer


class TipoConvocatoriaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Convocatoria a Órganos de Gobierno."""
    queryset: QuerySet = TipoConvocatoria.objects.select_related('creado_por')
    serializer_class = TipoConvocatoriaSerializer


class TipoCopiaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Copia (validez legal)."""
    queryset: QuerySet = TipoCopia.objects.select_related('creado_por')
    serializer_class = TipoCopiaSerializer


class TipoDiaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Día (hábiles/naturales)."""
    queryset: QuerySet = TipoDia.objects.select_related('creado_por')
    serializer_class = TipoDiaSerializer


class TipoEntregaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Entrega."""
    queryset: QuerySet = TipoEntrega.objects.select_related('creado_por')
    serializer_class = TipoEntregaSerializer


class TipoEscrituraViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Escritura Pública."""
    queryset: QuerySet = TipoEscritura.objects.select_related('creado_por')
    serializer_class = TipoEscrituraSerializer


class TipoEvidenciaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Evidencia."""
    queryset: QuerySet = TipoEvidencia.objects.select_related('creado_por')
    serializer_class = TipoEvidenciaSerializer


class TipoFianzaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Fianza."""
    queryset: QuerySet = TipoFianza.objects.select_related('creado_por')
    serializer_class = TipoFianzaSerializer


class TipoFirmaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Firma."""
    queryset: QuerySet = TipoFirma.objects.select_related('creado_por')
    serializer_class = TipoFirmaSerializer


class TipoGarantiaArrendamientoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Garantía de Arrendamiento."""
    queryset: QuerySet = TipoGarantiaArrendamiento.objects.select_related('creado_por')
    serializer_class = TipoGarantiaArrendamientoSerializer


class TipoHitoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Hito."""
    queryset: QuerySet = TipoHito.objects.select_related('creado_por')
    serializer_class = TipoHitoSerializer


class TipoIncidenciaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Incidencia."""
    queryset: QuerySet = TipoIncidencia.objects.select_related('creado_por')
    serializer_class = TipoIncidenciaSerializer


class TipoInmuebleViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Inmueble."""
    queryset: QuerySet = TipoInmueble.objects.select_related('creado_por')
    serializer_class = TipoInmuebleSerializer


class TipoInstrumentoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo maestro: Tipos de Instrumento Jurídico."""
    queryset: QuerySet = TipoInstrumento.objects.select_related('creado_por')
    serializer_class = TipoInstrumentoSerializer


class TipoModificatorioViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Modificatorio."""
    queryset: QuerySet = TipoModificatorio.objects.select_related('creado_por')
    serializer_class = TipoModificatorioSerializer


class TipoNotarioViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Fedatario Público."""
    queryset: QuerySet = TipoNotario.objects.select_related('creado_por')
    serializer_class = TipoNotarioSerializer


class TipoObligacionViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Obligación Caucionada."""
    queryset: QuerySet = TipoObligacion.objects.select_related('creado_por')
    serializer_class = TipoObligacionSerializer


class TipoParteViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Tipos de Parte (figuras jurídicas)."""
    queryset: QuerySet = TipoParte.objects.select_related('creado_por')
    serializer_class = TipoParteSerializer


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE ESTATUS (estatus_*)
# ─────────────────────────────────────────────────────────────────────────────

class EstatusActividadViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Estatus de Actividad."""
    queryset: QuerySet = EstatusActividad.objects.select_related('creado_por')
    serializer_class = EstatusActividadSerializer


class EstatusEntregaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Estatus de Entrega."""
    queryset: QuerySet = EstatusEntrega.objects.select_related('creado_por')
    serializer_class = EstatusEntregaSerializer


class EstatusHitoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Estatus de Hito."""
    queryset: QuerySet = EstatusHito.objects.select_related('creado_por')
    serializer_class = EstatusHitoSerializer


class EstatusIncidenciaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Estatus de Incidencia."""
    queryset: QuerySet = EstatusIncidencia.objects.select_related('creado_por')
    serializer_class = EstatusIncidenciaSerializer


class EstatusInstrumentoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Estatus de Instrumento."""
    queryset: QuerySet = EstatusInstrumento.objects.select_related('creado_por')
    serializer_class = EstatusInstrumentoSerializer


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS DE PRIORIDAD (prioridades_*)
# ─────────────────────────────────────────────────────────────────────────────

class PrioridadActividadViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Prioridades de Actividad."""
    queryset: QuerySet = PrioridadActividad.objects.select_related('creado_por')
    serializer_class = PrioridadActividadSerializer


class PrioridadHitoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Prioridades de Hito."""
    queryset: QuerySet = PrioridadHito.objects.select_related('creado_por')
    serializer_class = PrioridadHitoSerializer


class PrioridadInstrumentoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Prioridades de Instrumento."""
    queryset: QuerySet = PrioridadInstrumento.objects.select_related('creado_por')
    serializer_class = PrioridadInstrumentoSerializer


# ─────────────────────────────────────────────────────────────────────────────
# CATÁLOGOS MISCELÁNEOS
# ─────────────────────────────────────────────────────────────────────────────

class CategoriaAnexoViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Categorías de Anexo."""
    queryset: QuerySet = CategoriaAnexo.objects.select_related('creado_por')
    serializer_class = CategoriaAnexoSerializer


class CatFacultadViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Facultades Jurídicas de Representantes."""
    queryset: QuerySet = CatFacultad.objects.select_related('creado_por')
    serializer_class = CatFacultadSerializer


class GravedadIncidenciaViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Gravedades de Incidencia."""
    queryset: QuerySet = GravedadIncidencia.objects.select_related('creado_por')
    serializer_class = GravedadIncidenciaSerializer


class OrganoAdministracionViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Órganos de Administración Corporativa."""
    queryset: QuerySet = OrganoAdministracion.objects.select_related('creado_por')
    serializer_class = OrganoAdministracionSerializer


class RolViewSet(_CatalogoBaseViewSet):
    """Endpoint CRUD para el catálogo: Roles de Partes en Instrumentos."""
    queryset: QuerySet = Rol.objects.select_related('creado_por')
    serializer_class = RolSerializer
