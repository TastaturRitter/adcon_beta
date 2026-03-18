"""
Serializers del modelo de usuario para el sistema Adcon.

Implementa tres serializers diferenciados por responsabilidad:
- UserReadSerializer: solo lectura, exposición segura del perfil.
- UserWriteSerializer: escritura, manejo seguro de contraseña.
- ChangePasswordSerializer: acción dedicada al cambio de contraseña.

Regla de seguridad: el hash del password NUNCA se expone en ninguna respuesta.
"""

from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class UserReadSerializer(serializers.ModelSerializer):
    """
    Serializer de solo lectura para el perfil de usuario del sistema Adcon.

    Expone los datos de identificación, contacto y rol sin información sensible.
    Incluye propiedades calculadas del modelo para uso en lógica de UI.
    """

    # Propiedades calculadas del modelo expuestas como campos de solo lectura
    es_administrador: bool = serializers.BooleanField(read_only=True)
    es_gestor: bool = serializers.BooleanField(read_only=True)
    puede_escribir: bool = serializers.BooleanField(read_only=True)
    puede_editar: bool = serializers.BooleanField(read_only=True)
    role_display: str = serializers.CharField(
        source='get_role_display',
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'rfc',
            'telefono',
            'role',
            'role_display',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login',
            'fecha_actualizacion',
            'es_administrador',
            'es_gestor',
            'puede_escribir',
            'puede_editar',
        ]
        read_only_fields = fields


class UserWriteSerializer(serializers.ModelSerializer):
    """
    Serializer de escritura para creación y actualización de usuarios.

    Valida unicidad del RFC, fortaleza del password mediante los validadores
    de Django y utiliza set_password() para evitar guardar texto plano.

    El password es de solo escritura (write_only=True): nunca se devuelve
    en la respuesta, ni cifrado ni en texto plano.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        help_text='Contraseña del usuario. Se valida con los validadores de seguridad de Django.',
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'rfc',
            'telefono',
            'role',
            'is_active',
            'password',
        ]
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': False},
        }

    def validate_password(self, value: str) -> str:
        """
        Valida la fortaleza de la contraseña con los validadores
        configurados en AUTH_PASSWORD_VALIDATORS del settings de Django.
        """
        validate_password(value)
        return value

    def validate_rfc(self, value: str | None) -> str | None:
        """
        Valida que el RFC, si se proporciona, sea único en el sistema
        excluyendo al propio usuario en caso de actualización.
        """
        if value is None:
            return value
        qs = User.objects.filter(rfc=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Este RFC ya está registrado para otro usuario.')
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        """
        Crea un nuevo usuario. Extrae el password del payload y lo
        almacena cifrado mediante set_password().
        """
        password = validated_data.pop('password', None)
        user: User = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        """
        Actualiza un usuario existente. Si se incluye password en el payload,
        se re-cifra correctamente con set_password().
        """
        password = validated_data.pop('password', None)
        user: User = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer dedicado al cambio de contraseña del usuario autenticado.

    Requiere la contraseña actual para verificar la identidad del solicitante
    antes de aceptar la nueva contraseña, previniendo cambios no autorizados
    si la sesión fue comprometida.
    """

    password_actual = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Contraseña actual del usuario para verificar su identidad.',
    )
    password_nuevo = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Nueva contraseña. Debe cumplir todos los validadores de seguridad configurados.',
    )
    password_nuevo_confirmacion = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Confirmación de la nueva contraseña. Debe ser idéntica al campo anterior.',
    )

    def validate_password_actual(self, value: str) -> str:
        """Verifica que la contraseña actual proporcionada sea correcta."""
        user: User = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('La contraseña actual es incorrecta.')
        return value

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """
        Valida que la nueva contraseña y su confirmación coincidan,
        y que cumpla los requisitos de seguridad de Django.
        """
        nuevo = attrs.get('password_nuevo')
        confirmacion = attrs.get('password_nuevo_confirmacion')
        if nuevo != confirmacion:
            raise serializers.ValidationError(
                {'password_nuevo_confirmacion': 'Las contraseñas no coinciden.'}
            )
        validate_password(nuevo, self.context['request'].user)
        return attrs

    def save(self, **kwargs: Any) -> User:
        """Aplica la nueva contraseña al usuario autenticado."""
        user: User = self.context['request'].user
        user.set_password(self.validated_data['password_nuevo'])
        user.save(update_fields=['password'])
        return user
