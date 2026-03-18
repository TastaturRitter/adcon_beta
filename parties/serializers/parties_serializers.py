"""
Serializers para el app de partes (Parties) de Adcon.

Maneja la lógica de registro de Personas Físicas, Morales y Sucursales,
asegurando la integridad de los datos de contacto y la trazabilidad de auditoría.
"""

from rest_framework import serializers
from parties.models import Parte, PersonaFisica, PersonaMoral, Sucursal
from core.models.catalogs import TipoParte, OrganoAdministracion
from addresses.models.domicilio import Domicilio


class ParteSerializer(serializers.ModelSerializer):
    """
    Serializer base para el modelo Parte.
    """
    tipo_parte_nombre = serializers.CharField(source='tipo_parte.nombre', read_only=True)
    domicilio_detalle = serializers.CharField(source='domicilio.__str__', read_only=True)

    class Meta:
        model = Parte
        fields = [
            'id',
            'tipo_parte',
            'tipo_parte_nombre',
            'domicilio',
            'domicilio_detalle',
            'email',
            'telefono',
            'fecha_creacion',
            'creado_por',
        ]
        read_only_fields = ['id', 'fecha_creacion', 'creado_por']


class PersonaFisicaSerializer(serializers.ModelSerializer):
    """
    Serializer para Personas Físicas.
    
    Incluye los campos base de la Parte asociada para un registro unificado.
    """
    parte_data = ParteSerializer(source='parte', read_only=True)
    
    # Campos de Parte para creación/actualización mediante 'write'
    tipo_parte = serializers.PrimaryKeyRelatedField(
        queryset=TipoParte.objects.all(),
        source='parte.tipo_parte', write_only=True
    )
    domicilio = serializers.PrimaryKeyRelatedField(
        queryset=Domicilio.objects.all(),
        source='parte.domicilio', write_only=True, required=False
    )
    email = serializers.EmailField(source='parte.email', write_only=True, required=False)
    telefono = serializers.CharField(source='parte.telefono', write_only=True, required=False)

    class Meta:
        model = PersonaFisica
        fields = [
            'parte',
            'parte_data',
            'nombre',
            'apellido_paterno',
            'apellido_materno',
            'rfc',
            'curp',
            'fecha_nacimiento',
            'nacionalidad',
            # Campos de escritura de Parte
            'tipo_parte',
            'domicilio',
            'email',
            'telefono',
        ]
        read_only_fields = ['parte']

    def create(self, validated_data):
        parte_data = validated_data.pop('parte')
        parte = Parte.objects.create(**parte_data)
        persona = PersonaFisica.objects.create(parte=parte, **validated_data)
        return persona

    def update(self, instance, validated_data):
        parte_data = validated_data.pop('parte', {})
        parte = instance.parte
        for attr, value in parte_data.items():
            setattr(parte, attr, value)
        parte.save()
        return super().update(instance, validated_data)


class PersonaMoralSerializer(serializers.ModelSerializer):
    """
    Serializer para Personas Morales.
    """
    parte_data = ParteSerializer(source='parte', read_only=True)
    # Campos de Parte para escritura
    tipo_parte = serializers.PrimaryKeyRelatedField(
        queryset=TipoParte.objects.all(),
        source='parte.tipo_parte', write_only=True
    )
    domicilio = serializers.PrimaryKeyRelatedField(
        queryset=Domicilio.objects.all(),
        source='parte.domicilio', write_only=True, required=False
    )
    email = serializers.EmailField(source='parte.email', write_only=True, required=False)
    telefono = serializers.CharField(source='parte.telefono', write_only=True, required=False)

    class Meta:
        model = PersonaMoral
        fields = [
            'parte',
            'parte_data',
            'razon_social',
            'rfc',
            'fecha_constitucion',
            'objeto_social',
            'organo_administracion',
            'representante_legal',
            'apoderado_general',
            # Campos de escritura de Parte
            'tipo_parte',
            'domicilio',
            'email',
            'telefono',
        ]
        read_only_fields = ['parte']

    def create(self, validated_data):
        parte_data = validated_data.pop('parte')
        parte = Parte.objects.create(**parte_data)
        persona = PersonaMoral.objects.create(parte=parte, **validated_data)
        return persona

    def update(self, instance, validated_data):
        parte_data = validated_data.pop('parte', {})
        parte = instance.parte
        for attr, value in parte_data.items():
            setattr(parte, attr, value)
        parte.save()
        return super().update(instance, validated_data)


class SucursalSerializer(serializers.ModelSerializer):
    """
    Serializer para Sucursales de una Parte (Empresa).
    """
    class Meta:
        model = Sucursal
        fields = ['id', 'parte', 'domicilio', 'nombre', 'telefono', 'email']
        read_only_fields = ['id']
