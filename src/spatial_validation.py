from pathlib import Path
import pandas as pd
import geopandas as gpd

PROJECT_DIR = Path(__file__).resolve().parents[1]

csv_path = PROJECT_DIR / "data" / "raw" / "historico_siniestros_bogota.csv"
localidades_path = PROJECT_DIR / "data" / "external" / "localidades_bogota.geojson"

print("=" * 80)
print("SPATIAL VALIDATION - ROAD INCIDENTS VS LOCALIDADES")
print("=" * 80)

# Leer siniestros
try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding="latin1")

df.columns = (
    df.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

# Convertir coordenadas
df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

# Crear GeoDataFrame de puntos.
# Usamos EPSG:4686 porque la capa oficial de localidades viene en EPSG:4686.
gdf_siniestros = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["LONGITUD"], df["LATITUD"]),
    crs="EPSG:4686"
)

# Leer localidades
gdf_localidades = gpd.read_file(localidades_path)

print("\nCRS siniestros:")
print(gdf_siniestros.crs)

print("\nCRS localidades:")
print(gdf_localidades.crs)

# Asegurar mismo CRS
if gdf_siniestros.crs != gdf_localidades.crs:
    gdf_siniestros = gdf_siniestros.to_crs(gdf_localidades.crs)

# Seleccionar columnas útiles de localidades
localidades_cols = ["LocNombre", "LocCodigo", "geometry"]
gdf_localidades_simple = gdf_localidades[localidades_cols].copy()

# Spatial join: puntos dentro de polígonos
joined = gpd.sjoin(
    gdf_siniestros,
    gdf_localidades_simple,
    how="left",
    predicate="within"
)

print("\n1. Total de siniestros:")
print(len(joined))

print("\n2. Siniestros que caen dentro de una localidad oficial:")
inside_count = joined["LocNombre"].notna().sum()
print(inside_count)

print("\n3. Siniestros que NO caen dentro de una localidad oficial:")
outside_count = joined["LocNombre"].isna().sum()
print(outside_count)

print("\n4. Porcentaje fuera de localidad oficial:")
outside_percent = round((outside_count / len(joined)) * 100, 4)
print(f"{outside_percent}%")

print("\n5. Localidades calculadas espacialmente:")
print(joined["LocNombre"].value_counts(dropna=False).sort_index())

print("\n6. Registros con LOCALIDAD original nula:")
original_null = joined["LOCALIDAD"].isna().sum()
print(original_null)

print("\n7. Registros con LOCALIDAD original nula pero recuperada espacialmente:")
recovered = joined[joined["LOCALIDAD"].isna() & joined["LocNombre"].notna()]
print(len(recovered))

if len(recovered) > 0:
    print("\nMuestra de registros recuperables:")
    print(
        recovered[
            ["CODIGO_ACCIDENTE", "FECHA_OCURRENCIA_ACC", "LATITUD", "LONGITUD", "LOCALIDAD", "LocNombre"]
        ].head(20)
    )

print("\n8. Comparación LOCALIDAD original vs localidad espacial:")

comparison = joined[["LOCALIDAD", "LocNombre"]].copy()
comparison["LOCALIDAD_NORMALIZED"] = (
    comparison["LOCALIDAD"]
    .astype(str)
    .str.upper()
    .str.strip()
)

comparison["LOCNOMBRE_NORMALIZED"] = (
    comparison["LocNombre"]
    .astype(str)
    .str.upper()
    .str.strip()
)

comparison["matches"] = comparison["LOCALIDAD_NORMALIZED"] == comparison["LOCNOMBRE_NORMALIZED"]

valid_comparison = comparison[
    comparison["LOCALIDAD"].notna() & comparison["LocNombre"].notna()
]

matches = valid_comparison["matches"].sum()
total_valid = len(valid_comparison)
mismatches = total_valid - matches

print(f"Comparaciones válidas: {total_valid}")
print(f"Coincidencias: {matches}")
print(f"No coincidencias: {mismatches}")

if total_valid > 0:
    match_percent = round((matches / total_valid) * 100, 2)
    print(f"Porcentaje de coincidencia: {match_percent}%")

if mismatches > 0:
    print("\nMuestra de posibles diferencias:")
    mismatch_sample = joined[
        (comparison["LOCALIDAD"].notna())
        & (comparison["LocNombre"].notna())
        & (~comparison["matches"])
    ][["CODIGO_ACCIDENTE", "LOCALIDAD", "LocNombre", "LATITUD", "LONGITUD"]].head(20)

    print(mismatch_sample)

print("\n9. Exportar muestra de puntos fuera de localidad oficial")

outside_points = joined[joined["LocNombre"].isna()].copy()

output_path = PROJECT_DIR / "data" / "processed" / "siniestros_fuera_localidad.geojson"

if len(outside_points) > 0:
    outside_points.to_file(output_path, driver="GeoJSON")
    print(f"Archivo exportado: {output_path}")
else:
    print("No hay puntos fuera de localidades oficiales. No se exporta archivo.")

print("\n" + "=" * 80)
print("SPATIAL VALIDATION COMPLETED")
print("=" * 80)