# API ALMA

API REST construida con FastAPI y SQLAlchemy para Microsoft SQL Server.

## Requisitos

- Python 3.10+
- ODBC Driver 17 for SQL Server
- SQL Server (local o remoto)

## Instalación

### 1. Ingresar a la carpeta api

```bash
cd api 
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la carpeta `app/` con la siguiente configuración:

```env
DATABASE_URL=mssql+pyodbc://usuario:password@host:puerto/nombre_base_datos?driver=ODBC+Driver+17+for+SQL+Server
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


### 5. Crear la base de datos

Asegúrate de que la base de datos especificada en `DATABASE_URL` exista en SQL Server antes de iniciar la aplicación.

```sql
CREATE DATABASE mi_base_datos;
```

### 6. Iniciar la API

```bash
cd app
fastapi dev main.py
```

La API estará disponible en: `http://localhost:8000`

Documentación automática: `http://localhost:8000/docs`

## Modelos de datos

| Modelo              | Descripción                                  |
|---------------------|----------------------------------------------|
| `Usuario`           | Usuarios del sistema                         |
| `Rol`               | Roles (admin, usuario, etc.)                 |
| `Proyecto`          | Proyectos creados por usuarios               |
| `Experimento`       | Experimentos asociados a proyectos           |
| `EstadoExperimento` | Estados de experimentos                     |
| `Anotacion`         | Anotaciones asociadas a usuarios y experimentos |
| `UsuarioRol`        | Relación entre usuarios y roles |

## Notas

- Las tablas se crean automáticamente al iniciar la aplicación (via `create_all`).
- Si modificas los modelos, elimina las tablas existentes y reinicia la API para recrearlas.