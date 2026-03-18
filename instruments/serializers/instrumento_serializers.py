"""
Serializers para el app de Instrumentos de Adcon.

Este módulo es el corazón del CLM: serializa el modelo Instrumento y todas
sus especializaciones contractuales (Arrendamiento, Compraventa, Servicios,
Suministros) y sus entidades de soporte (Concurso, InstrumentoParte, ArchivoFisico).
"""

from rest_framework import serializers
from instruments.models.instrumento import (
    Concurso, Instrumento, InstrumentoParte, ArchivoFisico,
    Arrendamiento, CompraventaInmueble, ServicioPrestado, SuministroMercancia,
    ActoCorporativo, AccionistaEnActo,
)


class ConcursoSerializer(serializers.ModelSerializer):
    """
    Serializer para el proceso de adjudicación (licitación, concurso, AD).
    """
    tipo_concurso_nombre = serializers.CharField(source='tipo_concurso.nombre', read_only=True)

    class Meta:
        model = Concurso
        fields = [
            'id', 'tipo_concurso', 'tipo_concurso_nombre',
            'numero_concurso', 'titulo', 'descripcion',
            'fecha_publicacion', 'fecha_presentacion', 'fecha_fallo',
            'presupuesto_base', 'fundamento_legal',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class InstrumentoSerializer(serializers.ModelSerializer):
    """
    Serializer del modelo central del CLM: el Instrumento jurídico.

    Proporciona representaciones legibles de tipo, estatus y prioridad
    para facilitar el consumo en listas y en el dashboard de seguimiento.
    """
    tipo_instrumento_nombre = serializers.CharField(source='tipo_instrumento.nombre', read_only=True)
    estatus_nombre = serializers.CharField(source='estatus_instrumento.nombre', read_only=True)
    prioridad_nombre = serializers.CharField(source='prioridad_instrumento.nombre', read_only=True)

    class Meta:
        model = Instrumento
        fields = [
            'id', 'num_instrumento', 'titulo', 'dato_maestro_cliente',
            'tipo_instrumento', 'tipo_instrumento_nombre',
            'estatus_instrumento', 'estatus_nombre',
            'prioridad_instrumento', 'prioridad_nombre',
            'tipo_firma', 'tipo_contraprestacion',
            'concurso', 'es_renovacion_automatica', 'instrumento_vinculado',
            'fecha_inicio', 'fecha_termino', 'fecha_firma',
            'rfc_facturacion', 'comentarios',
            'fecha_creacion', 'fecha_actualizacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion', 'creado_por']


class InstrumentoParteSerializer(serializers.ModelSerializer):
    """
    Serializer para la vinculación entre un Instrumento y las Partes que intervienen.

    Presenta el rol de cada parte (Arrendador, Contratista, Garante, etc.)
    para facilitar la generación de reportes de representación contractual.
    """
    parte_nombre = serializers.SerializerMethodField()
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    class Meta:
        model = InstrumentoParte
        fields = [
            'id', 'instrumento', 'parte', 'parte_nombre', 'rol', 'rol_nombre',
            'domicilio_notificaciones', 'es_principal_para_rol', 'fecha_asociacion',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']

    def get_parte_nombre(self, obj: InstrumentoParte) -> str:
        """Retorna el nombre de la parte (Persona Física o Moral)."""
        return str(obj.parte)


class ArchivoFisicoSerializer(serializers.ModelSerializer):
    """
    Serializer para expedientes físicos de un instrumento (carpetas, cajas).
    """
    class Meta:
        model = ArchivoFisico
        fields = [
            'id', 'instrumento', 'nombre', 'descripcion',
            'cantidad', 'ubicacion', 'caja', 'fecha_ingreso',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class ArrendamientoSerializer(serializers.ModelSerializer):
    """
    Serializer para la especialización de Arrendamiento Inmobiliario.

    Proporciona todos los campos financieros y jurídicos del contrato de
    arrendamiento, de vital importancia para la validez legal de los pagos.
    """
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)
    inmueble_catastral = serializers.CharField(source='inmueble.clave_catastral', read_only=True)

    class Meta:
        model = Arrendamiento
        fields = [
            'instrumento', 'instrumento_clave',
            'inmueble', 'inmueble_catastral', 'tipo_garantia',
            'meses_arrendamiento', 'fecha_pago_renta',
            'monto_renta_sin_iva', 'monto_deposito',
            'actualizacion_renta_inpc', 'poliza_responsabilidad_civil',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['instrumento', 'fecha_creacion', 'creado_por']


class CompraventaInmuebleSerializer(serializers.ModelSerializer):
    """
    Serializer para contratos de compraventa de bienes inmuebles.
    """
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)

    class Meta:
        model = CompraventaInmueble
        fields = [
            'instrumento', 'instrumento_clave',
            'inmueble', 'precio_sin_iva', 'deposito_garantia',
            'es_promesa_contrato', 'plazo_pago_dias', 'fecha_firma_contrato_previo',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['instrumento', 'fecha_creacion', 'creado_por']


class ServicioPrestadoSerializer(serializers.ModelSerializer):
    """
    Serializer para contratos de servicios profesionales o consultoría.

    El campo 'requiere_repse' determina si el proveedor debe estar registrado
    en el Registro de Prestadores de Servicios Especializados y Externos.
    """
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)

    class Meta:
        model = ServicioPrestado
        fields = [
            'instrumento', 'instrumento_clave',
            'honorarios_monto', 'frecuencia_pago', 'contraprestacion_total_monto',
            'tipo_entregable', 'fecha_entregable',
            'requiere_repse', 'numero_registro_repse',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['instrumento', 'fecha_creacion', 'creado_por']


class SuministroMercanciaSerializer(serializers.ModelSerializer):
    """
    Serializer para contratos de suministro de bienes y mercancías.

    Soporta tanto contratos cerrados (monto fijo) como abiertos
    (presupuesto mín./máx.), cubriendo las modalidades más comunes
    de contratación de adquisiciones.
    """
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)

    class Meta:
        model = SuministroMercancia
        fields = [
            'instrumento', 'instrumento_clave',
            'domicilio_entrega',
            'subtotal', 'monto_iva', 'monto_total',
            'maximo_subtotal', 'maximo_iva', 'maximo_total',
            'minimo_subtotal', 'minimo_iva', 'minimo_total',
            'anticipo_monto', 'fecha_entrega',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['instrumento', 'fecha_creacion', 'creado_por']


class AccionistaEnActoSerializer(serializers.ModelSerializer):
    """
    Serializer para la participación accionaria en un acto corporativo.
    """
    parte_nombre = serializers.SerializerMethodField()

    class Meta:
        model = AccionistaEnActo
        fields = [
            'id', 'acto_corporativo', 'socio', 'parte_nombre',
            'total_acciones', 'acciones_capital_fijo',
            'acciones_capital_variable', 'acciones_otro_tipo',
            'rfc_socio_momentaneo',
        ]
        read_only_fields = ['id']

    def get_parte_nombre(self, obj: AccionistaEnActo) -> str:
        """Retorna el nombre del socio en el acto corporativo."""
        return str(obj.socio)


class ActoCorporativoSerializer(serializers.ModelSerializer):
    """
    Serializer para Actos Corporativos (Asambleas y decisiones de gobierno).
    """
    accionistas = AccionistaEnActoSerializer(many=True, read_only=True)
    organo_nombre = serializers.CharField(source='organo_administracion.nombre', read_only=True)

    class Meta:
        model = ActoCorporativo
        fields = [
            'id', 'instrumento', 'organo_administracion', 'organo_nombre',
            'tipo_convocatoria', 'domicilio_social',
            'libro_asambleas_foja', 'libro_var_capital_foja', 'libro_reg_acc_foja',
            'fecha_acto', 'contenido',
            'capital_social_fijo', 'capital_social_variable',
            'clausula_extranjeros', 'restricciones_venta_acciones',
            'accionistas', 'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']
