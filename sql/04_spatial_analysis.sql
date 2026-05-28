-- ============================================================
-- Road Safety Geospatial Pipeline - Bogotá
-- Spatial SQL Analysis
-- Database: road_safety_bogota
-- ============================================================

-- 1. Validate loaded tables

SELECT COUNT(*) AS total_siniestros
FROM clean.siniestros_bogota;

SELECT COUNT(*) AS total_localidades
FROM geo.localidades_bogota;


-- 2. Validate geometry types and SRID

SELECT 
    GeometryType(geometry) AS geometry_type,
    ST_SRID(geometry) AS srid,
    COUNT(*) AS total
FROM clean.siniestros_bogota
GROUP BY GeometryType(geometry), ST_SRID(geometry);

SELECT 
    GeometryType(geometry) AS geometry_type,
    ST_SRID(geometry) AS srid,
    COUNT(*) AS total
FROM geo.localidades_bogota
GROUP BY GeometryType(geometry), ST_SRID(geometry);


-- 3. Incidents by final locality

DROP VIEW IF EXISTS analysis.v_siniestros_por_localidad;

CREATE VIEW analysis.v_siniestros_por_localidad AS
SELECT
    localidad_final,
    COUNT(*) AS total_siniestros,
    SUM(CASE WHEN gravedad = 'SOLO DANOS' THEN 1 ELSE 0 END) AS solo_danos,
    SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS con_heridos,
    SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS con_muertos
FROM clean.siniestros_bogota
GROUP BY localidad_final
ORDER BY total_siniestros DESC;


-- 4. Incidents by severity

DROP VIEW IF EXISTS analysis.v_siniestros_por_gravedad;

CREATE VIEW analysis.v_siniestros_por_gravedad AS
SELECT
    gravedad,
    COUNT(*) AS total_siniestros,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM clean.siniestros_bogota
GROUP BY gravedad
ORDER BY total_siniestros DESC;


-- 5. Incidents by accident class

DROP VIEW IF EXISTS analysis.v_siniestros_por_clase;

CREATE VIEW analysis.v_siniestros_por_clase AS
SELECT
    clase_accidente,
    COUNT(*) AS total_siniestros,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM clean.siniestros_bogota
GROUP BY clase_accidente
ORDER BY total_siniestros DESC;


-- 6. Incidents by year

DROP VIEW IF EXISTS analysis.v_siniestros_por_anio;

CREATE VIEW analysis.v_siniestros_por_anio AS
SELECT
    anio,
    COUNT(*) AS total_siniestros,
    SUM(CASE WHEN gravedad = 'SOLO DANOS' THEN 1 ELSE 0 END) AS solo_danos,
    SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS con_heridos,
    SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS con_muertos
FROM clean.siniestros_bogota
GROUP BY anio
ORDER BY anio;


-- 7. Incidents by month

DROP VIEW IF EXISTS analysis.v_siniestros_por_mes;

CREATE VIEW analysis.v_siniestros_por_mes AS
SELECT
    anio,
    mes,
    COUNT(*) AS total_siniestros
FROM clean.siniestros_bogota
GROUP BY anio, mes
ORDER BY anio, mes;


-- 8. Incidents by day of week

DROP VIEW IF EXISTS analysis.v_siniestros_por_dia_semana;

CREATE VIEW analysis.v_siniestros_por_dia_semana AS
SELECT
    dia_semana,
    COUNT(*) AS total_siniestros,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS porcentaje
FROM clean.siniestros_bogota
GROUP BY dia_semana
ORDER BY total_siniestros DESC;


-- 9. Incidents by hour

DROP VIEW IF EXISTS analysis.v_siniestros_por_hora;

CREATE VIEW analysis.v_siniestros_por_hora AS
SELECT
    hora,
    COUNT(*) AS total_siniestros
FROM clean.siniestros_bogota
GROUP BY hora
ORDER BY hora;


-- 10. Locality polygons with incident counts
-- This view is useful for QGIS choropleth maps.

DROP VIEW IF EXISTS analysis.v_localidades_con_siniestros;

CREATE VIEW analysis.v_localidades_con_siniestros AS
SELECT
    l.localidad_nombre,
    l.localidad_codigo,
    COUNT(s.codigo_accidente) AS total_siniestros,
    SUM(CASE WHEN s.gravedad = 'SOLO DANOS' THEN 1 ELSE 0 END) AS solo_danos,
    SUM(CASE WHEN s.gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS con_heridos,
    SUM(CASE WHEN s.gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS con_muertos,
    l.geometry
FROM geo.localidades_bogota l
LEFT JOIN clean.siniestros_bogota s
    ON ST_Within(s.geometry, l.geometry)
GROUP BY
    l.localidad_nombre,
    l.localidad_codigo,
    l.geometry
ORDER BY total_siniestros DESC;


-- 11. Spatial validation from PostGIS

DROP VIEW IF EXISTS analysis.v_siniestros_inside_localidad_check;

CREATE VIEW analysis.v_siniestros_inside_localidad_check AS
SELECT
    s.codigo_accidente,
    s.localidad_original,
    s.localidad_espacial,
    s.localidad_final,
    l.localidad_nombre AS localidad_postgis,
    s.inside_localidad,
    ST_Within(s.geometry, l.geometry) AS within_localidad,
    s.geometry
FROM clean.siniestros_bogota s
LEFT JOIN geo.localidades_bogota l
    ON ST_Within(s.geometry, l.geometry);


-- 12. Records outside official locality polygons

DROP VIEW IF EXISTS analysis.v_siniestros_fuera_localidad;

CREATE VIEW analysis.v_siniestros_fuera_localidad AS
SELECT
    codigo_accidente,
    fecha_ocurrencia,
    fecha_hora,
    gravedad,
    clase_accidente,
    localidad_original,
    localidad_espacial,
    localidad_final,
    latitud,
    longitud,
    geometry
FROM clean.siniestros_bogota
WHERE inside_localidad = false;