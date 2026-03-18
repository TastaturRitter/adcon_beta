"""
ViewSet del modelo de usuario para la API REST del sistema Adcon.

Implementa las operaciones CRUD estándar más dos acciones personalizadas:
- me/: devuelve el perfil del usuario autenticado (GET).
- set-password/: permite cambiar la contraseña de forma segura (POST).

Política de permisos RBAC:
- Lectura (list/retrieve/me): cualquier usuario autenticado.
- Escritura (create/update/destroy): exclusivo para rol ADMIN.
- set-password: usuario autenticado (solo sobre su propia cuenta, o ADMIN sobre cualquiera).
"""

from typing import Any

from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from core.permissions import AdminOnlyPermission, IsAuthenticatedAdcon
from users.models import User
from users.serializers.user import (
    ChangePasswordSerializer,
    UserReadSerializer,
    UserWriteSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo para la gestión de usuarios del sistema Adcon.

    Endpoints estándar del router:
    - GET    /api/users/                    → list()
    - POST   /api/users/                    → create()
    - GET    /api/users/{id}/               → retrieve()
    - PATCH  /api/users/{id}/               → partial_update()
    - DELETE /api/users/{id}/               → destroy()

    Acciones personalizadas:
    - GET  /api/users/me/                   → perfil del usuario autenticado
    - POST /api/users/{id}/set-password/    → cambio de contraseña

    Regla RBAC: la gestión de usuarios es exclusiva para el rol ADMIN.
    Cualquier intento de escritura por parte de MANAGER, EDITOR o READER
    devolverá HTTP 403 con un mensaje descriptivo en español.
    """

    queryset: QuerySet = User.objects.select_related().order_by('username')

    def get_serializer_class(self) -> type[BaseSerializer]:
        """
        Devuelve el serializer apropiado según la acción HTTP:
        - Lectura (list, retrieve, me): UserReadSerializer.
        - Escritura (create, update, partial_update): UserWriteSerializer.
        - Cambio de contraseña: ChangePasswordSerializer.
        """
        if self.action in ('list', 'retrieve', 'me'):
            return UserReadSerializer
        if self.action == 'set_password':
            return ChangePasswordSerializer
        return UserWriteSerializer

    def get_permissions(self) -> list[Any]:
        """
        Permisos por acción:
        - me y set_password: cualquier usuario autenticado.
        - list y retrieve: cualquier usuario autenticado.
        - create, update, partial_update, destroy: exclusivo ADMIN.
        """
        if self.action in ('me', 'set_password', 'list', 'retrieve'):
            return [IsAuthenticatedAdcon()]
        # Escritura: gestión de usuarios solo para ADMIN
        return [AdminOnlyPermission()]

    @action(detail=False, methods=['get'], url_path='me', permission_classes=[IsAuthenticatedAdcon])
    def me(self, request: Request) -> Response:
        """
        Devuelve el perfil completo del usuario actualmente autenticado.

        GET /api/users/me/
        Respuesta: UserReadSerializer con todos los campos de perfil y RBAC.
        """
        serializer = UserReadSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        url_path='set-password',
        permission_classes=[IsAuthenticatedAdcon],
    )
    def set_password(self, request: Request, pk: int | None = None) -> Response:
        """
        Cambia la contraseña del usuario especificado.

        POST /api/users/{id}/set-password/
        Payload: { password_actual, password_nuevo, password_nuevo_confirmacion }

        Restricción: solo el propio usuario o un ADMIN puede cambiar la contraseña.
        Retorna 403 si un usuario intenta cambiar la contraseña de otro sin ser ADMIN.
        """
        user: User = self.get_object()

        # Verificación de identidad: solo el propio usuario o un ADMIN puede cambiar clave
        es_admin: bool = getattr(request.user, 'role', None) == User.Role.ADMIN
        if user.pk != request.user.pk and not (request.user.is_superuser or es_admin):
            return Response(
                {'detail': 'No tienes permiso para cambiar la contraseña de otro usuario.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': 'Contraseña actualizada correctamente.'},
            status=status.HTTP_200_OK,
        )
