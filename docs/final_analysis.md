# Final Analysis

## Road Safety Geospatial Pipeline - Bogotá

## 1. Project Overview

This project developed a reproducible geospatial data pipeline to analyze road traffic incidents in Bogotá D.C., Colombia, using Python, PostgreSQL/PostGIS, SQL and QGIS.

The analysis focused on road traffic incidents recorded between 2015 and 2021. The main goal was to transform raw open data into clean geospatial information, store it in a spatial database, generate SQL-based indicators and produce cartographic outputs for interpretation.

The project was designed as a geospatial data engineering workflow, not only as a map-making exercise. The main emphasis was placed on data quality, spatial validation, reproducibility and technical documentation.

---

## 2. Problem Statement

Road traffic incidents have a strong spatial component. Their distribution is not random across the city, and different areas may show different patterns depending on road density, urban activity, locality size, mobility dynamics and infrastructure conditions.

However, raw incident datasets usually require cleaning, validation and spatial processing before they can be used for analysis. Coordinates, administrative attributes and spatial boundaries must be checked carefully to avoid misleading conclusions.

This project addresses the following question:

> How can road traffic incident data in Bogotá D.C. be processed, validated, analyzed and visualized using a reproducible geospatial data pipeline?

---

## 3. Study Area

The study area is Bogotá D.C., Colombia.

The analysis uses official locality polygons as the administrative spatial unit. These polygons allow the aggregation of incident points by locality and support spatial validation through point-in-polygon operations.

---

## 4. Period of Analysis

The incident dataset covers the period:

```text
2015-01-01 to 2021-09-10
```

Therefore, the results should be interpreted as an exploratory analysis for the period 2015–2021. They should not be presented as a current diagnosis of road safety conditions in Bogotá for 2024, 2025 or 2026.

---

## 5. Data Sources

The project used two main data sources:

### Road Traffic Incidents

Source:

```text
Datos Abiertos Bogotá / Secretaría Distrital de Movilidad
```

Main variables used:

```text
CODIGO_ACCIDENTE
FECHA_OCURRENCIA_ACC
FECHA_HORA_ACC
DIRECCION
GRAVEDAD
CLASE_ACC
LOCALIDAD
LATITUD
LONGITUD
```

### Locality Boundaries

Source:

```text
IDECA / Secretaría Distrital de Planeación
```

Main variables used:

```text
LocNombre
LocCodigo
geometry
```

---

## 6. Methodology

The project followed a structured geospatial data pipeline:

```text
Raw open data
→ Python data cleaning
→ Geospatial transformation
→ PostgreSQL/PostGIS loading
→ SQL spatial analysis views
→ QGIS cartographic visualization
→ Technical documentation
```

### 6.1 Data Inspection

The raw incident dataset was inspected using Python. The review included:

- Number of records.
- Number of columns.
- Data types.
- Missing values.
- Date validity.
- Coordinate validity.
- Duplicate records.
- Severity distribution.
- Accident class distribution.

The dataset contained:

```text
199,146 incident records
16 original columns
0 duplicated records by CODIGO_ACCIDENTE
0 invalid date values
0 missing latitude or longitude values
```

This confirmed that the dataset was suitable for geospatial analysis.

---

### 6.2 Geospatial Cleaning

Incident points were created using:

```text
LONGITUD
LATITUD
```

The coordinate reference system used was:

```text
EPSG:4686 — MAGNA-SIRGAS
```

The cleaned dataset was exported as:

```text
data/processed/siniestros_bogota_clean.gpkg
data/processed/siniestros_bogota_clean.geojson
data/processed/siniestros_bogota_clean.csv
```

The clean incident table included fields such as:

```text
codigo_accidente
fecha_ocurrencia
fecha_hora
anio
mes
dia
hora
dia_semana
direccion
gravedad
clase_accidente
localidad_original
localidad_espacial
localidad_final
inside_localidad
latitud
longitud
geometry
```

---

### 6.3 Spatial Validation

A spatial validation was performed by intersecting incident points with official locality polygons.

Results:

```text
Total incident records: 199,146
Records inside official locality polygons: 199,089
Records outside official locality polygons: 57
Percentage outside locality polygons: 0.0286%
```

The project also compared the original locality field from the source dataset against the spatially assigned locality.

After text normalization, the locality agreement was:

```text
Valid comparisons: 199,088
Refined matches: 194,504
Refined mismatches: 4,584
Refined match percentage: 97.7%
```

The detected mismatches were mainly between neighboring localities, such as:

```text
Usaquén → Suba
Bosa → Ciudad Bolívar
Puente Aranda → Kennedy
San Cristóbal → Rafael Uribe Uribe
Santa Fe → Candelaria
Barrios Unidos → Teusaquillo
```

