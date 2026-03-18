"""
Router local del app de catálogos (core).

Registra los 35 ViewSets de catálogo con sus prefijos REST kebab-case
y los expone para su inclusión en el router principal bajo /api/core/.
"""

from rest_framework.routers import DefaultRouter

from core.views.catalog_viewsets import (
    # tipos_*
    TipoActividadViewSet, TipoAddendumViewSet, TipoAdminInstrumentoViewSet,
    TipoConcursoViewSet, TipoContraprestacionViewSet, TipoConvocatoriaViewSet,
    TipoCopiaViewSet, TipoDiaViewSet, TipoEntregaViewSet, TipoEscrituraViewSet,
    TipoEvidenciaViewSet, TipoFianzaViewSet, TipoFirmaViewSet,
    TipoGarantiaArrendamientoViewSet, TipoHitoViewSet, TipoIncidenciaViewSet,
    TipoInmuebleViewSet, TipoInstrumentoViewSet, TipoModificatorioViewSet,
    TipoNotarioViewSet, TipoObligacionViewSet, TipoParteViewSet,
    # estatus_*
    EstatusActividadViewSet, EstatusEntregaViewSet, EstatusHitoViewSet,
    EstatusIncidenciaViewSet, EstatusInstrumentoViewSet,
    # prioridades_*
    PrioridadActividadViewSet, PrioridadHitoViewSet, PrioridadInstrumentoViewSet,
    # misc
    CategoriaAnexoViewSet, CatFacultadViewSet, GravedadIncidenciaViewSet,
    OrganoAdministracionViewSet, RolViewSet,
)

router = DefaultRouter()

# ── tipos_* ──────────────────────────────────────────────────────────────────
router.register(r'tipos-actividad',               TipoActividadViewSet,               basename='tipo-actividad')
router.register(r'tipos-addendum',                TipoAddendumViewSet,                basename='tipo-addendum')
router.register(r'tipos-admin-instrumento',       TipoAdminInstrumentoViewSet,        basename='tipo-admin-instrumento')
router.register(r'tipos-concurso',                TipoConcursoViewSet,                basename='tipo-concurso')
router.register(r'tipos-contraprestacion',        TipoContraprestacionViewSet,        basename='tipo-contraprestacion')
router.register(r'tipos-convocatoria',            TipoConvocatoriaViewSet,            basename='tipo-convocatoria')
router.register(r'tipos-copia',                   TipoCopiaViewSet,                   basename='tipo-copia')
router.register(r'tipos-dia',                     TipoDiaViewSet,                     basename='tipo-dia')
router.register(r'tipos-entrega',                 TipoEntregaViewSet,                 basename='tipo-entrega')
router.register(r'tipos-escritura',               TipoEscrituraViewSet,               basename='tipo-escritura')
router.register(r'tipos-evidencia',               TipoEvidenciaViewSet,               basename='tipo-evidencia')
router.register(r'tipos-fianza',                  TipoFianzaViewSet,                  basename='tipo-fianza')
router.register(r'tipos-firma',                   TipoFirmaViewSet,                   basename='tipo-firma')
router.register(r'tipos-garantia-arrendamiento',  TipoGarantiaArrendamientoViewSet,   basename='tipo-garantia-arrendamiento')
router.register(r'tipos-hito',                    TipoHitoViewSet,                    basename='tipo-hito')
router.register(r'tipos-incidencia',              TipoIncidenciaViewSet,              basename='tipo-incidencia')
router.register(r'tipos-inmueble',                TipoInmuebleViewSet,                basename='tipo-inmueble')
router.register(r'tipos-instrumento',             TipoInstrumentoViewSet,             basename='tipo-instrumento')
router.register(r'tipos-modificatorio',           TipoModificatorioViewSet,           basename='tipo-modificatorio')
router.register(r'tipos-notario',                 TipoNotarioViewSet,                 basename='tipo-notario')
router.register(r'tipos-obligacion',              TipoObligacionViewSet,              basename='tipo-obligacion')
router.register(r'tipos-parte',                   TipoParteViewSet,                   basename='tipo-parte')

# ── estatus_* ─────────────────────────────────────────────────────────────────
router.register(r'estatus-actividad',             EstatusActividadViewSet,            basename='estatus-actividad')
router.register(r'estatus-entrega',               EstatusEntregaViewSet,              basename='estatus-entrega')
router.register(r'estatus-hito',                  EstatusHitoViewSet,                 basename='estatus-hito')
router.register(r'estatus-incidencia',            EstatusIncidenciaViewSet,           basename='estatus-incidencia')
router.register(r'estatus-instrumento',           EstatusInstrumentoViewSet,          basename='estatus-instrumento')

# ── prioridades_* ─────────────────────────────────────────────────────────────
router.register(r'prioridades-actividad',         PrioridadActividadViewSet,          basename='prioridad-actividad')
router.register(r'prioridades-hito',              PrioridadHitoViewSet,               basename='prioridad-hito')
router.register(r'prioridades-instrumento',       PrioridadInstrumentoViewSet,        basename='prioridad-instrumento')

# ── misceláneos ───────────────────────────────────────────────────────────────
router.register(r'categorias-anexo',              CategoriaAnexoViewSet,              basename='categoria-anexo')
router.register(r'facultades',                    CatFacultadViewSet,                 basename='facultad')
router.register(r'gravedades-incidencia',         GravedadIncidenciaViewSet,          basename='gravedad-incidencia')
router.register(r'organos-administracion',        OrganoAdministracionViewSet,        basename='organo-administracion')
router.register(r'roles',                         RolViewSet,                         basename='rol')

urlpatterns = router.urls
