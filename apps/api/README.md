# API ALMA

API REST construida con FastAPI y SQLAlchemy para Microsoft SQL Server.

## Requisitos

- Python 3.10+
- ODBC Driver 17 for SQL Server
- SQL Server (local o remoto)

### Dependencias del sistema en Ubuntu 22.04

Antes de usar `pyodbc`, instala `unixODBC`:

```bash
sudo apt-get update
sudo apt-get install -y unixodbc unixodbc-dev
```

Si `DATABASE_URL` usa SQL Server con `driver=ODBC+Driver+17+for+SQL+Server` o `driver=ODBC+Driver+18+for+SQL+Server`, tambien necesitas instalar el driver de Microsoft para SQL Server. Si instalas la version 18, recuerda actualizar `DATABASE_URL` para que el nombre del driver coincida exactamente.

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd new-api
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/macOS
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```env
DATABASE_URL=mssql+pyodbc://usuario:password@localhost:1433/nombre_base_datos?driver=ODBC+Driver+17+for+SQL+Server
AUTH_SECRET_KEY=tu_secret_key_aqui
```

#### Formato de DATABASE_URL

```
mssql+pyodbc://USUARIO:PASSWORD@SERVIDOR:PUERTO/BASE_DATOS?driver=ODBC+Driver+17+for+SQL+Server
```

| Variable         | Descripción                          |
|------------------|--------------------------------------|
| `USUARIO`        | Nombre de usuario de SQL Server       |
| `PASSWORD`       | Contraseña del usuario               |
| `SERVIDOR`       | Dirección del servidor (localhost o IP)|
| `PUERTO`         | Puerto de SQL Server (por defecto 1433)|
| `BASE_DATOS`     | Nombre de la base de datos           |

**Ejemplo:**
```env
DATABASE_URL=mssql+pyodbc://sa:MiPassword123@localhost:1433/mi_base_datos?driver=ODBC+Driver+17+for+SQL+Server
AUTH_SECRET_KEY=supersecretkey123
```

### 5. Crear la base de datos

Asegúrate de que la base de datos especificada en `DATABASE_URL` exista en SQL Server:

```sql
CREATE DATABASE mi_base_datos;
GO
```

### 6. Ejecutar migraciones

```bash
alembic upgrade head
```

Esto creará todas las tablas y ejecutará los seeds iniciales (roles, usuarios demo, etc.).

### 7. Iniciar la API

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

Documentación automática: `http://localhost:8000/docs`

## Comandos útiles

### Migraciones

```bash
# Aplicar todas las migraciones
alembic upgrade head

# Generar nueva migración automáticamente
alembic revision --autogenerate -m "descripcion de la migracion"
```

### Desarrollo

```bash
# Iniciar con hot reload
uvicorn main:app --reload

# Especificar puerto
uvicorn main:app --reload --port 8001
```

## Modelos de datos

| Modelo              | Descripción                                  |
|---------------------|----------------------------------------------|
| `Usuario`           | Usuarios del sistema                         |
| `Rol`               | Roles (Administrador, Investigador)          |
| `Proyecto`          | Proyectos creados por usuarios                |
| `Experimento`       | Experimentos asociados a proyectos           |
| `EstadoExperimento` | Estados de experimentos                     |
| `CategoriaExperimento` | Categorías de experimentos              |
| `Anotacion`         | Anotaciones asociadas a experimentos       |
| `ComentarioExperimento` | Comentarios en experimentos         |
| `ComentarioAnotacion` | Comentarios en anotaciones            |
| `UsuarioRol`        | Relación muchos a muchos entre usuarios y roles |

## Usuarios demo

| Email              | Contraseña | Rol           |
|--------------------|------------|---------------|
| admin@demo.com     | 1a2b3c     | Administrador |
| investigador@demo.com | 1a2b3c   | Investigador  |

## Notas

- Las tablas se crean mediante migraciones de Alembic
- Si modificas los modelos, genera una nueva migración con `alembic revision --autogenerate`.
