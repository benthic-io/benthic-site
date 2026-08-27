---
title: "Congressional District Maps"
---

### https://benthic.io/ngopen/up_cdmaps/ – Congressional district maps/boundaries

The core theme of this database, created using UCLA Polysci's excellent [congressional district dataset](https://cdmaps.polisci.ucla.edu/), is boundaries of congressional districts historic and current.

## Tables

### congressional_districts

Historical and current U.S. congressional district boundaries with geometry. One row per district definition from Congressional redistricting data.

| Column            | Type                         | Description                                           |
| ----------------- | ---------------------------- | ----------------------------------------------------- |
| `id`              | integer                      | Primary key                                           |
| `congress_number` | integer                      | Congress number (e.g. 118 = 118th Congress)           |
| `statename`       | varchar                      | State name                                            |
| `district`        | integer                      | District number (0 for at-large)                      |
| `startcong`       | numeric                      | Starting Congress number for this district definition |
| `endcong`         | numeric                      | Ending Congress number for this district definition   |
| `district_id`     | varchar                      | District identifier                                   |
| `districtsi`      | varchar                      | District significance code                            |
| `county`          | varchar                      | County name                                           |
| `page`            | varchar                      | Source page reference                                 |
| `law`             | varchar                      | Public law reference                                  |
| `note`            | varchar                      | Notes                                                 |
| `bestdec`         | varchar                      | Best decision indicator                               |
| `finalnote`       | varchar                      | Final note                                            |
| `rnote`           | varchar                      | Redistricting note                                    |
| `lastchange`      | date                         | Date of last change                                   |
| `fromcounty`      | varchar                      | Source county                                         |
| `statefp`         | varchar                      | State FIPS code                                       |
| `geom`            | geometry(MultiPolygon, 3857) | District boundary geometry (Web Mercator)             |
| `source_file`     | varchar                      | Source filename                                       |
| `imported_at`     | timestamp                    | When this row was imported                            |

#### Example queries

```bash
# Get all districts for a state in the current Congress
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?statename=eq.California&congress_number=eq.118&select=id,statename,district,congress_number"

# Get all at-large districts
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?district=eq.0&congress_number=eq.118&select=statename,district"

# Get all districts for a specific Congress number
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?congress_number=eq.118&select=id,statename,district&order=statename,district&limit=500"

# List available Congress numbers
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?select=congress_number&groupby=congress_number&order=congress_number"

# Get a specific state + district
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?statename=eq.Texas&district=eq.7&congress_number=eq.118"

# Count districts per state for a Congress
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?select=statename,count&congress_number=eq.118&groupby=statename"
```

## PostGIS Spatial Queries

The `geom` column is a PostGIS MultiPolygon stored in SRID 3857 (Web Mercator). Two purpose-built RPC functions handle the most common spatial lookups; both accept and return standard GeoJSON-friendly values.

### rpc_find_district

Point-in-polygon lookup: which district contains this coordinate?

```bash
curl -X POST "https://benthic.io/ngopen/up_cdmaps/rpc/rpc_find_district" \
  -H "Content-Type: application/json" \
  -d '{"lat": 38.9072, "lon": -77.0369, "congress": 118}'
```

### rpc_districts_in_bbox

All districts intersecting a bounding box:

```bash
curl -X POST "https://benthic.io/ngopen/up_cdmaps/rpc/rpc_districts_in_bbox" \
  -H "Content-Type: application/json" \
  -d '{"min_lat": 32.0, "max_lat": 36.0, "min_lon": -120.0, "max_lon": -114.0, "congress": 118}'
```

### Working with geometries directly

You can request raw geometry as GeoJSON (`select=id,statename,district,geom`) and run any further geometric analysis client-side (e.g. with Shapely, Turf.js, or QGIS). If you join `geom` polygons against geocoded point columns from other NGOpen datasets, remember those points are EPSG:4326 while these polygons are EPSG:3857 — reproject before comparing (`ST_Transform` server-side, or an equivalent in your GIS library).

## PostgREST Query Reference

### Filtering

| Operator     | Syntax                | Example                                       |
| ------------ | --------------------- | --------------------------------------------- |
| Equals       | `?col=value`          | `?statename=eq.California`                    |
| Not equal    | `?col=neq.value`      | `?district=neq.0`                             |
| Greater than | `?col=gt.value`       | `?congress_number=gt.110`                     |
| Less than    | `?col=lt.value`       | `?congress_number=lt.118`                     |
| Greater/eq   | `?col=gte.value`      | `?congress_number=gte.118`                    |
| Less/eq      | `?col=lte.value`      | `?congress_number=lte.118`                    |
| ILIKE        | `?col=ilike.PATTERN`  | `?statename=ilike.%25new%25`                  |
| IS null      | `?col=is.null`        | `?endcong=is.null`                            |
| IS NOT null  | `?col=not.is.null`    | `?lastchange=not.is.null`                     |
| IN           | `?col=in.(val1,val2)` | `?statename=in.(California,Texas,New%20York)` |

### Selecting columns

```
?select=id,statename,district,congress_number,statefp
```

### Ordering

```
?order=congress_number.desc,statename.asc,district.asc
```

### Pagination

```
?limit=100&offset=200
```

### Counting

```
Prefer: count=exact
```

## Key Relationships

This is a single-table database. Cross-reference to other benthic.io datasets:

- **USAspending** — match `statefp` + `district` to `ref_population_cong_district` for population data; use `financial_accounts_by_awards` to find spending in a district
- **USP CL** — `legislator_terms` contains `state` and `district` columns that match this table
- **IRS NG** — geocoded nonprofit locations can be spatial-joined to districts via `geom`

## Spatial RPC Functions

### rpc_find_district

Find the congressional district for a lat/lon point. Returns the district that contains the given coordinate.

| Parameter  | Type             | Description                    |
| ---------- | ---------------- | ------------------------------ |
| `lat`      | double precision | Latitude                       |
| `lon`      | double precision | Longitude                      |
| `congress` | integer          | Congress number (default: 118) |

#### Example queries

```bash
# Find district for Washington DC coordinates
curl -X POST "https://benthic.io/ngopen/up_cdmaps/rpc/rpc_find_district" \
  -H "Content-Type: application/json" \
  -d '{"lat": 38.9072, "lon": -77.0369}'

# Find district for a specific congress
curl -X POST "https://benthic.io/ngopen/up_cdmaps/rpc/rpc_find_district" \
  -H "Content-Type: application/json" \
  -d '{"lat": 34.0522, "lon": -118.2437, "congress": 117}'
```

### rpc_districts_in_bbox

Find all districts intersecting a bounding box. Useful for map viewport queries.

| Parameter  | Type             | Description                    |
| ---------- | ---------------- | ------------------------------ |
| `min_lat`  | double precision | Minimum latitude               |
| `max_lat`  | double precision | Maximum latitude               |
| `min_lon`  | double precision | Minimum longitude              |
| `max_lon`  | double precision | Maximum longitude              |
| `congress` | integer          | Congress number (default: 118) |

#### Example queries

```bash
# Get districts in a viewport bounding box
curl -X POST "https://benthic.io/ngopen/up_cdmaps/rpc/rpc_districts_in_bbox" \
  -H "Content-Type: application/json" \
  -d '{"min_lat": 32.0, "max_lat": 36.0, "min_lon": -120.0, "max_lon": -114.0}'
```

