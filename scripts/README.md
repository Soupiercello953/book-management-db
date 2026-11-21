# Book Management Database

Implementación de la base de datos relacional `book_management` en PostgreSQL utilizando Python (`SQLAlchemy`, `psycopg2`, `pandas` y `python-dotenv`) en el entorno de Conda `dbman`.

## Estructura del proyecto

- `data/`: archivos CSV de origen (`categories.csv`, `authors.csv`, `users.csv`, `books.csv`, `book_authors.csv`).
- `sql/`: scripts SQL (`01_create_tables.sql`, `02_validate_data.sql` y `00_reset_demo.sql`).
- `scripts/`: scripts de conexión, creación de esquema, carga de datos y verificación (`db_config.py`, `test_connection.py`, `create_schema.py`, `import_csv.py`, `verify_database.py`).
- `.env.example`: plantilla de variables de entorno para la conexión a PostgreSQL.
- `.env`: credenciales locales de conexión (ignorado por Git; no se sube al repositorio).

## Configuración y ejecución

1. Crear el entorno de Conda e instalar dependencias:
   ```bash
   conda create -n dbman python=3.11 -y
   conda activate dbman
   python -m pip install -r requirements.txt