from pathlib import Path
import unicodedata
import pandas as pd
import geopandas as gpd

PROJECT_DIR = Path(__file__).resolve().parents[1]

RAW_CSV = PROJECT_DIR / "data" / "raw" / "historico_siniestros_bogota.csv"
LOCALIDADES_GEOJSON = PROJECT_DIR / "data" / "external" / "localidades_bogota.geojson"

OUTPUT_GPKG = PROJECT_DIR / "data" / "processed" / "siniestros_bogota_clean.gpkg"
OUTPUT_GEOJSON = PROJECT_DIR / "data" / "processed" / "siniestros_bogota_clean.geojson"
OUTPUT_CSV = PROJECT_DIR / "data" / "processed" / "siniestros_bogota_clean.csv"

OUTPUT_LOCALIDADES = PROJECT_DIR / "data" / "processed" / "localidades_bogota_clean.gpkg"


def normalize_column_name(value: str) -> str:
    value = value.replace("\ufeff", "").strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace(" ", "_")
    value = value.replace("-", "_")
    return value


def normalize_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip().upper()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return value


def build_clean_dataset():
    print("=" * 80)
    print("BUILD CLEAN DATASET - SINIESTROS BOGOTÁ")
    print("=" * 80)

    print("\n1. Reading raw CSV...")

    try:
        df = pd.read_csv(RAW_CSV, encoding="utf-8-sig")
    except UnicodeDecodeError:
        df = pd.read_csv(RAW_CSV, encoding="latin1")

    print(f"Raw records: {len(df)}")
    print(f"Raw columns: {len(df.columns)}")

    print("\n2. Normalizing column names...")

    df.columns = [normalize_column_name(col) for col in df.columns]

    print("Columns after normalization:")
    for col in df.columns:
        print(f"- {col}")

    print("\n3. Converting data types...")

    df["latitud"] = pd.to_numeric(df["latitud"], errors="coerce")
    df["longitud"] = pd.to_numeric(df["longitud"], errors="coerce")

    df["fecha_ocurrencia"] = pd.to_datetime(
        df["fecha_ocurrencia_acc"],
        errors="coerce",
        utc=True
    ).dt.tz_convert(None)

    df["fecha_hora"] = pd.to_datetime(
        df["fecha_hora_acc"],
        errors="coerce",
        utc=True
    ).dt.tz_convert(None)

    df["anio"] = df["fecha_ocurrencia"].dt.year
    df["mes"] = df["fecha_ocurrencia"].dt.month
    df["dia"] = df["fecha_ocurrencia"].dt.day
    df["hora"] = df["fecha_hora"].dt.hour
    df["dia_semana_num"] = df["fecha_ocurrencia"].dt.dayofweek

    dias_semana = {
        0: "lunes",
        1: "martes",
        2: "miercoles",
        3: "jueves",
        4: "viernes",
        5: "sabado",
        6: "domingo",
    }

    df["dia_semana"] = df["dia_semana_num"].map(dias_semana)

    print("\n4. Creating point geometries...")

    gdf_siniestros = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitud"], df["latitud"]),
        crs="EPSG:4686"
    )

    print(f"Incident CRS: {gdf_siniestros.crs}")

    print("\n5. Reading locality polygons...")

    gdf_localidades = gpd.read_file(LOCALIDADES_GEOJSON)

    print(f"Locality records: {len(gdf_localidades)}")
    print(f"Locality CRS: {gdf_localidades.crs}")

    if gdf_localidades.crs != gdf_siniestros.crs:
        gdf_localidades = gdf_localidades.to_crs(gdf_siniestros.crs)

    print("\n6. Cleaning locality layer...")

    gdf_localidades_clean = gdf_localidades.rename(
        columns={
            "LocNombre": "localidad_nombre",
            "LocCodigo": "localidad_codigo",
            "LocArea": "localidad_area",
        }
    ).copy()

    locality_cols = [
        "localidad_nombre",
        "localidad_codigo",
        "geometry"
    ]

    gdf_localidades_for_join = gdf_localidades_clean[locality_cols].copy()

    print("\n7. Spatial join: incidents within official locality polygons...")

    joined = gpd.sjoin(
        gdf_siniestros,
        gdf_localidades_for_join,
        how="left",
        predicate="within"
    )

    joined["inside_localidad"] = joined["localidad_nombre"].notna()

    joined["localidad_original"] = joined["localidad"]
    joined["localidad_espacial"] = joined["localidad_nombre"]

    joined["localidad_final"] = (
    joined["localidad_espacial"]
    .fillna(joined["localidad_original"])
    .fillna("SIN_LOCALIDAD_ASIGNADA")
)

    joined["localidad_original_norm"] = joined["localidad_original"].apply(normalize_text)
    joined["localidad_espacial_norm"] = joined["localidad_espacial"].apply(normalize_text)

    print("\n8. Building final schema...")

    final_columns = [
        "objectid",
        "formulario",
        "codigo_accidente",
        "fecha_ocurrencia",
        "fecha_hora",
        "anio",
        "mes",
        "dia",
        "hora",
        "dia_semana",
        "direccion",
        "gravedad",
        "clase_acc",
        "localidad_original",
        "localidad_espacial",
        "localidad_final",
        "inside_localidad",
        "latitud",
        "longitud",
        "civ",
        "pk_calzada",
        "geometry",
    ]

    gdf_clean = joined[final_columns].copy()

    gdf_clean = gdf_clean.rename(
        columns={
            "clase_acc": "clase_accidente"
        }
    )

    print("\n9. Quality control of clean dataset...")

    print(f"Clean records: {len(gdf_clean)}")
    print(f"Clean columns: {len(gdf_clean.columns)}")

    print("\nNull values in final dataset:")
    print(gdf_clean.isna().sum())

    print("\nInside locality:")
    print(gdf_clean["inside_localidad"].value_counts(dropna=False))

    print("\nSeverity distribution:")
    print(gdf_clean["gravedad"].value_counts(dropna=False))

    print("\nAccident class distribution:")
    print(gdf_clean["clase_accidente"].value_counts(dropna=False))

    print("\nTemporal coverage:")
    print(f"Minimum date: {gdf_clean['fecha_ocurrencia'].min()}")
    print(f"Maximum date: {gdf_clean['fecha_ocurrencia'].max()}")

    print("\n10. Exporting clean outputs...")

    OUTPUT_GPKG.parent.mkdir(parents=True, exist_ok=True)

    gdf_clean.to_file(
        OUTPUT_GPKG,
        layer="siniestros_clean",
        driver="GPKG"
    )

    print(f"GeoPackage exported: {OUTPUT_GPKG}")

    gdf_clean.to_file(
        OUTPUT_GEOJSON,
        driver="GeoJSON"
    )

    print(f"GeoJSON exported: {OUTPUT_GEOJSON}")

    df_clean_no_geom = pd.DataFrame(gdf_clean.drop(columns="geometry"))
    df_clean_no_geom.to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"CSV exported: {OUTPUT_CSV}")

    gdf_localidades_clean.to_file(
        OUTPUT_LOCALIDADES,
        layer="localidades_clean",
        driver="GPKG"
    )

    print(f"Clean locality layer exported: {OUTPUT_LOCALIDADES}")

    print("\n" + "=" * 80)
    print("CLEAN DATASET COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    build_clean_dataset()