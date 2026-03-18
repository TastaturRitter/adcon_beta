"""
Serializers de autenticación para el sistema Adcon.

Implementa la extensión de SimpleJWT para incluir claims personalizados
en el payload del token, permitiendo que el cliente (Frontend) conozca
el rol del usuario sin realizar peticiones adicionales al servidor.
"""

from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token


class AdconTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para la obtención de pares de tokens JWT.

    Añade el campo 'role' al payload del Access Token generado, permitiendo
    una gestión de permisos eficiente en el lado del cliente (Frontend).
    """

    @classmethod
    def get_token(cls, user: Any) -> Token:
        """
        Sobreescribe la generación del token para inyectar claims personalizados.

        Argumentos:
            user: Instancia del modelo User autenticado.

        Retorna:
            Token: Instancia del Access Token con el claim 'role' incluido.
        """
        token = super().get_token(user)

        # Inyección del rol del usuario (RBAC) en el payload del token
        # Esto permite que el Frontend tome decisiones de UI basadas en el rol
        # de forma inmediata tras el login.
        token['role'] = user.role

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        """
        Valida las credenciales y personaliza la respuesta del endpoint de login.

        Añade datos del perfil del usuario a la respuesta JSON para facilitar
        la persistencia en el estado global de la aplicación (e.g. Redux/Zustand).
        """
        data = super().validate(attrs)

        # Datos adicionales en la respuesta de éxito del login
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
            'role': self.user.role,
            'full_name': self.user.get_full_name(),
        }

        return data
