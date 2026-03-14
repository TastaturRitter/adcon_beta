"""
Configuración principal del proyecto Django para Adcon Beta.

Todas las variables sensibles son cargadas desde el archivo .env
usando python-dotenv. NUNCA deben estar hardcodeadas en este archivo.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ─────────────────────────────────────────────────────────────────────────────
# Rutas base del proyecto usando pathlib para portabilidad entre sistemas
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde el archivo .env en la raíz del backend
load_dotenv(BASE_DIR / '.env')


# ─────────────────────────────────────────────────────────────────────────────
# Configuración de seguridad básica
# Estas variables DEBEN existir en .env — se falla rápido si no están presentes
# ─────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')


# ─────────────────────────────────────────────────────────────────────────────
# Aplicaciones instaladas — Framework Django + Apps del ecosistema Adcon
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Librería para integración con AWS S3 como backend de almacenamiento
    'storages',

    # Aplicaciones del dominio Adcon
    'assets',
    'audit',
    'core',
    'documents',
    'addresses',
    'guarantees',
    'instruments',
    'legal',
    'parties',
    'tracking',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'adcon_beta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'adcon_beta.wsgi.application'

# Modelo de usuario personalizado del ecosistema Adcon
AUTH_USER_MODEL = 'users.User'


# ─────────────────────────────────────────────────────────────────────────────
# Base de Datos — PostgreSQL
# Los credenciales se obtienen exclusivamente desde variables de entorno
# ─────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# Almacenamiento en AWS S3 — Documentos legales y activos multimedia de Adcon
#
# Política de seguridad obligatoria:
#   - Cifrado en servidor (SSE) con algoritmo AES256 en cada objeto subido.
#   - Los objetos se crean como privados (ACL deshabilitado para conformidad).
#   - Las URLs firmadas tienen expiración para minimizar exposición.
# ─────────────────────────────────────────────────────────────────────────────
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')

# Cifrado AES256 obligatorio para cumplimiento legal de contratos
AWS_S3_OBJECT_PARAMETERS = {
    'ServerSideEncryption': 'AES256',
}

# No conceder ACLs públicas — acceso controlado siempre mediante URLs firmadas
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False

# Expiración de URLs pre-firmadas en segundos (1 hora)
AWS_QUERYSTRING_EXPIRE = 3600

# Dominio personalizado del bucket para optimizar latencia
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

# Configuración del backend de almacenamiento de archivos de medios
STORAGES = {
    # Archivos estáticos servidos localmente (CSS, JS, imágenes del sistema)
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
    # Archivos de medios (contratos, PDFs, documentos legales) → AWS S3
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
    },
}

# URL pública base para archivos de medios alojados en S3
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'


# ─────────────────────────────────────────────────────────────────────────────
# Archivos estáticos del sistema (CSS, JavaScript, Imágenes del Admin)
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# ─────────────────────────────────────────────────────────────────────────────
# Validación de contraseñas — política estándar de Django
# ─────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────────────────────────────────
# Internacionalización y zona horaria
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True


# ─────────────────────────────────────────────────────────────────────────────
# Clave primaria por defecto para modelos que no la declaren explícitamente
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
