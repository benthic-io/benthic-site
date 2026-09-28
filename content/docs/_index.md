---
title: "API reference"
description: "Per-dataset reference for every API published on benthic.io — tables, views, RPC functions, and runnable PostgREST examples."
---

### Documentation map

Every dataset, and where its documentation lives, is listed on one page:
[the documentation map](/docs/map/). It is generated from the dataset registry
and checked in CI, so a dataset cannot be published without documentation.

### NGOpen

Federal spending, nonprofit, and legislative data. Five PostgREST APIs over
PostgreSQL/PostGIS, designed to be joined — see the
[join paths and worked cross-dataset queries](/apis/) for how they connect.

- **[USAspending](/docs/usaspending/)** — Federal spending: prime awards, subawards, financial accounts, and agency references from [USAspending.gov](https://www.usaspending.gov/).
- **[IRS Nonprofits](/docs/irs_ng/)** — IRS Exempt Organizations Business Master File, Form 990 SOI financials, Publication 78, auto-revocations, 990-N e-Postcards, 990 XML filings, Section 527 political organizations, and ACS census demographics.
- **[SAM Entity Registry](/docs/samer/)** — SAM.gov entity registrations for federal contractors and vendors.
- **[Congressional District Maps](/docs/up_cdmaps/)** — UCLA PolySci's congressional district boundaries for every Congress, served over PostGIS.
- **[Congress Legislators](/docs/usp_cl/)** — [@unitedstatesproject](https://unitedstates.github.io/)'s congress-legislators: members of Congress past and present, terms, committees, and district offices.

### Parts

Vehicle, component, and identifier reference data. A separate collection with
its own signed manifest; these datasets are **not** part of NGOpen.

- **[NHTSA vPIC Vehicle Information](/docs/nhtsa/)** — official vPIC decoder tables, VIN decoding RPCs, and synchronized manufacturer, WMI, variable, model, and equipment-plant reference data.

### Machine-readable references

Every endpoint has an OpenAPI specification, browsable at
[/swagger/](/swagger/) and served as JSON:

| Dataset                     | Specification                                    |
| --------------------------- | ------------------------------------------------ |
| USAspending                 | [`/api/usaspending.json`](/api/usaspending.json) |
| IRS Nonprofits              | [`/api/irs_ng.json`](/api/irs_ng.json)           |
| SAM Entity Registry         | [`/api/samer.json`](/api/samer.json)             |
| Congressional District Maps | [`/api/up_cdmaps.json`](/api/up_cdmaps.json)     |
| Congress Legislators        | [`/api/usp_cl.json`](/api/usp_cl.json)           |
| NHTSA vPIC                  | [`/api/NHTSA.json`](/api/NHTSA.json)             |

> **Note the casing.** Five specifications are lowercase; the NHTSA
> specification is uppercase, matching its `/parts/NHTSA/` API path. The
> reference page and swagger page for NHTSA are lowercase, with uppercase
> aliases at `/docs/NHTSA/` and `/swagger/NHTSA/`.

Each dataset also publishes a signed [BDP manifest](/bdp/) describing its
schema, provenance, and endpoints.
