---
title: "APIs"
---

### NGOpen API Collection

Benthic.io's debut API collection, dubbed NGOpen, consists of five PostgREST APIs exposed directly at the listed root URLs.  They return OpenAPI JSON specs and expose standard public REST endpoints to provide structured, queryable access to geospatially enhanced versions of major U.S. government datasets enhanced with latitude/longitude and PostGIS geometry columns. They also include census linkages, NAICS/PSC/CFDA crosswalks, reference tables for ZIPs/congressional districts, and more. This enables spatial filtering, proximity searches, point-in-polygon lookups, distance calculations, and mapping capabilities absent from the original sources. Together, these datasets aim turn raw government data and other publically available information into a geographically intelligent investigative toolkit. If something is missing, broken, or you have any ideas to expand functionality please do not hesitate to contact me via one of the channels listed at the bottom of the page. 

- **https://benthic.io/ngopen/usaspending/** – [USAspending.gov](https://www.usaspending.gov/) database enhanced with geocoding data. - [Documentation](/ngopen/usaspending/)

- **https://benthic.io/ngopen/samer/** – SAM.gov entity registrations for federal contractors & vendors enhanced with geocoding data.- [Documentation](/ngopen/samer/)

- **https://benthic.io/ngopen/up_cdmaps/** – UCLA Polysci's comprehesive congressional district maps & boundaries for every congress to present day. - [Documentation](/ngopen/up_cdmaps/)

- **https://benthic.io/ngopen/usp_cl/** – [@unitedstatesproject](https://unitedstates.github.io/)'s congress-legislators provides detailed data on members of Congress past & present.  - [Documentation](/ngopen/usp_cl/)

- **https://benthic.io/ngopen/irs_ng/** – Geocoded versions of IRS Exempt Organizations Business Master File, Form 990/990-EZ/990-PF SOI financials, Publication 78 deductibility eligibility, auto-revocation list, Form 990T, Form 990-N e-Postcard, Form 990 XML filings with Schedule O narratives and Schedule R flags, Section 527 political organizations, and ACS census demographics. - [Documentation](/ngopen/irs_ng/)

&nbsp;

### Join paths

| From | To | Key | Method |
|---|---|---|---|
| usaspending | samer | `uei` or `duns` | Direct match via `uei_crosswalk`, `historic_parent_duns`, or `sam_registrations` |
| usaspending | irs_ng | `ein` ≈ `duns` | DUNS often matches EIN for nonprofit recipients |
| samer | irs_ng | `duns` ≈ `ein` | DUNS often matches EIN for nonprofits |
| samer | irs_ng | — | Spatial join on geocoded addresses (Photon) |
| usaspending | up_cdmaps | — | Spatial join: `recipient_geocode_index` point -> district polygon |
| irs_ng | up_cdmaps | — | Spatial join: `bmf_organizations` lat/lon -> district polygon |
| usp_cl | up_cdmaps | `state` + `district` | Direct match on legislator terms to district boundaries |
| all geocoded | all geocoded | `latitude`, `longitude` | Photon geocoding is consistent across all databases |

## Use Cases

These scenarios show what becomes possible when combining datasets that individually describe only one facet of government.

### 1. Where does federal grant money go?

**Databases:** usaspending + irs_ng
**Join:** `fain` (grant ID) -> nonprofit -> `ein` -> BMF organization

Find which nonprofits receive federal grants, then pull their Form 990 financials to see how the money is spent. Cross-check deductibility status via Pub78 and revocation history.

```bash
# Step 1: Find grant transactions in usaspending
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?select=fain,obligations_incurred_total_by_award_cpe,treasury_appropriation_account(toptier_agency(name))&fain=not.is.null&obligations_incurred_total_by_award_cpe=gt.10000000&order=obligations_incurred_total_by_award_cpe.desc&limit=10"

# Step 2: Look up the recipient in irs_ng by EIN (which often matches DUNS)
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?ein=eq.123456789&select=org_name_current,ntee_irs,f990_org_addr_state,latitude,longitude,is_current"

# Step 3: Pull their 990 financials
curl "https://benthic.io/ngopen/irs_ng/form990_soi?ein=eq.123456789&select=tax_year,total_revenue,total_expenses,total_assets,contributions,compensation_officers&order=tax_year.desc"
```

