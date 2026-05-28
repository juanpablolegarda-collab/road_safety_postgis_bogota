# Pipeline Execution

## Project

Road Safety Geospatial Pipeline - Bogotá

## Purpose

This document describes how to execute the main geospatial data pipeline.

The pipeline processes raw road traffic incident data, builds a clean geospatial dataset, loads it into PostgreSQL/PostGIS and creates SQL analysis views.

## Main Command

To execute the full pipeline, run:

```powershell
python src\run_pipeline.py
```

## Pipeline Steps

The main pipeline executes the following scripts:

### 1. Build clean dataset

Script:

```text
src/build_clean_dataset.py
```

Purpose:

- Reads the raw incident CSV.
- Normalizes column names.
- Converts dates and coordinates.
- Creates point geometries from longitude and latitude.
- Performs a spatial join with official locality polygons.
- Assigns the analytical locality using spatial intersection.
- Preserves the original locality field for traceability.
- Exports clean GeoPackage, GeoJSON and CSV files.

Main outputs:

```text
data/processed/siniestros_bogota_clean.gpkg
data/processed/siniestros_bogota_clean.geojson
data/processed/siniestros_bogota_clean.csv
data/processed/localidades_bogota_clean.gpkg
```

---

### 2. Load clean data to PostGIS

Script:

```text
src/load_to_postgis.py
```

Purpose:

- Reads the clean GeoPackage files.
- Loads incident points into `clean.siniestros_bogota`.
- Loads locality polygons into `geo.localidades_bogota`.
- Creates spatial indexes.
- Validates record counts.
- Validates SRID values.

PostGIS output tables:

```text
clean.siniestros_bogota
geo.localidades_bogota
```

Expected validation:

```text
clean.siniestros_bogota: 199146 records
geo.localidades_bogota: 20 records
SRID siniestros: 4686
SRID localidades: 4686
```

Important note:

The script resets the `analysis` schema before replacing base tables. This is necessary because the analysis views depend on the clean and geo tables.

The analysis views are recreated automatically in the next step.

---

### 3. Create SQL analysis views

Script:

```text
src/run_sql_views.py
```

Purpose:

- Executes SQL files stored in the `sql/` folder.
- Creates or recreates analysis views in the `analysis` schema.
- Automates the SQL analysis stage without manually copying SQL into pgAdmin.

SQL files executed:

```text
sql/04_spatial_analysis.sql
sql/05_risk_indicators.sql
```

Main analysis views:

```text
analysis.v_siniestros_por_localidad
analysis.v_siniestros_por_gravedad
analysis.v_siniestros_por_clase
analysis.v_siniestros_por_anio
analysis.v_siniestros_por_mes
analysis.v_siniestros_por_hora
analysis.v_localidades_con_siniestros
analysis.v_siniestros_fuera_localidad
analysis.v_indicadores_riesgo_localidad
analysis.v_gravedad_por_hora
analysis.v_clase_accidente_por_localidad
```

## Expected Terminal Output

The pipeline is considered successful when the terminal shows:

```text
PIPELINE COMPLETED SUCCESSFULLY
```

Example successful outputs:

```text
CLEAN DATASET COMPLETED SUCCESSFULLY
POSTGIS LOAD COMPLETED SUCCESSFULLY
SQL VIEWS CREATED SUCCESSFULLY
PIPELINE COMPLETED SUCCESSFULLY
```

## Validation in pgAdmin

After running the pipeline, the analysis views can be validated in pgAdmin with:

```sql
SELECT table_schema, table_name
FROM information_schema.views
WHERE table_schema = 'analysis'
ORDER BY table_name;
```

The incident table can be validated with:

```sql
SELECT COUNT(*)
FROM clean.siniestros_bogota;
```

Expected result:

```text
199146
```

The locality table can be validated with:

```sql
SELECT COUNT(*)
FROM geo.localidades_bogota;
```

Expected result:

```text
20
```

The spatial reference system can be validated with:

```sql
SELECT 
    GeometryType(geometry) AS geometry_type,
    ST_SRID(geometry) AS srid,
    COUNT(*) AS total
FROM clean.siniestros_bogota
GROUP BY GeometryType(geometry), ST_SRID(geometry);
```

Expected result:

```text
POINT | 4686 | 199146
```

For locality polygons:

```sql
SELECT 
    GeometryType(geometry) AS geometry_type,
    ST_SRID(geometry) AS srid,
    COUNT(*) AS total
FROM geo.localidades_bogota
GROUP BY GeometryType(geometry), ST_SRID(geometry);
```

Expected result:

```text
POLYGON | 4686 | 20
```

## Conceptual Workflow

The project follows this workflow:

```text
Raw open data
→ Python cleaning and transformation
→ GeoPackage / GeoJSON / CSV outputs
→ PostgreSQL/PostGIS loading
→ SQL spatial analysis views
→ QGIS cartographic visualization
→ GitHub documentation
```

## Why This Pipeline Matters

This pipeline makes the project reproducible.

Instead of manually repeating each step, the main process can be executed with:

```powershell
python src\run_pipeline.py
```

This demonstrates:

- Python scripting.
- Geospatial data cleaning.
- PostgreSQL/PostGIS integration.
- SQL spatial analysis.
- Automated creation of analysis views.
- Reproducible geospatial data engineering workflow.

## Current Status

Main pipeline automated successfully.

The following stages are completed:

```text
[OK] Raw data inspection
[OK] Data quality review
[OK] Clean dataset generation
[OK] PostGIS loading
[OK] Spatial indexes
[OK] SQL analysis views
[OK] QGIS map outputs
[OK] Pipeline automation
```