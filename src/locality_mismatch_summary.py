from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

mismatch_path = PROJECT_DIR / "data" / "processed" / "localidad_mismatches_refined.csv"
output_path = PROJECT_DIR / "data" / "processed" / "localidad_mismatch_summary.csv"

print("=" * 80)
print("LOCALITY MISMATCH SUMMARY")
print("=" * 80)

if not mismatch_path.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo: {mismatch_path}. "
        "Ejecuta primero src\\refined_spatial_validation.py"
    )

df = pd.read_csv(mismatch_path, encoding="utf-8-sig")

print("\n1. Total de discrepancias:")
print(len(df))

print("\n2. Columnas disponibles:")
print(df.columns.tolist())

summary = (
    df.groupby(["LOCALIDAD", "LocNombre"])
    .size()
    .reset_index(name="count")
    .sort_values("count", ascending=False)
)

summary["percent_of_mismatches"] = (
    summary["count"] / len(df) * 100
).round(2)

print("\n3. Top 30 combinaciones de discrepancias:")
print(summary.head(30))

summary.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\nArchivo exportado: {output_path}")

print("\n4. Localidades originales con más discrepancias:")
print(
    df["LOCALIDAD"]
    .value_counts()
    .head(20)
)

print("\n5. Localidades espaciales que más reciben puntos discrepantes:")
print(
    df["LocNombre"]
    .value_counts()
    .head(20)
)

print("\n" + "=" * 80)
print("SUMMARY COMPLETED")
print("=" * 80)