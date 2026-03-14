-----

# ✒️ Administrador de Contratos (AdCon)

> Repositorio del proyecto `adcon_bt`

Sistema web para la gestión integral de contratos, diseñado para despachos de abogados y departamentos legales. La aplicación permite un control detallado sobre instrumentos, partes involucradas, fechas clave, documentos y actividades relacionadas.

El proyecto está construido sobre una arquitectura modular en **Django**, utilizando PostgreSQL como motor de base de datos y **Bootstrap 5** para una interfaz de usuario limpia y responsiva.

-----

## ✅ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado el siguiente software en tu sistema:

  * **Python** (versión 3.11 o superior)
  * **Pip** y **Venv** (generalmente incluidos con Python)
  * **PostgreSQL** (versión 14 o superior, con una instancia en ejecución)
  * **Git** para el control de versiones

-----

## 🚀 Instalación

Sigue estos pasos para configurar el entorno de desarrollo local.

1.  **Clonar el repositorio**

    ```powershell
    git clone https://github.com/tu-usuario/adcon_bt.git
    cd adcon_bt
    ```

2.  **Crear y activar el entorno virtual**

    ```powershell
    # Crear el entorno virtual
    python -m venv venv

    # Activar en Windows
    .\venv\Scripts\activate

    # Nota: Para activar en macOS/Linux, usa: source venv/bin/activate
    ```

3.  **Instalar dependencias**
    El archivo `requirements.txt` contiene todos los paquetes de Python necesarios.

    ```powershell
    pip install -r requirements.txt
    ```

4.  **Configurar las variables de entorno**
    Este proyecto utiliza un archivo `.env` para gestionar datos sensibles. Crea una copia del archivo de ejemplo y edítala con tus credenciales.

    ```powershell
    # En Windows
    copy .env.example .env

    # En macOS/Linux
    # cp .env.example .env
    ```

    Luego, abre el archivo `.env` y rellena las variables (más detalles abajo).

5.  **Configurar la base de datos**
    Asegúrate de que tu instancia de PostgreSQL esté en ejecución y crea una base de datos vacía para el proyecto.

    ```sql
    CREATE DATABASE adcon_bt_db;
    ```

    *No necesitas crear las tablas manualmente, Django se encargará de eso.*

6.  **Ejecutar las migraciones**
    Este comando creará todas las tablas en la base de datos basándose en los modelos de Django.

    ```powershell
    python manage.py migrate
    ```

7.  **Crear un superusuario**
    Necesitarás un usuario administrador para acceder al panel de Django (`/admin`).

    ```powershell
    python manage.py createsuperuser
    ```

    Sigue las instrucciones en pantalla para crear tu usuario.

-----

## ⚙️ Variables de Entorno

El archivo `.env` es crucial para la configuración del proyecto y **debe ser ignorado por Git**. Contiene todas las credenciales y configuraciones específicas del entorno.

Abre el archivo `.env` que creaste y configúralo con tus datos:

```ini
# Archivo .env para variables de entorno del proyecto adcon_bt

# --- Configuración de Django ---
# ¡Genera una nueva clave secreta para tu entorno!
SECRET_KEY='tu_clave_secreta_aqui'
DEBUG=True

# --- Base de Datos PostgreSQL ---
DB_NAME=adcon_bt_db
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_de_postgres
DB_HOST=localhost
DB_PORT=5432

# --- Hosts Permitidos ---
# En desarrollo, localhost es suficiente. En producción, añade tu dominio.
ALLOWED_HOSTS=127.0.0.1,localhost
```

-----

## ▶️ Ejecutar el Servidor de Desarrollo

Una vez completada la instalación, puedes iniciar el servidor de desarrollo de Django:

```powershell
python manage.py runserver
```

La aplicación estará disponible en tu navegador en la siguiente dirección: **[http://127.0.0.1:8000/](https://www.google.com/search?q=http://127.0.0.1:8000/)**

-----

## 📜 Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 [Adrian Martinez]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
