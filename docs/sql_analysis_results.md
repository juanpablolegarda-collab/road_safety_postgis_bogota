# SQL and PostGIS Analysis Results

## Project

Road Safety Geospatial Pipeline - Bogotá

## Analysis Stage

This document summarizes the main SQL and PostGIS analysis results generated from the cleaned road traffic incident dataset.

## Database Tables

Main tables used:

- `clean.siniestros_bogota`
- `geo.localidades_bogota`

Main analysis schema:

- `analysis`

## Main Views Created

- `analysis.v_siniestros_por_localidad`
- `analysis.v_siniestros_por_gravedad`
- `analysis.v_siniestros_por_clase`
- `analysis.v_siniestros_por_anio`
- `analysis.v_siniestros_por_mes`
- `analysis.v_siniestros_por_hora`
- `analysis.v_localidades_con_siniestros`
- `analysis.v_siniestros_fuera_localidad`
- `analysis.v_indicadores_riesgo_localidad`
- `analysis.v_gravedad_por_hora`
- `analysis.v_clase_accidente_por_localidad`

## Main Findings

### Total incidents by locality

The localities with the highest absolute number of road traffic incidents are:

1. Kennedy
2. Engativá
3. Suba
4. Usaquén
5. Fontibón

This result represents absolute counts and should not be interpreted directly as risk without considering area, population, road length or traffic flow.

### Incident severity distribution

The severity distribution is:

- Solo daños: 128,207 incidents
- Con heridos: 67,700 incidents
- Con muertos: 3,239 incidents

Most incidents are classified as material-damage-only events, but a significant proportion involves injuries.

### Spatial validation

A total of 57 incidents fall outside official locality polygons.

These records were preserved and marked instead of being deleted automatically, following a traceability-oriented data quality approach.

### Incident density by area

When normalizing by area, the ranking changes. Localities such as Los Mártires, Barrios Unidos, Puente Aranda, Antonio Nariño and Teusaquillo show high incident density per km².

This demonstrates the importance of comparing both absolute counts and spatial density.

### Severity by locality

The exploratory severity index shows higher average severity in localities such as Usme, San Cristóbal, Rafael Uribe Uribe, Ciudad Bolívar and Bosa.

This index is exploratory and is based on assigned weights for severity categories. It is not an official road safety risk index.

### Incidents by hour

The highest number of incidents occurs during daytime and high-activity hours, especially around midday and afternoon periods.

This temporal pattern should be interpreted carefully because traffic volume data is not included in the current dataset.

## Methodological Notes

- Absolute counts show concentration of records.
- Density per km² helps compare localities of different sizes.
- Severity indicators help identify where incidents tend to have more serious outcomes.
- Spatial joins were performed using official locality polygons.
- Distance and area calculations use projected coordinates through `ST_Transform`.

## Next Step

The next stage is to connect QGIS to the PostGIS database and create maps from the analysis views.