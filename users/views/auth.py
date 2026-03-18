"""
Vistas de autenticación JWT para el sistema Adcon.

Provee los endpoints para el intercambio de credenciales por tokens y
la renovación de sesiones mediante refresh tokens.
"""

from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers.auth import AdconTokenObtainPairSerializer


class AdconTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para el inicio de sesión (Login).

    Utiliza AdconTokenObtainPairSerializer para devolver un Access Token
    que contiene el rol del usuario (RBAC) y un Refresh Token para
    mantener la sesión activa.
    """
    serializer_class = AdconTokenObtainPairSerializer
