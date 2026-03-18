"""
Vistas para el app de Instrumentos (núcleo del CLM) de Adcon.

ViewSets para Instrumentos y todas sus entidades de soporte y especializaciones
contractuales. Aplica la matriz RBAC para proteger la integridad de los
contratos en todas sus fases del ciclo de vida.
"""

from rest_framework import viewsets
from instruments.models.instrumento import (
    Concurso, Instrumento, InstrumentoParte, ArchivoFisico,
    Arrendamiento, CompraventaInmueble, ServicioPrestado,
    SuministroMercancia, ActoCorporativo,
)
from instruments.serializers.instrumento_serializers import (
    ConcursoSerializer, InstrumentoSerializer, InstrumentoParteSerializer,
    ArchivoFisicoSerializer, ArrendamientoSerializer,
    CompraventaInmuebleSerializer, ServicioPrestadoSerializer,
    SuministroMercanciaSerializer, ActoCorporativoSerializer,
)
from core.permissions import AdconBasePermission


class ConcursoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para procesos de adjudicación (licitaciones, concursos, ADs).
    """
    queryset = Concurso.objects.all().select_related('tipo_concurso')
    serializer_class = ConcursoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class InstrumentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet central del CLM — gestiona el ciclo de vida de todos los contratos.

    El Instrumento es la entidad raíz del sistema. Las especializaciones
    (Arrendamiento, Compraventa, etc.) se vinculan a él mediante relaciones 1:1.
    """
    queryset = Instrumento.objects.all().select_related(
        'tipo_instrumento', 'estatus_instrumento',
        'prioridad_instrumento', 'concurso', 'creado_por',
    )
    serializer_class = InstrumentoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        """Asigna el usuario actual como creador del instrumento jurídico."""
        serializer.save(creado_por=self.request.user)


class InstrumentoParteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para los vínculos entre Instrumentos y Partes (roles contractuales).
    """
    queryset = InstrumentoParte.objects.all().select_related('instrumento', 'parte', 'rol')
    serializer_class = InstrumentoParteSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class ArchivoFisicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para el registro del archivo físico de un instrumento.
    """
    queryset = ArchivoFisico.objects.all().select_related('instrumento')
    serializer_class = ArchivoFisicoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class ArrendamientoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para contratos de arrendamiento inmobiliario.
    """
    queryset = Arrendamiento.objects.all().select_related('instrumento', 'inmueble', 'tipo_garantia')
    serializer_class = ArrendamientoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class CompraventaInmuebleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para contratos de compraventa de bienes inmuebles.
    """
    queryset = CompraventaInmueble.objects.all().select_related('instrumento', 'inmueble')
    serializer_class = CompraventaInmuebleSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class ServicioPrestadoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para contratos de servicios profesionales.
    """
    queryset = ServicioPrestado.objects.all().select_related('instrumento')
    serializer_class = ServicioPrestadoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class SuministroMercanciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para contratos de suministro de bienes y mercancías.
    """
    queryset = SuministroMercancia.objects.all().select_related('instrumento', 'domicilio_entrega')
    serializer_class = SuministroMercanciaSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)


class ActoCorporativoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Actos Corporativos (asambleas, cambios de administración).
    """
    queryset = ActoCorporativo.objects.all().select_related(
        'instrumento', 'organo_administracion', 'tipo_convocatoria'
    ).prefetch_related('accionistas')
    serializer_class = ActoCorporativoSerializer
    permission_classes = [AdconBasePermission]

    def perform_create(self, serializer) -> None:
        serializer.save(creado_por=self.request.user)
