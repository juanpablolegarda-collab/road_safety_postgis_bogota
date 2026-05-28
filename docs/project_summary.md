# Project Summary

## Road Safety Geospatial Pipeline - Bogotá

This project develops a reproducible geospatial data pipeline to analyze road traffic incidents in Bogotá D.C., Colombia, using Python, PostgreSQL/PostGIS and QGIS.

## Study Area

Bogotá D.C., Colombia.

## Period of Analysis

2015–2021.

## Objective

To process, clean, store, analyze and visualize georeferenced road traffic incident data using geospatial data engineering tools.

## Main Workflow

```text
Raw open data
→ Python data cleaning
→ Geospatial transformation
→ PostgreSQL/PostGIS loading
→ SQL spatial analysis views
→ QGIS cartographic visualization
→ Technical documentation
```

## Main Tools

- Python
- Pandas
- GeoPandas
- PostgreSQL
- PostGIS
- SQL
- QGIS
- Git/GitHub

## Main Datasets

- Road traffic incidents from Datos Abiertos Bogotá / Secretaría Distrital de Movilidad.
- Locality boundaries from IDECA / Secretaría Distrital de Planeación.

## Main Outputs

- Clean geospatial dataset of road traffic incidents.
- PostGIS spatial database.
- SQL analysis views.
- Five QGIS map outputs.
- Reproducible Python pipeline.
- Technical documentation.

## Main Maps

1. Spatial distribution of road traffic incidents.
2. Total incidents by locality.
3. Incident density by km².
4. Average severity by locality.
5. Incidents outside official locality polygons.

## Methodological Notes

- Incident points were created from latitude and longitude.
- Official locality polygons were used for spatial validation.
- The analytical locality was assigned spatially using official locality boundaries.
- Original locality values were preserved for traceability.
- Records outside official locality polygons were preserved and flagged.
- Density indicators were calculated using area in square kilometers.
- Area calculations were performed using projected geometries.
- The severity index is exploratory and is not an official road safety metric.
- Absolute counts and normalized density indicators were interpreted separately.

## Main Analytical Findings

- Kennedy, Engativá, Suba, Usaquén and Fontibón show the highest absolute number of registered road traffic incidents.
- Localities such as Los Mártires, Barrios Unidos, Puente Aranda, Antonio Nariño and Teusaquillo show high incident density per square kilometer.
- The exploratory severity index highlights localities such as Usme, San Cristóbal, Rafael Uribe Uribe, Ciudad Bolívar and Bosa.
- A total of 57 incident points were identified outside official locality polygons.
- The results should be interpreted as exploratory spatial analysis, not as an official road safety risk diagnosis.

## Data Quality Work

The project includes a data quality validation stage focused on:

- Checking missing values.
- Checking duplicate records.
- Validating date fields.
- Validating coordinate fields.
- Comparing original locality values against spatially assigned localities.
- Identifying records outside official locality polygons.
- Preserving traceability between original and processed fields.

## Database Structure

Main schemas used in PostgreSQL/PostGIS:

```text
raw
clean
geo
analysis
```

Main PostGIS tables:

```text
clean.siniestros_bogota
geo.localidades_bogota
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

## Pipeline Automation

The main processing workflow can be executed with:

```powershell
python src\run_pipeline.py
```

This command runs the main pipeline steps:

1. Build the clean geospatial dataset.
2. Load clean data into PostgreSQL/PostGIS.
3. Create or recreate SQL analysis views.

## Portfolio Value

This project demonstrates practical skills in:

- Geospatial data engineering.
- Spatial databases.
- PostgreSQL/PostGIS.
- SQL spatial analysis.
- Python data processing.
- GeoPandas workflows.
- Spatial data quality validation.
- QGIS cartographic visualization.
- Reproducible project documentation.

## Status

The main geospatial pipeline, PostGIS analysis views and QGIS map outputs were completed successfully.