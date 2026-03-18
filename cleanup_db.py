"""
Script de limpieza de base de datos para Adcon.

Elimina todas las tablas de los apps afectados por el cambio de UUID
y purga los registros de django_migrations para esos apps, permitiendo
una migración limpia desde cero.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adcon_beta.settings')
django.setup()

from django.db import connection

# Apps cuyos esquemas necesitan ser reconstruidos con UUIDs correctos
AFFECTED_APPS = ['addresses', 'assets', 'parties', 'documents', 'guarantees', 'instruments', 'legal', 'tracking']

# Tablas a eliminar en orden (respetando dependencias via CASCADE)
# Se usa CASCADE para que PostgreSQL maneje las dependencias automáticamente
TABLES_TO_DROP = [
    # Tracking app
    'actividades', 'hitos', 'incidencias', 'entregas',
    # Legal app
    'escrituras_facultades', 'escrituras_personalidad', 'escrituras', 'notarios',
    # Documents app
    'partidas', 'addenda', 'anexos', 'evidencias', 'modificatorios', 'documentos_gestion',
    # Instruments app — especializaciones primero
    'arrendamientos', 'compraventas_inmuebles', 'servicios_prestados', 'suministros_mercancias',
    'accionistas_en_acto', 'actos_corporativos', 'archivos_fisicos',
    'instrumento_parte', 'concursos', 'instrumentos',
    # Guarantees app
    'garantias', 'fianzas',
    # Assets / Parties
    'inmuebles',
    'sucursales', 'personas_fisicas', 'personas_morales', 'partes',
    # Addresses
    'domicilios',
]

with connection.cursor() as cursor:
    print("[1/2] Eliminando tablas...")
    for table in TABLES_TO_DROP:
        try:
            cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
            print(f"  ✓ {table}")
        except Exception as e:
            print(f"  ✗ {table}: {e}")

    print("\n[2/2] Purgando registros de django_migrations...")
    placeholders = ', '.join(['%s'] * len(AFFECTED_APPS))
    cursor.execute(f'DELETE FROM django_migrations WHERE app IN ({placeholders})', AFFECTED_APPS)
    print(f"  ✓ Registros eliminados para: {', '.join(AFFECTED_APPS)}")

print("\n✅ Base de datos lista. Ejecuta 'python manage.py migrate' para reconstruir el esquema.")
