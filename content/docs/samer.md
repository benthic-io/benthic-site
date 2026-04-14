---
title: "Docs"
---
### https://benthic.io/ngopen/samer/ – SAM.gov entity registrations (federal contractors/vendors)

The core theme of this database is federal contractors and vendors and it provides:
- Entity & registration: UEI, DUNS (legacy), entity_id, legal_business_name, dba_name, primary_naics (and full list), psc_codes, purpose_of_registration, registration_expiration, last_update, business_start_date, corporate_url, is_current.
- Addresses & geocoding: Physical + mailing (line1, city, state, zip, country) + latitude/longitude, geocode_date.
- Examples: “Active vendors by NAICS in a state with expiration dates”; “Geocoded contractors near specific coordinates”; match to spending via UEI.


## Tables

### sam_registrations

Entity registrations from the System for Award Management (SAM.gov). One row per entity registration. Geocoded via Photon API using structured search with US country-code bias for accuracy.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `uei` | varchar(50) | Unique Entity Identifier |
| `entity_id` | varchar(50) | SAM.gov entity ID |
| `duns` | varchar(20) | DUNS number (legacy identifier) |
| `legal_business_name` | varchar(255) | Legal business name |
| `dba_name` | varchar(255) | Doing Business As name |
| `physical_address_line1` | text | Physical street address |
| `physical_city` | varchar(100) | Physical address city |
| `physical_state` | varchar(100) | Physical address state |
| `physical_zip` | varchar(20) | Physical address ZIP |
| `physical_country` | varchar(10) | Physical address country code |
| `mailing_address_line1` | text | Mailing street address |
| `mailing_city` | varchar(100) | Mailing address city |
| `mailing_state` | varchar(100) | Mailing address state |
| `mailing_zip` | varchar(50) | Mailing address ZIP |
| `mailing_country` | varchar(10) | Mailing address country code |
| `primary_naics` | varchar(10) | Primary NAICS code |
| `naics_codes` | text | All NAICS codes (space-separated) |
| `psc_codes` | text | Product/Service Codes (space-separated) |
| `registration_expiration` | varchar(20) | Registration expiration date |
| `last_update` | varchar(20) | Date of last SAM update |
| `business_start_date` | varchar(20) | Business start date |
| `corporate_url` | text | Corporate website URL |
| `purpose_of_registration` | varchar(50) | Purpose of registration |
| `source_file` | varchar(255) | Source filename |
| `imported_at` | timestamp | When this row was imported |
| `is_current` | boolean | TRUE for the latest registration snapshot |
| `latitude` | double precision | Geocoded latitude |
| `longitude` | double precision | Geocoded longitude |
| `geom_point` | geometry(Point, 4326) | PostGIS point geometry (auto-populated from lat/lon) |
| `geocode_date` | timestamp | When geocoding was performed |
| `geocode_system` | varchar(50) | Geocoding system used |

#### Example queries

```bash
# Find a registration by UEI
curl "https://benthic.io/ngopen/samer/sam_registrations?uei=eq.ABCDEFGHIJK&select=legal_business_name,physical_city,physical_state,primary_naics"

# Search by business name (case-insensitive)
curl "https://benthic.io/ngopen/samer/sam_registrations?legal_business_name=ilike.*lockheed*&select=uei,legal_business_name,physical_state,primary_naics&limit=20"

# Filter by primary NAICS code
curl "https://benthic.io/ngopen/samer/sam_registrations?primary_naics=eq.541512&select=uei,legal_business_name,physical_city,physical_state&limit=50"

# Filter by state
curl "https://benthic.io/ngopen/samer/sam_registrations?physical_state=eq.VA&is_current=is.true&limit=25"

# Get geocoded registrations in a bounding box
curl "https://benthic.io/ngopen/samer/sam_registrations?latitude=gte.38.0&latitude=lte.39.0&longitude=gte.-77.0&longitude=lte.-76.0&latitude=not.is.null&select=uei,legal_business_name,latitude,longitude&limit=100"

# PostGIS spatial query: registrations near a point (via RPC)
curl -X POST "https://benthic.io/ngopen/samer/rpc/st_dwithin" \
  -H "Content-Type: application/json" \
  -d '{"geom1": {"type": "Point", "coordinates": [-77.0369, 38.9072]}, "geom2_column": "geom_point", "distance_meters": 5000}'

# Count registrations per state
curl "https://benthic.io/ngopen/samer/sam_registrations?select=physical_state,count&is_current=is.true&groupby=physical_state"

# Find registrations expiring soon
curl "https://benthic.io/ngopen/samer/sam_registrations?registration_expiration=lte.20260630&is_current=is.true&select=uei,legal_business_name,registration_expiration&limit=50"

# Lookup by DUNS
curl "https://benthic.io/ngopen/samer/sam_registrations?duns=eq.123456789&select=uei,legal_business_name,physical_state"
```


## PostgREST Query Reference

### Filtering

| Operator | Syntax | Example |
|---|---|---|
| Equals | `?col=value` | `?physical_state=eq.CA` |
| Not equal | `?col=neq.value` | `?physical_country=neq.US` |
| Greater than | `?col=gt.value` | `?latitude=gt.40.0` |
| Less than | `?col=lt.value` | `?latitude=lt.41.0` |
| Greater/eq | `?col=gte.value` | `?latitude=gte.40.0` |
| Less/eq | `?col=lte.value` | `?latitude=lte.41.0` |
| LIKE | `?col=like.PATTERN` | `?legal_business_name=like.*Inc*` |
| ILIKE | `?col=ilike.PATTERN` | `?legal_business_name=ilike.%25boeing%25` |
| IS null | `?col=is.null` | `?latitude=is.null` |
| IS NOT null | `?col=not.is.null` | `?latitude=not.is.null` |
| IN | `?col=in.(val1,val2)` | `?physical_state=in.(CA,NY,TX)` |

