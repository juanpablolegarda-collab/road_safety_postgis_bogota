# Map Outputs

## Project

Road Safety Geospatial Pipeline - Bogotá

## Purpose

This document summarizes the cartographic outputs generated in QGIS from PostgreSQL/PostGIS analysis views.

The maps were created to communicate spatial patterns, absolute counts, density indicators, exploratory severity indicators and spatial data quality checks for road traffic incidents in Bogotá D.C. between 2015 and 2021.

## Maps

### Map 1 — Spatial distribution of road traffic incidents

File:

maps/mapa_01_distribucion_siniestros.png

Purpose:

Shows the spatial distribution of georeferenced road traffic incidents in Bogotá D.C. between 2015 and 2021.

Main layer:

clean.siniestros_bogota

Interpretation:

This map shows the general concentration of incident points across Bogotá D.C. It should not be interpreted as a risk map because it does not normalize by area, population, traffic flow or road length.

---

### Map 2 — Total incidents by locality

File:

maps/mapa_02_total_siniestros_localidad.png

Purpose:

Shows the absolute number of road traffic incidents by locality.

Main layer:

analysis.v_indicadores_riesgo_localidad

Main field:

total_siniestros

Interpretation:

This map identifies localities with the highest number of registered incidents. It represents absolute counts, not normalized risk. A locality with more incidents is not necessarily more dangerous without considering area, population, road length or traffic exposure.

---

### Map 3 — Incident density by km²

File:

maps/mapa_03_densidad_siniestros_km2.png

Purpose:

Shows the density of road traffic incidents per square kilometer by locality.

Main layer:

analysis.v_indicadores_riesgo_localidad

Main field:

siniestros_por_km2

Interpretation:

This map allows comparison between localities of different sizes by normalizing incident counts by area. It helps identify localities where incidents are more spatially concentrated.

---

### Map 4 — Average severity by locality

File:

maps/mapa_04_severidad_promedio_localidad.png

Purpose:

Shows an exploratory average severity index by locality.

Main layer:

analysis.v_indicadores_riesgo_localidad

Main field:

indice_severidad_promedio

Interpretation:

This map highlights localities where incidents tend to have more severe outcomes. The index is exploratory and is based on assigned weights for severity categories. It does not represent an official road safety risk metric.

---

### Map 5 — Incidents outside official locality polygons

File:

maps/mapa_05_puntos_fuera_localidad.png

Purpose:

Shows road traffic incident points located outside official locality polygons.

Main layer:

analysis.v_siniestros_fuera_localidad

Interpretation:

This is a spatial data quality control map. It identifies records that require attention due to their position outside official administrative boundaries. These records were preserved and flagged instead of being automatically deleted.

## Main Data Sources

- Road traffic incidents: Datos Abiertos Bogotá – Secretaría Distrital de Movilidad.
- Locality boundaries: IDECA / Secretaría Distrital de Planeación.
- Processing: Python, GeoPandas, PostgreSQL/PostGIS and QGIS.

## Tools Used

- QGIS
- PostgreSQL/PostGIS
- Python
- GeoPandas
- SQL

## Methodological Notes

- Spatial joins were performed using official locality polygons.
- The main analytical locality was assigned spatially using PostGIS.
- The original locality field was preserved for traceability.
- Area-based indicators were calculated using projected geometries with ST_Transform.
- Absolute counts and normalized density indicators were interpreted separately.
- The severity index is exploratory and should not be presented as an official road safety indicator.

## Status

Main cartographic outputs generated successfully.