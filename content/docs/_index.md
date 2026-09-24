---
title: "APIs"
---

### NGOpen Documentation

Reference documentation for each API in the NGOpen collection. Every page covers the key tables, views, and RPC functions for its dataset, with runnable [PostgREST](https://postgrest.org/) query examples.

### Parts Documentation

Reference documentation for the Parts collection. These datasets use BDP provenance manifests and are not part of NGOpen.

- **[NHTSA vPIC Vehicle Information](/docs/NHTSA/)** – official vPIC decoder tables, VIN decoding RPCs, and synchronized manufacturer, WMI, variable, model, and equipment-plant reference data.

- **[USAspending](/docs/usaspending/)** – Federal spending: prime awards, subawards, financial accounts, and agency references from [USAspending.gov](https://www.usaspending.gov/).

- **[SAM Entity Registry](/docs/samer/)** – SAM.gov entity registrations for federal contractors & vendors.

- **[Congressional District Maps](/docs/up_cdmaps/)** – UCLA Polysci's congressional district maps & boundaries for every congress to present day, served over PostGIS.

- **[Congress Legislators](/docs/usp_cl/)** – [@unitedstatesproject](https://unitedstates.github.io/)'s congress-legislators: members of Congress past & present, terms, committees, and offices.

- **[IRS Nonprofits](/docs/irs_ng/)** – IRS Exempt Organizations Business Master File, Form 990 SOI financials, Publication 78, auto-revocations, 990-N e-Postcards, 990 XML filings, Section 527 political organizations, and ACS census demographics.

Machine-readable OpenAPI specifications for every endpoint are published at `/api/<dataset>.json` (for example [`/api/usaspending.json`](/api/usaspending.json)), and each dataset also publishes a signed [BDP manifest](/bdp/) describing its schema, provenance, and endpoints.
