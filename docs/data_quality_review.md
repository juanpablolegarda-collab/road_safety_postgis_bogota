## Quality Findings - Main Dataset

### Dataset

Histórico Siniestros Bogotá D.C.

### General Structure

- Total records: 199,146
- Total columns: 16
- Complete duplicated rows: 0
- Duplicates by `CODIGO_ACCIDENTE`: 0
- Records with valid latitude and longitude: 199,146
- Records with invalid dates: 0

### Temporal Coverage

- Minimum date: 2015-01-01
- Maximum date: 2021-09-10

The dataset will be analyzed for the period 2015–2021. It should not be presented as a current 2024–2026 road safety diagnosis.

### Main Variables

The dataset contains the required fields for geospatial and temporal analysis:

- `CODIGO_ACCIDENTE`
- `FECHA_OCURRENCIA_ACC`
- `FECHA_HORA_ACC`
- `DIRECCION`
- `GRAVEDAD`
- `CLASE_ACC`
- `LOCALIDAD`
- `LATITUD`
- `LONGITUD`

### Severity Distribution

- Solo daños: 128,207
- Con heridos: 67,700
- Con muertos: 3,239

### Accident Class Distribution

- Choque: 170,802
- Atropello: 20,138
- Caída de ocupante: 4,639
- Volcamiento: 2,729
- Otro: 804
- Incendio: 24
- Autolesión: 10

### Spatial Validation Against Official Locality Polygons

The road incident points were spatially validated against the official Bogotá locality polygons.

- Total records: 199,146
- Records inside official locality polygons: 199,089
- Records outside official locality polygons: 57
- Percentage outside official locality polygons: 0.0286%
- Records with missing original locality: 46
- Records with missing original locality recoverable by spatial join: 1

### Locality Consistency

A refined comparison was performed between the original locality field and the spatially assigned locality, normalizing uppercase text and accents.

- Valid comparisons: 199,088
- Refined matches: 194,504
- Refined mismatches: 4,584
- Refined match percentage: 97.7%

The main discrepancies occur between neighboring localities, such as:

- Usaquén → Suba
- Bosa → Ciudad Bolívar
- Puente Aranda → Kennedy
- San Cristóbal → Rafael Uribe Uribe
- Santa Fe → Candelaria
- Barrios Unidos → Teusaquillo

### Methodological Decision

For spatial analysis, the project will use the locality assigned through spatial intersection with official locality polygons as the main analytical locality.

The original locality field from the source dataset will be preserved as a traceability field.

### Cleaning Rules

The following rules will be applied during data transformation:

1. Normalize column names to lowercase.
2. Convert date fields to valid datetime format.
3. Convert latitude and longitude to numeric values.
4. Create point geometry from longitude and latitude.
5. Assign official locality using spatial join with locality polygons.
6. Preserve the original locality field.
7. Add a boolean field indicating whether each point falls inside an official locality polygon.
8. Mark records outside official locality polygons instead of deleting them automatically.
9. Preserve severity and accident class fields.
10. Export a cleaned GeoPackage or GeoJSON for further loading into PostGIS.