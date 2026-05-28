from pathlib import Path
import unicodedata
import pandas as pd
import geopandas as gpd

PROJECT_DIR = Path(__file__).resolve().parents[1]

csv_path = PROJECT_DIR / "data" / "raw" / "historico_siniestros_bogota.csv"
localidades_path = PROJECT_DIR / "data" / "external" / "localidades_bogota.geojson"

print("=" * 80)
print("REFINED SPATIAL VALIDATION - LOCALIDAD NORMALIZATION")
print("=" * 80)


def normalize_text(value):
    """
    Normalize text for comparison:
    - convert to string
    - uppercase
    - strip spaces
    - remove accents
    """
    if pd.isna(value):
        return None

    value = str(value).strip().upper()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return value


# Read incident dataset
try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding="latin1")

df.columns = (
    df.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

gdf_siniestros = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["LONGITUD"], df["LATITUD"]),
    crs="EPSG:4686"
)

# Read localidades
gdf_localidades = gpd.read_file(localidades_path)

if gdf_siniestros.crs != gdf_localidades.crs:
    gdf_siniestros = gdf_siniestros.to_crs(gdf_localidades.crs)

gdf_localidades_simple = gdf_localidades[["LocNombre", "LocCodigo", "geometry"]].copy()

# Spatial join
joined = gpd.sjoin(
    gdf_siniestros,
    gdf_localidades_simple,
    how="left",
    predicate="within"
)

# Normalize names
joined["localidad_original_norm"] = joined["LOCALIDAD"].apply(normalize_text)
joined["localidad_espacial_norm"] = joined["LocNombre"].apply(normalize_text)

# Compare only where both values exist
valid_comparison = joined[
    joined["localidad_original_norm"].notna()
    & joined["localidad_espacial_norm"].notna()
].copy()

valid_comparison["matches_refined"] = (
    valid_comparison["localidad_original_norm"]
    == valid_comparison["localidad_espacial_norm"]
)

matches = valid_comparison["matches_refined"].sum()
total_valid = len(valid_comparison)
mismatches = total_valid - matches

print("\n1. Total de registros:")
print(len(joined))

print("\n2. Registros dentro de localidad oficial:")
print(joined["LocNombre"].notna().sum())

print("\n3. Registros fuera de localidad oficial:")
print(joined["LocNombre"].isna().sum())

print("\n4. Comparación refinada sin tildes:")
print(f"Comparaciones válidas: {total_valid}")
print(f"Coincidencias refinadas: {matches}")
print(f"No coincidencias refinadas: {mismatches}")

if total_valid > 0:
    print(f"Porcentaje de coincidencia refinada: {round((matches / total_valid) * 100, 2)}%")

print("\n5. Mismatches reales después de normalización:")

real_mismatches = valid_comparison[~valid_comparison["matches_refined"]].copy()

print(f"Cantidad: {len(real_mismatches)}")

if len(real_mismatches) > 0:
    print("\nMuestra:")
    print(
        real_mismatches[
            [
                "CODIGO_ACCIDENTE",
                "LOCALIDAD",
                "LocNombre",
                "localidad_original_norm",
                "localidad_espacial_norm",
                "LATITUD",
                "LONGITUD",
            ]
        ].head(30)
    )

    output_path = PROJECT_DIR / "data" / "processed" / "localidad_mismatches_refined.csv"
    real_mismatches[
        [
            "CODIGO_ACCIDENTE",
            "FECHA_OCURRENCIA_ACC",
            "LOCALIDAD",
            "LocNombre",
            "localidad_original_norm",
            "localidad_espacial_norm",
            "LATITUD",
            "LONGITUD",
        ]
    ].to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nArchivo exportado: {output_path}")

print("\n6. Registros sin localidad original:")

missing_original = joined[joined["LOCALIDAD"].isna()].copy()
print(f"Cantidad: {len(missing_original)}")

print("\n7. Registros sin localidad original pero con localidad espacial:")
recoverable = missing_original[missing_original["LocNombre"].notna()].copy()
print(f"Cantidad recuperable: {len(recoverable)}")

if len(recoverable) > 0:
    print(
        recoverable[
            [
                "CODIGO_ACCIDENTE",
                "FECHA_OCURRENCIA_ACC",
                "LOCALIDAD",
                "LocNombre",
                "LATITUD",
                "LONGITUD",
            ]
        ].head(20)
    )

print("\n" + "=" * 80)
print("REFINED VALIDATION COMPLETED")
print("=" * 80)