### Methodological Decision

For spatial analysis, the project used the locality assigned by spatial intersection as the main analytical locality.

The original locality field was preserved for traceability.

This decision is more defensible because it relies on the actual geometric position of each incident point relative to official locality boundaries.

---

## 7. PostGIS Database Design

The cleaned data was loaded into PostgreSQL/PostGIS using Python.

Main schemas:

```text
raw
clean
geo
analysis
```

Main tables:

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

Spatial indexes were created to improve spatial query performance.

The PostGIS validation confirmed:

```text
clean.siniestros_bogota: 199,146 records
geo.localidades_bogota: 20 records
SRID siniestros: 4686
SRID localidades: 4686
```

---

## 8. Main Results

### 8.1 Total Incidents by Locality

The localities with the highest absolute number of registered road traffic incidents were:

```text
Kennedy
Engativá
Suba
Usaquén
Fontibón
Puente Aranda
Chapinero
Teusaquillo
Barrios Unidos
Bosa
```

Kennedy showed the highest absolute number of incidents, with approximately:

```text
23,961 incidents
```

However, this result should be interpreted carefully. A high number of incidents does not automatically mean that a locality is more dangerous. Absolute counts are influenced by size, road network, population, traffic flow and urban activity.

Correct interpretation:

> Kennedy concentrates the highest absolute number of registered incidents in the dataset.

Incorrect interpretation:

> Kennedy is the most dangerous locality.

---

### 8.2 Severity Distribution

The distribution by severity was:

```text
Solo daños: 128,207 incidents
Con heridos: 67,700 incidents
Con muertos: 3,239 incidents
```

Percentages:

```text
Solo daños: 64.38%
Con heridos: 34.00%
Con muertos: 1.63%
```

Most incidents were material-damage-only events. However, a significant proportion involved injured people, which is relevant for road safety analysis.

---

### 8.3 Incident Density by km²

The density indicator was calculated as:

```text
total_siniestros / area_km2
```

This indicator changes the interpretation compared with absolute counts.

Localities with high incident density included:

```text
Los Mártires
Barrios Unidos
Puente Aranda
Antonio Nariño
Teusaquillo
Kennedy
Engativá
Tunjuelito
Fontibón
Candelaria
```

This result is important because it shows that the ranking changes when incidents are normalized by area.

For example:

```text
Kennedy has the highest absolute number of incidents.
Los Mártires has one of the highest incident densities per km².
```

This distinction is methodologically important because density allows a better comparison between localities of different sizes.

---

### 8.4 Exploratory Severity Index

An exploratory severity index was created using weighted severity categories:

```text
Solo daños → lower weight
Con heridos → medium weight
Con muertos → higher weight
```

The localities with higher average severity included:

```text
Usme
San Cristóbal
Rafael Uribe Uribe
Ciudad Bolívar
Bosa
Tunjuelito
Antonio Nariño
Kennedy
Santa Fe
Los Mártires
```

This result suggests that some localities may not have the highest number of incidents but may show relatively more severe outcomes.

Important limitation:

```text
The severity index is exploratory and does not represent an official road safety risk metric.
```

It should be used as an analytical indicator, not as a formal public policy index.

---

### 8.5 Incidents by Hour

The highest number of incidents occurred during daytime and high-activity hours, especially around:

```text
14:00
13:00
12:00
15:00
07:00
11:00
16:00
17:00
08:00
10:00
```

This suggests concentration during working hours, commuting periods and high urban activity times.

However, causality cannot be inferred from this dataset alone. To explain why these hours concentrate more incidents, additional variables would be required, such as:

- Traffic volume.
- Road hierarchy.
- Speed limits.
- Weather.
- Public transport flow.
- Road infrastructure.
- Pedestrian activity.

---

### 8.6 Records Outside Locality Polygons

A total of:

```text
57 incident points
```

were identified outside official locality polygons.

These records were not deleted automatically. Instead, they were preserved and flagged.

This decision follows a traceability-oriented data quality approach. Deleting records without review could hide potential coordinate issues or boundary inconsistencies.

---

## 9. Map Outputs

The project generated five QGIS maps.

### Map 1 — Spatial Distribution of Road Traffic Incidents

Purpose:

```text
Shows the general spatial distribution of incident points in Bogotá D.C.
```

Interpretation:

This map is useful for visualizing where incident points are concentrated. It should not be interpreted as a risk map because it does not normalize by area, population or traffic exposure.

---

### Map 2 — Total Incidents by Locality

Purpose:

