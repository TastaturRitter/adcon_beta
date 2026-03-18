"""
Serializers para el app Legal de Adcon.

Transforma los modelos notariales y de personalidad jurídica a JSON,
garantizando que los datos del fedatario, fechas y poderes sean correctamente
representados para el consumo del frontend y los reportes legales.
"""

from rest_framework import serializers
from legal.models.legal import Notario, Escritura, EscrituraPersonalidad, EscrituraFacultad


class NotarioSerializer(serializers.ModelSerializer):
    """
    Serializer para el fedatario público (Notario o Corredor Público).
    """
    tipo_notario_nombre = serializers.CharField(source='tipo_notario.nombre', read_only=True)

    class Meta:
        model = Notario
        fields = [
            'id', 'tipo_notario', 'tipo_notario_nombre',
            'nombre', 'apellido_paterno', 'apellido_materno',
            'numero_notaria', 'distrito', 'rfc', 'email',
            'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class EscrituraSerializer(serializers.ModelSerializer):
    """
    Serializer para escrituras públicas y pólizas mercantiles.

    Incluye los datos del notario en formato legible y preserva la ruta
    al archivo digitalizado en S3 para garantizar su consulta segura.
    """
    notario_nombre = serializers.CharField(source='notario.__str__', read_only=True)
    tipo_escritura_nombre = serializers.CharField(source='tipo_escritura.nombre', read_only=True)

    class Meta:
        model = Escritura
        fields = [
            'id', 'instrumento', 'notario', 'notario_nombre',
            'tipo_escritura', 'tipo_escritura_nombre',
            'titulo', 'numero_escritura', 'numero_testimonio',
            'datos_registro_publico', 'descripcion',
            'nombre_archivo', 'ruta_archivo',
            'fecha_otorgamiento', 'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class EscrituraFacultadSerializer(serializers.ModelSerializer):
    """
    Serializer para las facultades o atribuciones de una escritura de poder.
    """
    facultad_nombre = serializers.CharField(source='facultad.nombre', read_only=True)

    class Meta:
        model = EscrituraFacultad
        fields = ['id', 'escritura_personalidad', 'facultad', 'facultad_nombre', 'limitacion_descripcion']
        read_only_fields = ['id']


class EscrituraPersonalidadSerializer(serializers.ModelSerializer):
    """
    Serializer para escrituras de personalidad jurídica (poderes notariales).

    Incluye las facultades otorgadas (nested read-only) y representa las
    partes en formato legible para facilitar auditorías de representación legal.
    """
    representante_nombre = serializers.SerializerMethodField()
    representado_nombre = serializers.SerializerMethodField()
    notario_nombre = serializers.CharField(source='notario.__str__', read_only=True)
    facultades = EscrituraFacultadSerializer(many=True, read_only=True)

    class Meta:
        model = EscrituraPersonalidad
        fields = [
            'id', 'representante', 'representante_nombre',
            'representado', 'representado_nombre',
            'notario', 'notario_nombre',
            'instrumento_origen',
            'numero_escritura', 'fecha_otorgamiento', 'lugar_otorgamiento',
            'comentarios', 'nombre_archivo', 'ruta_archivo',
            'facultades', 'fecha_creacion', 'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']

    def get_representante_nombre(self, obj: EscrituraPersonalidad) -> str:
        """Retorna el nombre legible del representante (persona física o moral)."""
        return str(obj.representante)

    def get_representado_nombre(self, obj: EscrituraPersonalidad) -> str:
        """Retorna el nombre legible del representado (persona moral)."""
        return str(obj.representado)
