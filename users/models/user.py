"""
Modelo de usuario personalizado del sistema Adcon.

Extiende AbstractUser para mantener compatibilidad total con el sistema
de autenticación estándar de Django, añadiendo un campo `role` que
implementa el Control de Acceso Basado en Roles (RBAC) del CLM.

Regla de seguridad: Este modelo es la fuente de verdad de identidad.
Toda operación de escritura queda auditada en historial_registros con
referencia al usuario que la ejecutó (patrón Maker-Checker).
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Usuario del sistema Adcon con RBAC de cuatro niveles.

    Los cuatro roles mapean a los siguientes niveles de acceso jurídico-operativo:

    ADMIN   → Administrador del sistema. Acceso total (CRUD) sobre todos los
              recursos, incluyendo la gestión de usuarios. Equivale a is_superuser
              a nivel de negocio. Reservado para el equipo de TI/Legal senior.

    MANAGER → Gestor de contratos. Acceso CRUD completo sobre todos los registros
              de negocio (instrumentos, partes, documentos, activos, etc.).
              No puede gestionar usuarios ni cambiar la configuración del sistema.

    EDITOR  → Editor. Puede consultar y editar registros existentes (GET, PATCH, PUT)
              pero NO puede crear nuevos contratos ni eliminar registros.
              Perfil para analistas jurídicos en revisión de expedientes.

    READER  → Lector. Acceso de solo lectura (GET) a todos los recursos públicos.
              Perfil para auditores externos, comités de revisión y consultas.

    Hereda de AbstractUser los campos: username, email, first_name, last_name,
    password, is_staff, is_active, is_superuser, date_joined, last_login.
    """

    class Role(models.TextChoices):
        """
        Enumeración de roles del sistema RBAC de Adcon.

        El valor de la base de datos (izquierda) es el que se persiste.
        La etiqueta (derecha) es la representación legible para la UI.
        """
        ADMIN   = 'ADMIN',   'Administrador'
        MANAGER = 'MANAGER', 'Gestor de Contratos'
        EDITOR  = 'EDITOR',  'Editor'
        READER  = 'READER',  'Lector (Solo Lectura)'

    # ── RBAC PRINCIPAL ────────────────────────────────────────────────────────
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.READER,
        verbose_name='Rol en el Sistema',
        db_index=True,
        help_text=(
            'Define el nivel de acceso del usuario en la plataforma Adcon. '
            'ADMIN: acceso total. MANAGER: CRUD en negocio. '
            'EDITOR: consulta y edición. READER: solo lectura.'
        ),
    )

    # ── IDENTIFICACIÓN FISCAL ─────────────────────────────────────────────────
    rfc = models.CharField(
        max_length=13,
        null=True,
        blank=True,
        unique=True,
        verbose_name='RFC',
        help_text='Registro Federal de Contribuyentes del operador. Único si se captura.',
    )

    # ── CONTACTO ──────────────────────────────────────────────────────────────
    telefono = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name='Teléfono',
        help_text='Número de contacto para soporte y notificaciones urgentes.',
    )

    # ── AUDITORÍA DE PERFIL ───────────────────────────────────────────────────
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización del Perfil',
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

    # ── PROPIEDADES DE CONVENIENCIA RBAC ──────────────────────────────────────

    @property
    def es_administrador(self) -> bool:
        """True si el rol del usuario es ADMIN (acceso total al sistema)."""
        return self.role == self.Role.ADMIN

    @property
    def es_gestor(self) -> bool:
        """True si el rol permite CRUD completo sobre registros de negocio."""
        return self.role in (self.Role.ADMIN, self.Role.MANAGER)

    @property
    def puede_escribir(self) -> bool:
        """
        True si el usuario puede crear o eliminar registros.
        Solo ADMIN y MANAGER tienen permiso de escritura destructiva.
        """
        return self.role in (self.Role.ADMIN, self.Role.MANAGER)

    @property
    def puede_editar(self) -> bool:
        """
        True si el usuario puede modificar registros existentes (PATCH/PUT).
        Incluye ADMIN, MANAGER y EDITOR. Excluye READER.
        """
        return self.role in (self.Role.ADMIN, self.Role.MANAGER, self.Role.EDITOR)
