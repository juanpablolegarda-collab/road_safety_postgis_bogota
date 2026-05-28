from pathlib import Path
import os

import geopandas as gpd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


PROJECT_DIR = Path(__file__).resolve().parents[1]

SINIESTROS_GPKG = PROJECT_DIR / "data" / "processed" / "siniestros_bogota_clean.gpkg"
LOCALIDADES_GPKG = PROJECT_DIR / "data" / "processed" / "localidades_bogota_clean.gpkg"


def create_db_engine():
    env_path = PROJECT_DIR / ".env"
    load_dotenv(env_path)

    db_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(db_url)


def ensure_schemas(engine):
    schemas = ["raw", "clean", "geo", "analysis"]

    with engine.begin() as connection:
        for schema in schemas:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))

    print("Schemas verified:", ", ".join(schemas))


def reset_analysis_schema(engine):
    """
    Drop analysis schema before replacing base tables.

    This is required because analysis views depend on clean and geo tables.
    The views will be recreated later by run_sql_views.py.
    """
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA IF EXISTS analysis CASCADE;"))
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS analysis;"))

    print("Analysis schema reset successfully.")


def load_geodata():
    print("=" * 80)
    print("LOAD CLEAN GEODATA TO POSTGIS")
    print("=" * 80)

    engine = create_db_engine()

    ensure_schemas(engine)
    reset_analysis_schema(engine)

    print("\n1. Reading clean incident layer...")
    gdf_siniestros = gpd.read_file(SINIESTROS_GPKG, layer="siniestros_clean")

    print(f"Incident records: {len(gdf_siniestros)}")
    print(f"Incident CRS: {gdf_siniestros.crs}")

    print("\n2. Reading clean locality layer...")
    gdf_localidades = gpd.read_file(LOCALIDADES_GPKG, layer="localidades_clean")

    print(f"Locality records: {len(gdf_localidades)}")
    print(f"Locality CRS: {gdf_localidades.crs}")

    print("\n3. Loading incidents to clean.siniestros_bogota...")
    gdf_siniestros.to_postgis(
        name="siniestros_bogota",
        con=engine,
        schema="clean",
        if_exists="replace",
        index=False,
    )

    print("Loaded: clean.siniestros_bogota")

    print("\n4. Loading localities to geo.localidades_bogota...")
    gdf_localidades.to_postgis(
        name="localidades_bogota",
        con=engine,
        schema="geo",
        if_exists="replace",
        index=False,
    )

    print("Loaded: geo.localidades_bogota")

    print("\n5. Creating spatial indexes...")

    with engine.begin() as connection:
        connection.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_siniestros_bogota_geom
            ON clean.siniestros_bogota
            USING GIST (geometry);
            """)
        )

        connection.execute(
            text("""
            CREATE INDEX IF NOT EXISTS idx_localidades_bogota_geom
            ON geo.localidades_bogota
            USING GIST (geometry);
            """)
        )

    print("Spatial indexes created.")

    print("\n6. Validating loaded tables...")

    with engine.connect() as connection:
        siniestros_count = connection.execute(
            text("SELECT COUNT(*) FROM clean.siniestros_bogota;")
        ).scalar()

        localidades_count = connection.execute(
            text("SELECT COUNT(*) FROM geo.localidades_bogota;")
        ).scalar()

        srid_siniestros = connection.execute(
            text("""
            SELECT ST_SRID(geometry)
            FROM clean.siniestros_bogota
            WHERE geometry IS NOT NULL
            LIMIT 1;
            """)
        ).scalar()

        srid_localidades = connection.execute(
            text("""
            SELECT ST_SRID(geometry)
            FROM geo.localidades_bogota
            WHERE geometry IS NOT NULL
            LIMIT 1;
            """)
        ).scalar()

    print(f"clean.siniestros_bogota: {siniestros_count} records")
    print(f"geo.localidades_bogota: {localidades_count} records")
    print(f"SRID siniestros: {srid_siniestros}")
    print(f"SRID localidades: {srid_localidades}")

    print("\n" + "=" * 80)
    print("POSTGIS LOAD COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    load_geodata()