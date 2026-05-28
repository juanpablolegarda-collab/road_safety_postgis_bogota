import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(db_url)

try:
    with engine.connect() as connection:
        print("Conexión a PostgreSQL exitosa.")

        postgres_version = connection.execute(text("SELECT version();")).scalar()
        print("\nVersión de PostgreSQL:")
        print(postgres_version)

        postgis_version = connection.execute(text("SELECT postgis_full_version();")).scalar()
        print("\nVersión de PostGIS:")
        print(postgis_version)

        schemas_query = """
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name IN ('raw', 'clean', 'geo', 'analysis')
        ORDER BY schema_name;
        """

        schemas = pd.read_sql(schemas_query, connection)

        print("\nEsquemas del proyecto:")
        print(schemas)

except Exception as error:
    print("Error al conectar con PostgreSQL/PostGIS:")
    print(error)