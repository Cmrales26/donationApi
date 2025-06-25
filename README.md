# Backend de Donaciones de Útiles Escolares

Este `README.md` te proporciona los comandos esenciales para poner en marcha y gestionar el proyecto de backend de donaciones de útiles escolares, tanto en tu máquina local como utilizando Docker.

###📋 Prerequisitos

** Asegúrate de tener instalado:**

- Python 3.8+
- pip
- Docker y Docker Compose

### 💻 Entorno Loca

#### 1. Configuración Inicial

**Activar el entorno virtual:**

`source env/bin/activate # macOS/Linux`

`.\env\Scripts\activate # Windows`

**Instalar dependencias:**

`pip install -r requirements.txt`

### 2. Migraciones y Ejecución

**Aplicar migraciones a la base de datos:**

`python manage.py migrate`

**Iniciar el servidor de desarrollo:**

`python manage.py runserver`

# 🐳 Entorno Docker

`docker-compose up -d`

### 2. Migraciones y Comandos

**Ejecutar migraciones dentro del contenedor (asumiendo que tu servicio Django se llama `donationsapi_web_1`):**

`docker exec -it donationsapi_web_1 python manage.py migrate`

**Ejecutar comandos específicos dentro del contenedor (ej. crear superusuario):**

`docker exec -it donationsapi_web_1 python manage.py createsuperuser`

**Detener y eliminar los contenedores:**

`docker-compose down`

**Para eliminar también los volúmenes de datos**:

`docker-compose down -v`