```text
Shows the absolute number of incidents by locality.
```

Interpretation:

This map identifies localities with the highest number of registered incidents. It represents absolute counts, not normalized risk.

---

### Map 3 — Incident Density by km²

Purpose:

```text
Shows incident concentration per square kilometer.
```

Interpretation:

This map allows a better comparison between localities of different sizes. It is more analytically robust than absolute counts when comparing spatial concentration.

---

### Map 4 — Average Severity by Locality

Purpose:

```text
Shows an exploratory severity index by locality.
```

Interpretation:

This map highlights localities where incidents tend to have more severe outcomes. The index is exploratory and should not be interpreted as an official risk indicator.

---

### Map 5 — Incidents Outside Official Locality Polygons

Purpose:

```text
Shows spatial data quality issues.
```

Interpretation:

This map identifies incident points located outside official locality polygons. It supports the data quality validation process.

---

## 10. Limitations

This project has several limitations that must be considered.

### 10.1 No Exposure Variable

The analysis does not include traffic exposure variables such as:

```text
vehicle flow
population
pedestrian flow
road length
public transport volume
vehicle kilometers traveled
```

Without exposure data, the project cannot calculate true accident risk rates.

### 10.2 Dataset Period

The incident dataset ends in 2021. Therefore, the results do not represent current road safety conditions.

### 10.3 Exploratory Severity Index

The severity index is based on assigned weights. It is useful for exploratory comparison but is not an official methodology.

### 10.4 Aggregation by Locality

Locality-level aggregation can hide intra-locality variation. Some critical corridors or intersections may be masked when data is summarized by large administrative polygons.

### 10.5 Coordinate Accuracy

Although most points fall inside official locality polygons, some coordinates may still have positional uncertainty or be affected by geocoding/capture errors.

---

## 11. Conclusions

This project successfully developed a reproducible geospatial data pipeline for road traffic incident analysis in Bogotá D.C.

The workflow demonstrated how raw open data can be transformed into structured geospatial information using Python, PostgreSQL/PostGIS and QGIS.

Main conclusions:

1. The dataset is technically suitable for geospatial analysis due to its complete coordinate fields, valid dates and large number of records.
2. Spatial validation is necessary because original locality values do not always match the locality assigned by geometry.
3. Absolute incident counts and density indicators produce different spatial interpretations.
4. Kennedy has the highest absolute number of incidents, but compact central localities such as Los Mártires and Barrios Unidos show high incident density per km².
5. Some southern localities show higher exploratory severity values.
6. A small number of records were identified outside official locality polygons and were preserved for traceability.
7. PostGIS allowed the creation of reusable spatial analysis views.
8. QGIS allowed the visualization of SQL-derived indicators through professional map outputs.
9. The pipeline structure makes the project reproducible and suitable for portfolio use.

---

## 12. Future Work

Future improvements could include:

### 12.1 Road Network Analysis

Integrate Bogotá's road network to analyze:

```text
incidents by road segment
critical corridors
proximity to intersections
road hierarchy
```

### 12.2 Hotspot Analysis

Apply spatial clustering methods such as:

```text
DBSCAN
HDBSCAN
Kernel Density Estimation
Getis-Ord Gi*
```

This would help identify statistically significant clusters or critical zones.

### 12.3 Machine Learning Extension

A future version could include machine learning to:

```text
classify incident severity
identify high-risk spatial patterns
predict incident concentration
cluster critical areas
```

However, this should be done carefully because the severity classes are imbalanced.

### 12.4 Exposure-Based Risk Indicators

Add external datasets such as:

```text
population
road length
traffic volume
public transport flow
vehicle fleet
```

This would allow the calculation of more defensible risk rates.

### 12.5 Dashboard Development

Create an interactive dashboard using:

```text
Power BI
Streamlit
Dash
Kepler.gl
Leaflet
```

This would improve communication of results to non-technical audiences.

---

## 13. Portfolio Interpretation

This project demonstrates practical junior-level skills in:

```text
Python scripting
GeoPandas workflows
PostgreSQL/PostGIS
SQL spatial analysis
spatial joins
CRS handling
data quality validation
QGIS cartography
technical documentation
Git/GitHub workflow
reproducible geospatial pipelines
```

The strongest value of the project is not only the final maps, but the complete technical workflow from raw data to cleaned geospatial database, SQL indicators and documented cartographic outputs.

---

## 14. Final Statement

The project provides a complete and reproducible geospatial data engineering workflow for exploratory road safety analysis in Bogotá D.C.

It shows how open data can be transformed into spatial indicators and cartographic products using a professional stack based on Python, PostgreSQL/PostGIS and QGIS.