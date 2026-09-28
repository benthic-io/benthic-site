---
title: "NHTSA vPIC Vehicle Information"
aliases:
  - /docs/NHTSA/
---

### https://benthic.io/parts/NHTSA/ – NHTSA Vehicle Product Information Catalog

The NHTSA dataset combines the official vPIC decoder data with the vPIC reference data used to interpret vehicles, manufacturers, makes, models, WMI codes, variable values, and equipment plants. The decoder and reference data are published through benthic.io; reference tables are synchronized from the vPIC API.

The default profile contains the decoder tables and RPCs. Reference tables are published at the `/reference/` path.

## At a glance

| | |
|---|---|
| Collection | Parts |
| Endpoint | [`/parts/NHTSA/`](https://benthic.io/parts/NHTSA/) |
| OpenAPI | [`NHTSA.json`](/api/NHTSA.json) |
| Manifest | [`parts/nhtsa`](https://benthic.io/bdp/parts/nhtsa/manifest.json) |
| Provenance | `migrated` 2026-09-24, commit `81e1d7de3c` |
| Relations | 106 queryable of 107 |
| Columns | 383 |
| Updated | Monthly |
| Licence | Public domain (U.S. federal government work). See https:/... |
| Source | 2 upstream feeds (see [Data sources](#data-sources)) |
| Pipeline | [partout-pipelines/pipelines/nhtsa/README.md](https://github.com/benthic-io/partout-pipelines/blob/main/pipelines/nhtsa/README.md) |
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

The published reference path selects the `api_reference` profile automatically. Direct PostgREST clients can select it with `Accept-Profile: api_reference` on GET requests and `Content-Profile: api_reference` on writes.

## Tables

### Decoder tables

| Table            | Purpose                                                              |
| ---------------- | -------------------------------------------------------------------- |
| `wmi`            | World Manufacturer Identifier records and manufacturer links         |
| `manufacturer`   | Manufacturer records in the decoder snapshot                         |
| `make`           | Make records used by VIN patterns                                    |
| `model`          | Model records used by VIN patterns                                   |
| `element`        | Variable definitions used by decoded output                          |
| `vinschema`      | VIN schema and pattern records                                       |
| `vindescriptor`  | Variable descriptors used to build decoded results                   |
| `decodingoutput` | Decoded output projections supplied by the published decoder dataset |

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

The same syntax as every other benthic.io dataset. Paths differ: decoder tables
and RPCs are at the root, reference tables under `/reference/`.

### Filtering

| Operator     | Syntax                | Example                            |
| ------------ | --------------------- | ---------------------------------- |
| Equals       | `?col=value`          | `?manufacturer_id=eq.2364`         |
| Not equal    | `?col=neq.value`      | `?plant_status=neq.Closed`         |
| Greater than | `?col=gt.value`       | `?year=gt.2020`                    |
| Less than    | `?col=lt.value`       | `?year=lt.2010`                    |
| Greater/eq   | `?col=gte.value`      | `?year=gte.2018`                   |
| Less/eq      | `?col=lte.value`      | `?year=lte.2026`                   |
| LIKE         | `?col=like.PATTERN`   | `?model_name=like.*CIVIC*`         |
| ILIKE        | `?col=ilike.PATTERN`  | `?manufacturer_name=ilike.*HONDA*` |
| IS null      | `?col=is.null`        | `?plant_code=is.null`              |
| IS NOT null  | `?col=not.is.null`    | `?dot_code=not.is.null`            |
| IN           | `?col=in.(val1,val2)` | `?year=in.(2023,2024,2025)`        |

> **Case-insensitive matching:** use `ilike`, not `like`, when the pattern
> casing is unknown. `ilike` treats `*` as the wildcard; the pattern must be
> URL-encoded, so `*` is `%25` in a query string.

### Selecting columns

```text
?select=manufacturer_id,manufacturer_name
```

Omitting `select` returns every column, which on `models_historical` is
substantially more data than you usually want.

### Ordering

```text
?order=year.desc
?order=manufacturer_name.asc,year.desc
```

### Pagination

```text
?limit=100&offset=200
```

Or use range headers:

```http
Range: 0-99
```

### Counting

```http
Prefer: count=exact
```

```text
?select=count
```

### Grouping / aggregation

```text
?select=plant_state,count&groupby=plant_state&order=count.desc
```

### Calling the decoder functions

The two vPIC decoder RPCs take a JSON body and are called with `POST`:

```bash
curl -X POST "https://benthic.io/parts/NHTSA/rpc/spvindecode" \
  -H "Content-Type: application/json" \
  -d '{"VIN": "1HGCM82633A004352"}'

curl -X POST "https://benthic.io/parts/NHTSA/rpc/spvindecodemultiple" \
  -H "Content-Type: application/json" \
  -d '{"VINs": ["1HGCM82633A004352", "5YJ3E1EA8LF000000"]}'
```

## Provenance and limits

- The decoder tables and functions are published through benthic.io from the official NHTSA/vPIC dataset.
- Reference tables are synchronized from the vPIC API and published under `/reference/`.
- The published decoder data is a snapshot; some current vPIC API responses may differ.
- Plant records without a stable DOT code are omitted from the reference tables.
- NHTSA/vPIC data is a U.S. government work; check the [NHTSA site](https://www.nhtsa.gov/about) for applicable terms and attribution requirements.

The signed [BDP manifest](/bdp/parts/nhtsa/manifest.json) and [collection](/bdp/parts/collection.json) describe the published schema and provenance.

## Key relationships

NHTSA sits in the `parts` collection and shares no key with the NGOpen
datasets — there is no join from vehicle reference data to federal spending,
nonprofit, or legislative data. What it does offer is a lookup direction:

- **`spvindecode` is a bridge from an arbitrary string to structured data.** A
  VIN that appears in a fleet operator's records, an insurance claim, or a
  recall notice can be decoded to make, model, year, and manufacturer without
  knowing any of them in advance. That is the intended entry point.
- **Manufacturer names are the loose join to everything else.** `manufacturers`
  and `wmi_codes` carry name and country columns, so a manufacturer observed in
  `samer` or `usaspending` can be matched by name — but this is a fuzzy
  entity-resolution problem, not a key. Do not treat it as one.
- **The WMI prefix encodes the manufacturer.** The first three characters of a
  VIN are the World Manufacturer Identifier and appear in `wmi_codes`, so a
  partially-redacted VIN can often be resolved to a manufacturer without a
  full decode.

## Data sources

| Source                                                                                                  | Description                                                                                                         | Update frequency |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------- |
| [NHTSA vPIC API](https://vpic.nhtsa.dot.gov/api/)                                                       | Reference tables: manufacturers, WMI codes, vehicle variables, variable values, historical models, equipment plants | Periodic         |
| [NHTSA vPIC bulk decoder release](https://vpic.nhtsa.dot.gov/downloads/vPICList_lite_2026_09.plain.zip) | VIN decoder tables and functions, pinned by SHA-256                                                                 | Monthly          |

Decoder data is a snapshot of the current vPIC release and is refreshed
monthly. Reference tables are synchronised from the API and published under
`/reference/`; some current vPIC API responses may differ from the published
snapshot.

All data originates from publicly available U.S. government sources. NHTSA/vPIC
is a U.S. government work — see the [NHTSA site](https://www.nhtsa.gov/about)
for applicable terms and attribution requirements.

## Related

- [Swagger explorer](https://benthic.io/swagger/nhtsa/) — interactive API browser for `/parts/NHTSA`
- [Signed manifest](https://benthic.io/bdp/parts/nhtsa/manifest.json) — every relation, column, and licence, signed with the publisher's Ed25519 key
- [Pipeline README](https://github.com/benthic-io/partout-pipelines/blob/main/pipelines/nhtsa/README.md) — how this dataset is actually built
- [BDP specification](https://benthic.io/bdp/) — what the manifest signature proves, and how to verify it offline
- [Documentation map](https://benthic.io/docs/map/) — every dataset on benthic.io and where its documentation lives
- [APIs overview](https://benthic.io/apis/) — join paths between datasets and worked cross-collection queries
- In Ngopen: [USAspending](https://benthic.io/docs/usaspending/), [SAM Entity Registry](https://benthic.io/docs/samer/), [IRS Nonprofits](https://benthic.io/docs/irs_ng/), [Congress Legislators](https://benthic.io/docs/usp_cl/), [Congressional District Maps](https://benthic.io/docs/up_cdmaps/)
