-- ============================================================
-- Road Safety Geospatial Pipeline - Bogotá
-- Risk Indicators by Locality
-- Database: road_safety_bogota
-- ============================================================

-- ============================================================
-- 1. Risk indicators by locality
-- ============================================================

DROP VIEW IF EXISTS analysis.v_indicadores_riesgo_localidad;

CREATE VIEW analysis.v_indicadores_riesgo_localidad AS
WITH base AS (
    SELECT
        l.localidad_nombre,
        l.localidad_codigo,
        ROUND((ST_Area(ST_Transform(l.geometry, 3116)) / 1000000.0)::numeric, 2) AS area_km2,

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
)

SELECT
    localidad_nombre,
    localidad_codigo,
    area_km2,
    total_siniestros,
    solo_danos,
    con_heridos,
    con_muertos,

    ROUND((total_siniestros::numeric / NULLIF(area_km2, 0)), 2) AS siniestros_por_km2,

    ROUND((solo_danos::numeric * 100 / NULLIF(total_siniestros, 0)), 2) AS porcentaje_solo_danos,
    ROUND((con_heridos::numeric * 100 / NULLIF(total_siniestros, 0)), 2) AS porcentaje_con_heridos,
    ROUND((con_muertos::numeric * 100 / NULLIF(total_siniestros, 0)), 2) AS porcentaje_con_muertos,

    ROUND(
        (
            (solo_danos * 1) +
            (con_heridos * 3) +
            (con_muertos * 10)
        )::numeric / NULLIF(total_siniestros, 0),
        2
    ) AS indice_severidad_promedio,

    geometry
FROM base;


-- ============================================================
-- 2. Yearly incidents by locality
-- ============================================================

DROP VIEW IF EXISTS analysis.v_siniestros_localidad_anio;

CREATE VIEW analysis.v_siniestros_localidad_anio AS
SELECT
    localidad_final,
    anio,
    COUNT(*) AS total_siniestros,
    SUM(CASE WHEN gravedad = 'SOLO DANOS' THEN 1 ELSE 0 END) AS solo_danos,
    SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS con_heridos,
    SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS con_muertos
FROM clean.siniestros_bogota
GROUP BY localidad_final, anio
ORDER BY localidad_final, anio;


-- ============================================================
-- 3. Severity by hour
-- ============================================================

DROP VIEW IF EXISTS analysis.v_gravedad_por_hora;

CREATE VIEW analysis.v_gravedad_por_hora AS
SELECT
    hora,
    COUNT(*) AS total_siniestros,
    SUM(CASE WHEN gravedad = 'SOLO DANOS' THEN 1 ELSE 0 END) AS solo_danos,
    SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END) AS con_heridos,
    SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END) AS con_muertos,
    ROUND(SUM(CASE WHEN gravedad = 'CON HERIDOS' THEN 1 ELSE 0 END)::numeric * 100 / COUNT(*), 2) AS porcentaje_heridos,
    ROUND(SUM(CASE WHEN gravedad = 'CON MUERTOS' THEN 1 ELSE 0 END)::numeric * 100 / COUNT(*), 2) AS porcentaje_muertos
FROM clean.siniestros_bogota
GROUP BY hora
ORDER BY hora;


-- ============================================================
-- 4. Accident class by locality
-- ============================================================

DROP VIEW IF EXISTS analysis.v_clase_accidente_por_localidad;

CREATE VIEW analysis.v_clase_accidente_por_localidad AS
SELECT
    localidad_final,
    clase_accidente,
    COUNT(*) AS total_siniestros,
    ROUND(
        COUNT(*)::numeric * 100 / SUM(COUNT(*)) OVER (PARTITION BY localidad_final),
        2
    ) AS porcentaje_en_localidad
FROM clean.siniestros_bogota
GROUP BY localidad_final, clase_accidente
ORDER BY localidad_final, total_siniestros DESC;