### 2. Contractor profiles

**Databases:** usaspending + samer
**Join:** `uei` or `duns`

See a contractor's SAM.gov registration details alongside their federal award history. Understand what they do (NAICS/PSC), where they are, and how much they've received.

```bash
# Find a contractor's SAM registration
curl "https://benthic.io/ngopen/samer/sam_registrations?uei=eq.ABCDEFGHIJK&select=legal_business_name,physical_city,physical_state,primary_naics,naics_codes,latitude,longitude"

# Find their contract awards in usaspending
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?distinct_award_key=ilike.*ABCDEFGHIJK*&select=piid,obligations_incurred_total_by_award_cpe,gross_outlay_amount_by_award_cpe,reporting_period_end&order=obligations_incurred_total_by_award_cpe.desc&limit=25"
```

### 3. Nonprofits in a congressional district

**Databases:** irs_ng + up_cdmaps
**Join:** Spatial join on geocoded address -> district polygon

Enumerate all tax-exempt organizations operating within a congressional district. Filter by NTEE code to focus on education, health, housing, etc.

```bash
# Get the district boundary geometry
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?statename=eq.Texas&district=eq.7&congress_number=eq.118&select=id,statename,district,geom"

# Geocoded orgs can be spatial-joined client-side using the district geometry
# Or query by approximate bounding box:
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?latitude=gte.29.5&latitude=lte.30.0&longitude=gte.-95.8&longitude=lte.-95.2&is_current=is.true&latitude=not.is.null&select=ein,org_name_current,ntee_irs,bmf_subsection_code&limit=100"
```

### 4. Federal spending in a legislator's district

**Databases:** usp_cl + up_cdmaps + usaspending
**Join:** legislator terms (state+district) -> district geometry -> recipient locations

Map federal spending into a specific legislator's district. See which agencies are funding what, and which recipients are located there.

```bash
# Find a legislator and their district
curl "https://benthic.io/ngopen/usp_cl/legislators?official_full=ilike.*smith*&select=bioguide_id,official_full,legislator_terms!inner(state,district,party,term_type)&legislator_terms.term_end=gte.2026-01-01"

# Get the district boundary
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?statename=eq.California&district=eq.20&congress_number=eq.118&select=geom"

# Find geocoded recipients within approximate district bounds
curl "https://benthic.io/ngopen/usaspending/recipient_geocode_index?latitude=gte.36.5&latitude=lte.37.0&longitude=gte.-121.0&longitude=lte.-120.0&latitude=not.is.null&select=source_id,latitude,longitude&limit=100"
```

### 5. Are revoked nonprofits still receiving federal funds?

**Databases:** irs_ng + usaspending
**Join:** `ein` (from revocation list) -> `duns` (in usaspending)

Cross-reference the IRS auto-revocation list against federal award data to identify spending anomalies.

```bash
# Get revoked organizations
curl "https://benthic.io/ngopen/irs_ng/revoked_organizations?revocation_date=gte.2023-01-01&select=ein,org_name,revocation_date&limit=100"

# Check if any received federal funds after revocation
# (client-side: take the EIN list and query usaspending with matching DUNS)
```

### 6. Census-contextualized spending

**Databases:** usaspending + irs_ng (census_demographics)
**Join:** geocoded address -> census tract GEOID -> demographics

Analyze federal funding relative to community need. Compare spending per capita against poverty rates, median income, and population density at the census tract level.

```bash
# Get demographics for a census tract
curl "https://benthic.io/ngopen/irs_ng/census_demographics?geoid=eq.36061000100&geo_type=eq.tract&year=eq.2022&select=total_population,median_household_income,poverty_count"

# Get nonprofits in that area (approximate lat/lon)
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?latitude=gte.40.7&latitude=lte.40.8&longitude=gte.-73.9&longitude=lte.-74.0&is_current=is.true&latitude=not.is.null&select=ein,org_name_current,ntee_irs&limit=50"
```

### 7. Committee jurisdiction and federal spending

**Databases:** usp_cl + usaspending
**Join:** committee jurisdiction text -> agency/budget function

Connect congressional committee oversight to the agencies and programs they fund. See which legislators sit on committees that authorize the spending their districts receive.

