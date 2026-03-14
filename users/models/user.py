"""
Modelo de usuario personalizado del sistema Adcon.

Extiende AbstractUser de Django para mantener compatibilidad total con
el sistema de autenticación, sesiones y administración estándar, mientras
agrega los campos específicos requeridos por el Control de Acceso Basado
en Roles (RBAC) del ecosistema CLM.

Regla de seguridad: Este modelo es la fuente de verdad de identidad del sistema.
Toda operación de escritura queda vinculada a una instancia de este modelo
en la tabla historial_registros (patrón Maker-Checker).
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Usuario del sistema Adcon.

    Hereda de AbstractUser los campos estándar de Django:
    username, email, first_name, last_name, password,
    is_staff, is_active, is_superuser, date_joined, last_login.

    Se agregan campos específicos del negocio para soportar:
    - Identificación fiscal (RFC) del operador.
    - Contacto telefónico para soporte y notificaciones.
    - Rol de sistema para RBAC de alto nivel.
    - Marca de tiempo de última actualización del perfil.
    """

    class RolSistema(models.TextChoices):
        """
        Roles de alto nivel que determinan el nivel de acceso
        del usuario dentro de la plataforma Adcon.

        Estos roles complementan el sistema de permisos granulares
        de Django (is_staff / is_superuser / groups).
        """
        ADMINISTRADOR = 'ADMIN',     'Administrador'
        GESTOR        = 'GESTOR',    'Gestor de Contratos'
        REVISOR       = 'REVISOR',   'Revisor / Auditor'
        CONSULTOR     = 'CONSULTOR', 'Consultor (Solo Lectura)'

    # ── IDENTIFICACIÓN FISCAL ─────────────────────────────────────────────────
    rfc = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        unique=True,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes del operador. Opcional pero único si se captura.',
    )

    # ── CONTACTO ──────────────────────────────────────────────────────────────
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Teléfono',
        help_text='Número de contacto para soporte y notificaciones urgentes.',
    )

    # ── RBAC DE ALTO NIVEL ────────────────────────────────────────────────────
    rol_sistema = models.CharField(
        max_length=20,
        choices=RolSistema.choices,
        default=RolSistema.CONSULTOR,
        verbose_name='Rol en el Sistema',
        help_text=(
            'Define el nivel de acceso global del usuario en Adcon. '
            'El permiso granular se gestiona mediante Groups de Django.'
        ),
    )

    # ── AUDITORÍA DE PERFIL ───────────────────────────────────────────────────
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización del Perfil',
        help_text='Se actualiza automáticamente cada vez que se modifica el registro del usuario.',
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['username']

    def __str__(self) -> str:
        """Representación legible: nombre completo o username como fallback."""
        nombre_completo = self.get_full_name()
        return nombre_completo if nombre_completo else self.username

    @property
    def es_administrador(self) -> bool:
        """Verifica si el usuario tiene rol de administrador del sistema."""
        return self.rol_sistema == self.RolSistema.ADMINISTRADOR

    @property
    def puede_escribir(self) -> bool:
        """
        Verifica si el usuario tiene permisos para crear o modificar registros.
        Los roles CONSULTOR y REVISOR son de solo lectura a nivel de negocio.
        """
        return self.rol_sistema in (
            self.RolSistema.ADMINISTRADOR,
            self.RolSistema.GESTOR,
        )
