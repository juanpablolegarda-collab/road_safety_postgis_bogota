from pathlib import Path
import pandas as pd
import geopandas as gpd

PROJECT_DIR = Path(__file__).resolve().parents[1]

csv_path = PROJECT_DIR / "data" / "raw" / "historico_siniestros_bogota.csv"
localidades_path = PROJECT_DIR / "data" / "external" / "localidades_bogota.geojson"

print("=" * 80)
print("INSPECCIÓN DEL DATASET DE SINIESTROS")
print("=" * 80)

print(f"Ruta CSV: {csv_path}")
print(f"Existe CSV: {csv_path.exists()}")
print(f"Tamaño CSV: {csv_path.stat().st_size / 1024 / 1024:.2f} MB")

# Intentamos leer el archivo con detección automática de separador.
try:
    df_sample = pd.read_csv(csv_path, sep=None, engine="python", nrows=1000, encoding="utf-8")
except UnicodeDecodeError:
    df_sample = pd.read_csv(csv_path, sep=None, engine="python", nrows=1000, encoding="latin1")

print("\nPrimeras filas:")
print(df_sample.head())

print("\nColumnas detectadas:")
for col in df_sample.columns:
    print(f"- {col}")

print("\nInformación general de la muestra:")
print(df_sample.info())

print("\nValores nulos en la muestra:")
print(df_sample.isna().sum())

print("\nPosibles columnas espaciales:")
spatial_keywords = ["lat", "lon", "long", "x", "y", "coord", "geo", "geom", "geometry"]
for col in df_sample.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in spatial_keywords):
        print(f"- {col}")

print("\nPosibles columnas temporales:")
date_keywords = ["fecha", "date", "anio", "año", "mes", "dia", "día"]
for col in df_sample.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in date_keywords):
        print(f"- {col}")

print("\nPosibles columnas de severidad / víctimas:")
severity_keywords = ["gravedad", "fatal", "lesionado", "victima", "víctima", "muerto", "herido", "clase", "tipo"]
for col in df_sample.columns:
    col_lower = col.lower()
    if any(keyword in col_lower for keyword in severity_keywords):
        print(f"- {col}")

print("\n" + "=" * 80)
print("INSPECCIÓN DE LOCALIDADES")
print("=" * 80)

print(f"Ruta GeoJSON: {localidades_path}")
print(f"Existe GeoJSON: {localidades_path.exists()}")
print(f"Tamaño GeoJSON: {localidades_path.stat().st_size / 1024 / 1024:.2f} MB")

gdf_localidades = gpd.read_file(localidades_path)

print("\nPrimeras filas de localidades:")
print(gdf_localidades.head())

print("\nColumnas de localidades:")
for col in gdf_localidades.columns:
    print(f"- {col}")

print("\nCRS de localidades:")
print(gdf_localidades.crs)

print("\nTipo de geometría:")
print(gdf_localidades.geometry.geom_type.value_counts())

print("\nCantidad de registros de localidades:")
print(len(gdf_localidades))

print("\n¿Geometrías válidas?")
print(gdf_localidades.is_valid.value_counts())