### Selecting columns

```
?select=uei,legal_business_name,physical_state,latitude,longitude
```

### Ordering

```
?order=legal_business_name.asc
?order=registration_expiration.desc
```

### Pagination

```
?limit=100&offset=200
```

Or use range headers:

```
Range: 0-99
```

### Counting

```
# Count with headers only
Prefer: count=exact

# Count as a column
?select=count
```

### Grouping / aggregation

```
?select=primary_naics,count&groupby=primary_naics&order=count.desc&limit=10
```


## Key Relationships

This is a single-table database. Cross-reference to other benthic.io datasets:

- **USAspending** — link via `uei` or `duns` to find federal awards for a SAM-registered entity
- **IRS NG** — link via EIN (`duns` often matches EIN for nonprofits)
- Same geocoding scheme (Photon API) enables spatial cross-referencing across all databases


## Views

### mv_contractor_registry

Active contractor registry with expiration status classification. Filters `sam_registrations` to current records only and adds a computed `registration_status` column (`active`, `expiring_soon`, `expired`).

| Column | Type | Description |
|---|---|---|
| `uei` | varchar(50) | Unique Entity Identifier |
| `entity_id` | varchar(50) | SAM.gov entity ID |
| `duns` | varchar(20) | DUNS number |
| `legal_business_name` | varchar(255) | Legal business name |
| `dba_name` | varchar(255) | DBA name |
| `primary_naics` | varchar(10) | Primary NAICS code |
| `naics_codes` | text | All NAICS codes |
| `psc_codes` | text | Product/Service codes |
| `physical_city` | varchar(100) | City |
| `physical_state` | varchar(100) | State |
| `physical_zip` | varchar(20) | ZIP |
| `physical_country` | varchar(10) | Country |
| `latitude` | double precision | Geocoded latitude |
| `longitude` | double precision | Geocoded longitude |
| `geom_point` | geometry | PostGIS point geometry |
| `registration_expiration` | varchar(20) | Expiration date |
| `last_update` | varchar(20) | Last update date |
| `business_start_date` | varchar(20) | Business start date |
| `corporate_url` | text | Corporate website |
| `purpose_of_registration` | varchar(50) | Registration purpose |
| `registration_status` | text | `active`, `expiring_soon`, or `expired` |

#### Example queries

```bash
# Expired registrations
curl "https://benthic.io/ngopen/samer/mv_contractor_registry?registration_status=eq.expired&select=uei,legal_business_name,registration_expiration&limit=25"

# Expiring soon (within 90 days)
curl "https://benthic.io/ngopen/samer/mv_contractor_registry?registration_status=eq.expiring_soon&select=uei,legal_business_name,registration_expiration,primary_naics&limit=25"

# Active contractors by NAICS
curl "https://benthic.io/ngopen/samer/mv_contractor_registry?registration_status=eq.active&primary_naics=eq.541512&select=uei,legal_business_name,physical_state&limit=50"
```


## Data Pipeline

SAM.gov entity registration data is updated automatically via `sam_pipeline.py`. The pipeline:

1. **Downloads** the latest monthly SAM extract from SAM.gov bulk data service
2. **Imports** new/updated registrations into the `sam_er` PostgreSQL database via `gov_to_pg.py`
3. **Geocodes** new addresses using Photon's structured search endpoint (`/api/structured`) with per-row country-code bias, falling back to free-text search when structured results are unavailable
4. **Fixes** erroneous geocodes by detecting US-addressed entities whose lat/lon fell outside US bounds and re-geocoding them
5. **Refreshes** the `mv_contractor_registry` materialized view

| Field | Value |
|---|---|
| Data source | SAM.gov monthly bulk extract |
| Update frequency | Monthly (automated) |
| Geocoder | Photon (self-hosted, OpenStreetMap data) |
| Geocoding method | Structured search with country-code bias, free-text fallback |
| Script | `sam_pipeline.py` |

```bash
# Run full pipeline
python sam_pipeline.py

# Run specific steps
python sam_pipeline.py --download-only
python sam_pipeline.py --import-only
python sam_pipeline.py --geocode-only
python sam_pipeline.py --fix-only
python sam_pipeline.py --refresh-views
```


## NAICS Code Reference

NAICS (North American Industry Classification System) codes classify business establishments by type of economic activity. Common codes in federal contracting:

| Code | Sector |
|---|---|
| 541511 | Custom Computer Programming Services |
| 541512 | Computer Systems Design Services |
| 541513 | Computer Facilities Management Services |
| 541519 | Other Computer Related Services |
| 541330 | Engineering Services |
| 541715 | Research and Development in the Physical, Engineering, and Life Sciences |
| 236220 | Commercial and Institutional Building Construction |
| 561210 | Facilities Support Services |
| 336411 | Aircraft Manufacturing |
| 334511 | Search, Detection, Navigation, Guidance, Aeronautical Systems |

Use `primary_naics` to filter by primary classification or `naics_codes` to search across all registered codes.