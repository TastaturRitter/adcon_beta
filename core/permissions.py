"""
Sistema de permisos RBAC para el ecosistema Adcon CLM.

Define la clase base AdconBasePermission que evalúa el campo `role`
del usuario para determinar qué operaciones HTTP están permitidas,
y clases derivadas para casos de uso específicos.

Matriz de permisos por rol:

    | Método HTTP         | ADMIN | MANAGER | EDITOR | READER |
    |---------------------|-------|---------|--------|--------|
    | GET (consulta)      |  ✓    |  ✓      |  ✓     |  ✓     |
    | HEAD / OPTIONS      |  ✓    |  ✓      |  ✓     |  ✓     |
    | POST (creación)     |  ✓    |  ✓      |  ✗     |  ✗     |
    | PUT / PATCH (edit.) |  ✓    |  ✓      |  ✓     |  ✗     |
    | DELETE (eliminac.)  |  ✓    |  ✓      |  ✗     |  ✗     |

Regla de seguridad: la gestión de usuarios (UserViewSet write actions)
es exclusiva del rol ADMIN, independientemente del método HTTP.
"""

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

# Métodos que únicamente requieren capacidad de lectura
_READ_METHODS: frozenset[str] = frozenset({'GET', 'HEAD', 'OPTIONS'})

# Métodos que solo requieren capacidad de edición (sin crear ni eliminar)
_EDIT_METHODS: frozenset[str] = frozenset({'PUT', 'PATCH'})

# Métodos que implican escritura destructiva (crear o eliminar registros)
_WRITE_METHODS: frozenset[str] = frozenset({'POST', 'DELETE'})


class AdconBasePermission(BasePermission):
    """
    Permiso base del sistema RBAC de Adcon.

    Evalúa el campo `role` del usuario autenticado contra la matriz
    de permisos por método HTTP. Aplica a todos los recursos de negocio
    (instrumentos, partes, documentos, activos, catálogos, etc.).

    Uso:
        permission_classes = [AdconBasePermission]
    """

    message: str = (
        'Tu rol no cuenta con los permisos suficientes para realizar esta operación.'
    )

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Valida si el usuario tiene el rol requerido para el método HTTP solicitado.

        Retorna False (403) cuando:
        - El usuario no está autenticado.
        - El método HTTP requiere un rol mayor al que tiene el usuario.
        """
        # Bloquear acceso a usuarios no autenticados
        if not request.user or not request.user.is_authenticated:
            self.message = 'Las credenciales de autenticación no fueron proporcionadas.'
            return False

        # Los superusuarios de Django siempre tienen acceso (compatibilidad con admin)
        if request.user.is_superuser:
            return True

        role: str = getattr(request.user, 'role', None)

        # Acceso de solo lectura: permitido a todos los roles autenticados
        if request.method in _READ_METHODS:
            return role is not None

        # Acceso de edición (PUT/PATCH): ADMIN, MANAGER y EDITOR
        if request.method in _EDIT_METHODS:
            return role in ('ADMIN', 'MANAGER', 'EDITOR')

        # Escritura destructiva (POST/DELETE): solo ADMIN y MANAGER
        if request.method in _WRITE_METHODS:
            return role in ('ADMIN', 'MANAGER')

        # Bloquear cualquier otro método no contemplado
        return False


class AdminOnlyPermission(BasePermission):
    """
    Permiso exclusivo para el rol ADMIN del sistema Adcon.

    Aplica estrictamente a la gestión de usuarios (UserViewSet):
    solo el rol ADMIN puede crear, modificar o eliminar cuentas de usuario.
    Esto cumple con el principio de mínimo privilegio y la separación
    de funciones requerida por los estándares de seguridad del CLM.

    Uso:
        permission_classes = [AdminOnlyPermission]
    """

    message: str = (
        'La gestión de usuarios está reservada exclusivamente para el rol Administrador.'
    )

    def has_permission(self, request: Request, view: APIView) -> bool:
        """
        Permite el acceso únicamente si el usuario tiene rol ADMIN
        o es superusuario de Django (compatibilidad con el panel de administración).
        """
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        return getattr(request.user, 'role', None) == 'ADMIN'


class IsAuthenticatedAdcon(BasePermission):
    """
    Verificación de autenticación mínima para el sistema Adcon.

    Reemplaza IsAuthenticated de DRF con un mensaje de error en español
    y coherente con el ecosistema Adcon. Actúa como piso mínimo de seguridad.

    Uso:
        permission_classes = [IsAuthenticatedAdcon]
    """

    message: str = 'Debes iniciar sesión para acceder a este recurso.'

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Retorna True solo si el usuario está autenticado."""
        return bool(request.user and request.user.is_authenticated)