```bash
# Get Appropriations Committee members
curl "https://benthic.io/ngopen/usp_cl/committee_membership?committee_thomas_id=eq.SAPP&select=legislator_name,party,rank,title&order=rank"

# Get their district offices (geocoded)
curl "https://benthic.io/ngopen/usp_cl/district_offices?bioguide_id=eq.S000033&select=city,state,latitude,longitude"

# Get budget authority for Defense (agency_identifier 097)
curl "https://benthic.io/ngopen/usaspending/budget_authority?agency_identifier=eq.097&select=year,amount&order=year.desc"
```

### 8. Geographic clustering of federal funding

**Databases:** usaspending + samer + irs_ng
**Join:** All geocoded via Photon API (consistent lat/lon)

Identify hotspots where federal spending, nonprofit activity, and contractor registrations cluster geographically. All three databases use the same Photon geocoding scheme, enabling direct spatial comparison.

```bash
# Federal recipients in a region
curl "https://benthic.io/ngopen/usaspending/recipient_geocode_index?latitude=gte.38.8&latitude=lte.39.0&longitude=gte.-77.1&longitude=lte.-76.9&latitude=not.is.null&select=source_id,latitude,longitude&limit=100"

# Nonprofits in the same region
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?latitude=gte.38.8&latitude=lte.39.0&longitude=gte.-77.1&longitude=lte.-76.9&is_current=is.true&latitude=not.is.null&select=ein,org_name_current,ntee_irs&limit=100"

# SAM-registered entities in the same region
curl "https://benthic.io/ngopen/samer/sam_registrations?latitude=gte.38.8&latitude=lte.39.0&longitude=gte.-77.1&longitude=lte.-76.9&latitude=not.is.null&select=uei,legal_business_name,primary_naics&limit=100"
```



## Geocoding

All databases with address data were building using local [Photon](https://photon.komoot.io/) geocoder instances with [OpenStreetMap](https://www.openstreetmap.org) data for consistent spatial coordinates. This means:

- **Same coordinate system** across usaspending, irs_ng, and samer
- **Direct spatial comparison** between federal spending recipients, nonprofits, and contractors
- **Bounding box queries** work identically across all geocoded tables
- **Spatial joins** between datasets require no coordinate transformation
- **PostGIS `geom_point` columns** on all geocoded tables enable native spatial queries (ST_DWithin, ST_Intersects, etc.)

Geocoded columns across datasets:

| Database | Table | lat column | lon column | PostGIS geom | GIST index |
|---|---|---|---|---|---|
| usaspending | `recipient_geocode_index` | `latitude` | `longitude` | `geom_point` (Point, 4326) | `idx_rgi_geom_point` |
| irs_ng | `bmf_organizations` | `latitude` | `longitude` | `geom_point` (Point, 4326) | `idx_bmf_geom_point` |
| irs_ng | `political_orgs_527` | `latitude` | `longitude` | `geom_point` (Point, 4326) | `idx_527_geom_point` |
| samer | `sam_registrations` | `latitude` | `longitude` | `geom_point` (Point, 4326) | `idx_sam_geom_point` |
| usp_cl | `district_offices` | `latitude` | `longitude` | `geom_point` (Point, 4326) | `idx_offices_geom_point` |
| up_cdmaps | `congressional_districts` | — | — | `geom` (MultiPolygon, 3857) | `idx_cd_geom` |

All point geometries use SRID 4326 (WGS 84). The congressional districts polygon uses SRID 3857 (Web Mercator) — PostGIS can transform between them on-the-fly with `ST_Transform()`.

## PostgREST Query Syntax

All five databases use the same PostgREST query syntax. Common patterns:

| Operation | Syntax |
|---|---|
| Filter | `?column=eq.value` |
| Select columns | `?select=col1,col2,col3` |
| Order | `?order=column.desc` |
| Limit | `?limit=100` |
| Offset | `?offset=200` |
| Count | `Prefer: count=exact` |
| Not null | `?column=not.is.null` |
| Pattern match | `?column=ilike.%25search%25` |
| Embed (join) | `?select=col,related_table(col)` |

Full syntax reference: [PostgREST docs](https://docs.postgrest.org/)
