from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
csv_path = PROJECT_DIR / "data" / "raw" / "historico_siniestros_bogota.csv"

print("=" * 80)
print("FULL QUALITY CHECK - HISTÓRICO SINIESTROS BOGOTÁ")
print("=" * 80)

try:
    df = pd.read_csv(csv_path, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding="latin1")

# Normalizar nombres solo para inspección
df.columns = (
    df.columns
    .str.replace("\ufeff", "", regex=False)
    .str.strip()
)

print("\n1. Dimensiones del dataset:")
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")

print("\n2. Columnas:")
for col in df.columns:
    print(f"- {col}")

print("\n3. Tipos de datos:")
print(df.dtypes)

print("\n4. Nulos por columna:")
print(df.isna().sum())

print("\n5. Porcentaje de nulos por columna:")
null_percent = (df.isna().mean() * 100).round(2)
print(null_percent)

print("\n6. Duplicados:")
print(f"Filas duplicadas completas: {df.duplicated().sum()}")

if "CODIGO_ACCIDENTE" in df.columns:
    print(f"Duplicados por CODIGO_ACCIDENTE: {df['CODIGO_ACCIDENTE'].duplicated().sum()}")

print("\n7. Revisión de fechas:")

for date_col in ["FECHA_OCURRENCIA_ACC", "FECHA_HORA_ACC"]:
    if date_col in df.columns:
        parsed_date = pd.to_datetime(df[date_col], errors="coerce", dayfirst=False)
        print(f"\nColumna: {date_col}")
        print(f"Fechas inválidas: {parsed_date.isna().sum()}")
        print(f"Fecha mínima: {parsed_date.min()}")
        print(f"Fecha máxima: {parsed_date.max()}")

print("\n8. Valores únicos de GRAVEDAD:")
if "GRAVEDAD" in df.columns:
    print(df["GRAVEDAD"].value_counts(dropna=False))

print("\n9. Valores únicos de CLASE_ACC:")
if "CLASE_ACC" in df.columns:
    print(df["CLASE_ACC"].value_counts(dropna=False))

print("\n10. Localidades detectadas:")
if "LOCALIDAD" in df.columns:
    print(df["LOCALIDAD"].value_counts(dropna=False).sort_index())

print("\n11. Validación de coordenadas:")

required_coords = ["LATITUD", "LONGITUD"]

if all(col in df.columns for col in required_coords):
    df["LATITUD"] = pd.to_numeric(df["LATITUD"], errors="coerce")
    df["LONGITUD"] = pd.to_numeric(df["LONGITUD"], errors="coerce")

    missing_coords = df["LATITUD"].isna().sum() + df["LONGITUD"].isna().sum()
    print(f"Valores faltantes o no numéricos en coordenadas: {missing_coords}")

    # Rango amplio esperado para Bogotá
    lat_min, lat_max = 4.3, 4.9
    lon_min, lon_max = -74.4, -73.9

    invalid_coords = df[
        ~(
            df["LATITUD"].between(lat_min, lat_max)
            & df["LONGITUD"].between(lon_min, lon_max)
        )
    ]

    print(f"Registros fuera del rango aproximado de Bogotá: {len(invalid_coords)}")

    print("\nResumen LATITUD:")
    print(df["LATITUD"].describe())

    print("\nResumen LONGITUD:")
    print(df["LONGITUD"].describe())

    if len(invalid_coords) > 0:
        print("\nMuestra de coordenadas fuera de rango:")
        print(
            invalid_coords[
                ["CODIGO_ACCIDENTE", "FECHA_OCURRENCIA_ACC", "LATITUD", "LONGITUD", "LOCALIDAD"]
            ].head(20)
        )

print("\n12. Revisión de columnas X/Y:")
if "X" in df.columns and "Y" in df.columns:
    print("Columnas X/Y detectadas.")
    print(df[["X", "Y", "LONGITUD", "LATITUD"]].head())
else:
    print("No se detectaron columnas X/Y limpias o hubo caracteres especiales en el nombre.")

print("\n" + "=" * 80)
print("QUALITY CHECK COMPLETED")
print("=" * 80)