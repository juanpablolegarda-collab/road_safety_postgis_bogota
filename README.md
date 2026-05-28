# Road Safety Geospatial Pipeline - Bogotá

This project develops a reproducible geospatial data pipeline to analyze road traffic incidents in Bogotá D.C., Colombia, using Python, PostgreSQL/PostGIS and QGIS.

The project focuses on data cleaning, spatial validation, PostGIS loading, SQL spatial analysis and cartographic visualization.

## Study Area

Bogotá D.C., Colombia.

## Period of Analysis

2015–2021.

## Objective

To process, clean, store, analyze and visualize georeferenced road traffic incident data using geospatial data engineering tools.

## Workflow

```text
Raw open data
→ Python data cleaning
→ Geospatial transformation
→ PostgreSQL/PostGIS loading
→ SQL spatial analysis views
→ QGIS cartographic visualization
→ Technical documentation
```

## Tools and Technologies

- Python
- Pandas
- GeoPandas
- PostgreSQL
- PostGIS
- SQL
- QGIS
- Git/GitHub

## Data Sources

- Road traffic incidents: Datos Abiertos Bogotá / Secretaría Distrital de Movilidad.
- Locality boundaries: IDECA / Secretaría Distrital de Planeación.

## Project Structure

```text
road_safety_postgis_bogota/
│
├── data/
│   ├── raw/              # Ignored in Git
│   ├── external/         # Ignored in Git
│   └── processed/        # Ignored in Git
│
├── docs/                 # Technical documentation
├── maps/                 # Exported map outputs
├── notebooks/            # Optional exploratory notebooks
├── qgis/                 # QGIS project file
├── sql/                  # SQL and PostGIS analysis scripts
├── src/                  # Python pipeline scripts
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Main Pipeline

The main processing workflow can be executed with:

```powershell
python src\run_pipeline.py
```

This command runs:

1. Clean dataset generation.
2. PostGIS data loading.
3. SQL analysis view creation.

## Main Python Scripts

```text
src/build_clean_dataset.py
src/load_to_postgis.py
src/run_sql_views.py
src/run_pipeline.py
```

## Main SQL Files

```text
sql/04_spatial_analysis.sql
sql/05_risk_indicators.sql
```

## Database Structure

Main PostgreSQL/PostGIS schemas:

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

## Map Outputs

The project generated five QGIS map outputs:

1. Spatial distribution of road traffic incidents.
2. Total incidents by locality.
3. Incident density by km².
4. Average severity by locality.
5. Incidents outside official locality polygons.

Map files are stored in:

```text
maps/
```

## Main Results

- Kennedy, Engativá, Suba, Usaquén and Fontibón show the highest absolute number of registered road traffic incidents.
- Localities such as Los Mártires, Barrios Unidos, Puente Aranda, Antonio Nariño and Teusaquillo show high incident density per square kilometer.
- The exploratory severity index highlights localities such as Usme, San Cristóbal, Rafael Uribe Uribe, Ciudad Bolívar and Bosa.
- A total of 57 incident points were identified outside official locality polygons.
- Absolute counts, density indicators and severity indicators were interpreted separately.

## Methodological Notes

- Incident points were created from latitude and longitude.
- Official locality polygons were used for spatial validation.
- The analytical locality was assigned spatially using official locality boundaries.
- Original locality values were preserved for traceability.
- Records outside official locality polygons were preserved and flagged.
- Area-based indicators were calculated using projected geometries.
- The severity index is exploratory and is not an official road safety risk metric.

## Data Quality

The project includes data quality validation steps:

- Missing value review.
- Duplicate record review.
- Date validation.
- Coordinate validation.
- CRS validation.
- Spatial validation against locality polygons.
- Locality consistency comparison.
- Identification of records outside official locality polygons.

## Important Notes

The raw and processed datasets are not included in the repository because they are excluded through `.gitignore`.

Ignored folders include:

```text
data/raw/
data/external/
data/processed/
venv/
.env
```

To reproduce the project, the user must download the source datasets and configure the local database connection in a `.env` file.

## Environment Variables

The project requires a local `.env` file with the following structure:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=road_safety_bogota
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file must not be uploaded to GitHub.

## Documentation

Additional documentation is available in:

```text
docs/environment_setup.md
docs/data_sources.md
docs/data_quality_review.md
docs/sql_analysis_results.md
docs/map_outputs.md
docs/pipeline_execution.md
docs/project_summary.md
```

## Portfolio Value

This project demonstrates practical skills in:

- Geospatial data engineering.
- PostgreSQL/PostGIS.
- SQL spatial analysis.
- Python data processing.
- GeoPandas workflows.
- Spatial data quality validation.
- QGIS cartographic visualization.
- Reproducible technical documentation.

## Status

Main geospatial pipeline, PostGIS analysis views and QGIS map outputs completed successfully.