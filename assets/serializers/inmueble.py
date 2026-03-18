"""
Serializers para el app de activos (Assets) de Adcon.

Transforma los modelos de inmuebles a representaciones JSON, manejando
la validación de superficies y relaciones con los catálogos de core.
"""

from rest_framework import serializers
from assets.models.inmueble import Inmueble


class InmuebleSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Inmueble.

    Incluye nombres legibles para las claves foráneas para facilitar
    el consumo desde el frontend.
    """
    tipo_inmueble_nombre = serializers.CharField(source='tipo_inmueble.nombre', read_only=True)
    domicilio_detalle = serializers.CharField(source='domicilio.__str__', read_only=True)
    propietario_nombre = serializers.SerializerMethodField()

    class Meta:
        model = Inmueble
        fields = [
            'id',
            'clave_catastral',
            'tipo_inmueble',
            'tipo_inmueble_nombre',
            'propietario',
            'propietario_nombre',
            'domicilio',
            'domicilio_detalle',
            'descripcion',
            'superficie_terreno_m2',
            'superficie_construccion_m2',
            'fecha_creacion',
            'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']

    def get_propietario_nombre(self, obj: Inmueble) -> str | None:
        """
        Retorna el nombre del propietario (Persona Física o Moral) 
        asociado al inmueble.
        """
        if obj.propietario:
            return str(obj.propietario)
        return None
