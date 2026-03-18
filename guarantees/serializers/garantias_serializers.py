"""
Serializers para el app de Garantías de Adcon.

Gestiona la representación de Fianzas y Penas convencionales, incluyendo
la lógica de cálculo de montos penalizados y la trazabilidad de pólizas
de garantía para la gestión del cumplimiento contractual.
"""

from rest_framework import serializers
from guarantees.models.garantias import Pena, Fianza


class PenaSerializer(serializers.ModelSerializer):
    """
    Serializer para Penas Convencionales.

    El campo 'monto_penalizado' puede ser calculado automáticamente
    (monto_a_penalizar × porcentaje / 100) o capturarse manualmente.
    """
    tipo_dia_nombre = serializers.CharField(source='tipo_dia.nombre', read_only=True)
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)

    class Meta:
        model = Pena
        fields = [
            'id', 'instrumento', 'instrumento_clave',
            'addendum', 'modificatorio', 'anexo', 'partida',
            'unidad_medida_penalizada', 'cantidad_unidad_medida',
            'dias_atraso', 'tipo_dia', 'tipo_dia_nombre', 'periodo_pena',
            'monto_a_penalizar', 'valor_pena_porcentaje', 'monto_penalizado',
            'comentario', 'link_factura', 'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class FianzaSerializer(serializers.ModelSerializer):
    """
    Serializer para Fianzas (pólizas de garantía).

    Incluye datos de la afianzadora y el tipo de obligación cubierta.
    El campo 'ruta_archivo' apunta al PDF de la póliza en S3.
    """
    tipo_fianza_nombre = serializers.CharField(source='tipo_fianza.nombre', read_only=True)
    afianzadora_nombre = serializers.SerializerMethodField()
    instrumento_clave = serializers.CharField(source='instrumento.num_instrumento', read_only=True)

    class Meta:
        model = Fianza
        fields = [
            'id', 'instrumento', 'instrumento_clave',
            'tipo_fianza', 'tipo_fianza_nombre',
            'tipo_obligacion', 'afianzadora', 'afianzadora_nombre', 'pena',
            'numero_poliza', 'monto', 'descripcion_obligacion',
            'fecha_inicio', 'fecha_fin',
            'nombre_archivo', 'ruta_archivo',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']

    def get_afianzadora_nombre(self, obj: Fianza) -> str | None:
        """Retorna el nombre (razón social o nombre) de la afianzadora."""
        if obj.afianzadora:
            return str(obj.afianzadora)
        return None
