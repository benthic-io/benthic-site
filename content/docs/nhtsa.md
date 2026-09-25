---
title: "NHTSA vPIC Vehicle Information"
aliases:
  - /docs/NHTSA/
---

### https://benthic.io/parts/NHTSA/ – NHTSA Vehicle Product Information Catalog

The NHTSA dataset combines the official vPIC PostgreSQL decoder with the vPIC reference data used to interpret vehicles, manufacturers, makes, models, WMI codes, variable values, and equipment plants. The decoder is served locally from the September 2026 vPIC bulk release; reference tables are synchronized from the vPIC API.

The default profile is the upstream `vpic` schema. Reference tables are under the `api_reference` profile and are published at the `/reference/` path.

## Quick start

```bash
# Decode one VIN
curl -X POST "https://benthic.io/parts/NHTSA/rpc/spvindecode" \
  -H "Content-Type: application/json" \
  -d '{"v":"1HGCM82633A004352"}'

# Decode a batch
curl -X POST "https://benthic.io/parts/NHTSA/rpc/spvindecodemultiple" \
  -H "Content-Type: application/json" \
  -d '{"vin_list":["1HGCM82633A004352","1FTFW1ET4EFA12345"]}'

# Query the upstream decoder tables
curl "https://benthic.io/parts/NHTSA/wmi?limit=1"
curl "https://benthic.io/parts/NHTSA/make?select=id,name&order=name&limit=20"

# Query synchronized reference data
curl "https://benthic.io/parts/NHTSA/reference/manufacturers?limit=25"
curl "https://benthic.io/parts/NHTSA/reference/wmi_codes?select=wmi,brand_name,country&limit=25"
```

The decoder returns one row per decoded variable. The `Error Code` and `Error Text` variables report whether the VIN decoded cleanly. A VIN that is syntactically valid but not present in the current vPIC patterns may return a non-clean result.

## Data profiles

| Public path               | PostgREST profile | Contents                                                                             |
| ------------------------- | ----------------- | ------------------------------------------------------------------------------------ |
| `/parts/NHTSA/`           | `vpic`            | Official vPIC decoder tables and decoder RPCs                                        |
| `/parts/NHTSA/reference/` | `api_reference`   | Manufacturers, WMI codes, variables, values, historical models, and equipment plants |

When calling the database directly rather than through the published proxy, select the reference profile with `Accept-Profile: api_reference` on GET requests and `Content-Profile: api_reference` on writes.

## Key tables

### Upstream decoder tables

| Table            | Purpose                                                      |
| ---------------- | ------------------------------------------------------------ |
| `wmi`            | World Manufacturer Identifier records and manufacturer links |
| `manufacturer`   | Manufacturer records in the decoder snapshot                 |
| `make`           | Make records used by VIN patterns                            |
| `model`          | Model records used by VIN patterns                           |
| `element`        | Variable definitions used by decoded output                  |
| `vinschema`      | VIN schema and pattern records                               |
| `vindescriptor`  | Variable descriptors used to build decoded results           |
| `decodingoutput` | Decoded output projections supplied by the official database |

Use the [OpenAPI specification](/api/NHTSA.json) for the complete relation and column contract.

### Reference tables

| Table               | Key columns                                | Purpose                                        |
| ------------------- | ------------------------------------------ | ---------------------------------------------- |
| `manufacturers`     | `manufacturer_id`, `manufacturer_name`     | vPIC manufacturer directory                    |
| `wmi_codes`         | `wmi`, `manufacturer_id`                   | WMI, make, vehicle type, and country reference |
| `vehicle_variables` | `variable_id`, `variable_name`             | Variable definitions and lookup metadata       |
| `variable_values`   | `variable_id`, `value_id`                  | Values used by lookup variables                |
| `models_historical` | `make_id`, `model_id`, `year`              | Serialized vPIC model history                  |
| `equipment_plants`  | `equipment_type`, `plant_year`, `dot_code` | Manufacturer equipment plant reports           |

## Querying reference data

```bash
# Search manufacturers
curl "https://benthic.io/parts/NHTSA/reference/manufacturers?manufacturer_name=ilike.*HONDA*&select=manufacturer_id,manufacturer_name,manufacturer_common_name&limit=25"

# Find WMI codes for a manufacturer
curl "https://benthic.io/parts/NHTSA/reference/wmi_codes?manufacturer_id=eq.2364&select=wmi,brand_name,country&order=wmi&limit=100"

# List active equipment plants in a country
curl "https://benthic.io/parts/NHTSA/reference/equipment_plants?plant_country=ilike.*UNITED STATES*&plant_status=eq.Active&select=plant_name,plant_city,plant_state,dot_code&limit=50"

# Historical models for a make
curl "https://benthic.io/parts/NHTSA/reference/models_historical?make_id=eq.468&select=year,model_id,model_name&order=year.desc&limit=100"
```

## PostgREST query reference

| Operation               | Syntax                                     |
| ----------------------- | ------------------------------------------ |
| Filter                  | `?column=eq.value`                         |
| Select columns          | `?select=column_a,column_b`                |
| Case-insensitive search | `?column=ilike.*pattern*`                  |
| Null test               | `?column=is.null` or `?column=not.is.null` |
| Ordering                | `?order=column.desc`                       |
| Pagination              | `?limit=100&offset=200`                    |
| Count                   | `?select=count` with `Prefer: count=exact` |
| Embedded relation       | `?select=table(column_a,column_b)`         |

## Provenance and limits

- The decoder tables and functions come from the official NHTSA/vPIC PostgreSQL bulk release `vPICList_lite_2026_09`, released September 16, 2026.
- Reference tables are populated by the single-worker, resumable `parts-pipelines` importer with a minimum one-second request interval and an immediate circuit breaker on HTTP 403.
- The upstream vPIC database is a decoder snapshot, not a complete substitute for every current API response. The synchronized reference layer is published separately under `/reference/`.
- The importer skips plant rows without a stable DOT code and records all fetches under the private `nhtsa_import` schema.
- NHTSA/vPIC data is a U.S. government work; check the [NHTSA site](https://www.nhtsa.gov/about) for applicable terms and attribution requirements.

The signed [BDP manifest](/bdp/parts/nhtsa/manifest.json) and [collection](/bdp/parts/collection.json) describe the published schema and provenance.
