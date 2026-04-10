# NGOpen AI Agent Guide

Government spending investigative data toolkit. Five PostgREST APIs backed by PostgreSQL databases, providing unified access to federal spending, nonprofit, contractor, legislative, and geographic data.

## System Overview

| Service | URL | Database | Purpose |
|---------|-----|----------|---------|
| USAspending | `/ngopen/usaspending/` | usaspending_db | Federal grants, contracts, loans, subawards |
| SAM.gov | `/ngopen/samer/` | sam_er | Entity registration, NAICS/PSC codes |
| IRS NGO | `/ngopen/irs_ng/` | irs_ng | 501(c)(3) nonprofits, Form 990, 527 political orgs |
| Congress-Leg | `/ngopen/usp_cl/` | us_project_cl | Legislators, committees, leadership history |
| CD Maps | `/ngopen/up_cdmaps/` | ucla_polysci_cdmaps | Congressional district boundaries, demographics |

Base URL for all examples: `https://benthic.io`

Full OpenAPI specs:
- [usaspending.json](/api/usaspending.json)
- [samer.json](/api/samer.json)
- [irs_ng.json](/api/irs_ng.json)
- [usp_cl.json](/api/usp_cl.json)
- [up_cdmaps.json](/api/up_cdmaps.json)

## PostgREST Quick Reference

Full documentation: [PostgREST Docs](https://postgrest.org/en/stable/references/api/tables_views.html)

### Basic Queries

```
GET /table?select=col1,col2&col3=eq.value&order=col1.desc&limit=100
```

| Parameter | Example | Description |
|-----------|---------|-------------|
| `select` | `select=*,related_table(col1,col2)` | Columns + embedded joins |
| `eq` | `name=eq.Acme` | Exact match |
| `ilike` | `name=ilike.*acme*` | Case-insensitive pattern |
| `gt/gte/lt/lte` | `amount=gt.1000000` | Numeric comparison |
| `in` | `state=in.(CA,NY,TX)` | Set membership |
| `order` | `order=date.desc` | Sort direction |
| `limit/offset` | `limit=100&offset=200` | Pagination |
| `or` | `or=(name.ilike.*acme*,alias.ilike.*acme*)` | OR logic |
| `not` | `name=not.is.null` | NOT null |
| `csv` | Append `&format=csv` | CSV output |

### Embedded Joins

Use parentheses `()` for embedding, not curly braces. PostgREST auto-detects foreign keys.

```bash
# Award with agency name via FK chain
GET /ngopen/usaspending/financial_accounts_by_awards?select=fain,obligations_incurred_total_by_award_cpe,treasury_appropriation_account(toptier_agency(name))

# Subaward with parent prime award info
GET /ngopen/usaspending/subawards?select=subaward_id,subaward_amount,prime_awards(piid,prime_award_amount,prime_recipient_name)

# Legislator terms with embedded legislator name
GET /ngopen/usp_cl/legislator_terms?select=legislators(first_name,last_name,official_full),state,district,party,term_start,term_end

# Committee membership
GET /ngopen/usp_cl/committee_membership?select=legislator_name,committee_thomas_id,rank,title&bioguide_id=eq.X000001
```

For multiple FK paths to the same table, use hints: `toptier_agency:toptier_agency_1(name)`.

### Range Filters (same column, two bounds)

Use `and=()` when filtering a single column with both upper and lower bounds:

```bash
# WRONG: latitude=gte.34.0&latitude=lte.34.2 (second overwrites first)
# RIGHT:
GET /ngopen/usaspending/recipient_geocode_index?select=*&and=(latitude.gte.34.0,latitude.lte.34.2,longitude.gte.-118.3,longitude.lte.-118.1)&latitude=not.is.null&limit=50
```

### Operators

```bash
GET /table?and=(col1.gt.100,col2.lt.200)
GET /table?or=(col1.eq.foo,col2.eq.bar)
GET /table?col=not.is.null
GET /table?col=is.null
```

### Aggregation

PostgREST does not support server-side `GROUP BY` via query parameters. Aggregation must be done client-side or via materialized views.

```bash
# WRONG: group=state (not valid PostgREST)
# RIGHT: fetch rows and aggregate client-side, or use a pre-computed view
GET /ngopen/irs_ng/bmf_organizations?select=f990_org_addr_state&is_current=is.true&limit=5000
# Then count occurrences of each state in your code
```

## Data Type Notes

- `action_date` is a date string: `YYYY-MM-DD`
- `fiscal_year` is an integer: `2024` not `"2024"`
- `pop_congressional_district` stores just the district number as a string: `"11"` not `"CA-11"`
- `term_end`, `term_start`, `action_date`, `date_signed` are all `YYYY-MM-DD` strings

## Entity Resolution & Crosswalk

### Identifiers

| Identifier | Format | Source | Reliability |
|------------|--------|--------|-------------|
| UEI | 12-char alphanumeric (e.g., `A1B2C3D4E5F6`) | SAM.gov, USAspending | Highest - current standard |
| DUNS | 9-digit (e.g., `123456789`) | Legacy USAspending, SAM.gov | High - phased out 2022 |
| EIN | XX-XXXXXXX (e.g., `12-3456789`) | IRS Form 990 | High for nonprofits |
| CAGE | 5-char alphanumeric | SAM.gov, Defense contracts | High for contractors |

### Cross-Database Join Patterns

These are the primary keys for linking across APIs. Cross-database joins must be done client-side (two sequential API calls).

| From | To | Key | Method | Reliability |
|------|----|-----|--------|-------------|
| `usaspending.prime_awards.recipient_uei` | `samer.sam_registrations.uei` | UEI | Direct match | Reliable |
| `usaspending.prime_awards.parent_duns` | `samer.sam_registrations.duns` | DUNS | Direct match | Reliable |
| `usaspending.uei_crosswalk.awardee_or_recipient_uniqu` | `usaspending.uei_crosswalk.uei` | DUNS→UEI | Crosswalk table | Reliable |
| `usaspending.prime_awards.recipient_name` | `irs_ng.bmf_organizations.org_name_current` | Name | Heuristic match | Partial |
| `irs_ng.bmf_organizations.ein` | `irs_ng.form990_soi.ein` | EIN | Direct match | Reliable |
| `irs_ng.bmf_organizations.ein` | `irs_ng.political_orgs_527.ein` | EIN | Direct match | Reliable |
| `usp_cl.legislator_terms.bioguide_id` | `usp_cl.committee_membership.bioguide_id` | bioguide_id | Direct match | Reliable |
| `usp_cl.legislator_terms.bioguide_id` | `usp_cl.district_offices.bioguide_id` | bioguide_id | Direct match | Reliable |
| `usp_cl.legislator_terms.state` + `district` | `up_cdmaps.congressional_districts.statename` + `district` | State+District | Direct match | Reliable |
| All geocoded tables | All geocoded tables | `geom_point` (SRID 4326) | Spatial join via RPC | Reliable |

### Entity Reliability Ratings

| Match Type | Confidence | Notes |
|------------|-----------|-------|
| UEI exact match | ★★★★★ | Authoritative |
| EIN exact match | ★★★★★ | Authoritative for nonprofits |
| DUNS exact match | ★★★★☆ | Legacy but reliable |
| Name + city + state | ★★★☆☆ | False positives possible |
| Name only | ★★☆☆☆ | Many false positives |
| Fuzzy name match | ★★☆☆☆ | Requires manual review |

## Key Tables Reference

Full schema: load any OpenAPI JSON file from `/api/*.json` into an OpenAPI viewer for complete column reference.

### USAspending (`usaspending_db`)

Size warnings: `prime_awards` ~50M+ rows, `financial_accounts_by_awards` ~820M+ rows. Always use filters.

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `prime_awards` | All federal prime awards | `award_id, piid, parent_duns, parent_uei, recipient_uei, recipient_duns, recipient_name, award_amount, action_date, date_signed, fiscal_year, award_type, awarding_agency, awarding_agency_code, funding_agency, funding_agency_code, naics_code, naics_description, product_or_service_code, product_or_service_description, description, pop_state, pop_city, pop_country, pop_congressional_district, recipient_state, recipient_city, recipient_country, total_obligation, total_outlays, total_covid_obligation, total_covid_outlay, cfda_number, cfda_program_title, extent_competed, period_of_performance_start_date, period_of_performance_current_end_date, business_categories, disaster_emergency_fund_codes` |
| `subawards` | Subcontract/subgrant data | `subaward_id, parent_award_id, subrecipient_uei, subrecipient_duns, subrecipient_name, subaward_amount, subaward_description, sub_action_date, prime_recipient_uei, prime_recipient_name, prime_award_amount, prime_award_piid_fain, pop_state, sub_state, sub_city, sub_country, fiscal_year, awarding_agency_name, funding_agency_name, sub_naics, sub_naics_description` |
| `all_entities` | Unified entity registry | `entity_id, legal_business_name, uei, duns, entity_type, total_obligation, award_count, prime_subaward_count, prime_subaward_amount, subaward_received_amount, subaward_received_count, city, state, country_code, congressional_district, address_line_1, address_line_2, zip5, geohash_6, is_geocoded, parent_uei, date_first_award, date_last_award, latitude, longitude, geom_point` |
| `entity_awards` | Entity-aggregate spending | `entity_id, uei, total_award_amount, award_count, first_date, last_date` |
| `financial_accounts_by_awards` | Award-level financial data | `fain, piid, obligations_incurred_total_by_award_cpe, gross_outlay_amount_by_award_cpe, treasury_appropriation_account, reporting_period_end` |
| `financial_accounts_by_program_activity_object_class` | Program+object class spending | `obligations_incurred_by_program_object_class_cpe, program_activity_code, program_activity_name, object_class_code, object_class_name, treasury_appropriation_account` |
| `recipient_geocode_index` | Geocoded recipients | `source_id, latitude, longitude, geom_point` |
| `uei_crosswalk` | UEI/DUNS mapping | `uei, awardee_or_recipient_uniqu, legal_business_name, entity_type` |
| `agency` | Federal agencies | `agency_id, agency_name, toptier_flag, subtier_agency_id, toptier_agency_id` |
| `toptier_agency` | Top-tier agencies | `toptier_agency_id, name, abbreviation` |
| `subtier_agency` | Sub-tier agencies | `subtier_agency_id, name, abbreviation, toptier_agency_id` |
| `budget_authority` | Budget authority by agency/year | `agency_identifier, year, amount` |
| `naics` | NAICS code definitions | `code, description` |
| `psc` | Product/Service codes | `code, description` |
| `references_cfda` | CFDA program listings | `program_number, program_title` |
| `appropriation_account_balances` | Account-level budget data | `treasury_account_identifier, agency_identifier, fiscal_year, obligations_incurred_total` |
| `object_class` | Object class definitions | `object_class_code, object_class_name` |
| `ref_program_activity` | Program activity reference | `program_activity_code, program_activity_name` |
| `disaster_emergency_fund_code` | DEF fund codes | `code, title, public_law` |
| `federal_account` | Federal account reference | `federal_account_code, federal_account_name` |
| `office` | Agency offices | `office_id, office_name, agency_id` |

**Materialized views (usaspending):**

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `mv_agency_autocomplete` | Fast agency search | `agency_id, agency_name, agency_code` |
| `mv_agency_office_autocomplete` | Agency+office search | `agency_id, office_id, name` |
| `tas_autocomplete_matview` | TAS search | `tas_rendering_label, agency_name` |

**Download views (usaspending):** Pre-joined views with agency names included.

| Table | Purpose |
|-------|---------|
| `vw_appropriation_account_balances_download` | Account balances + agency_identifier_name |
| `vw_financial_accounts_by_awards_download` | Award financials + agency names |
| `vw_financial_accounts_by_program_activity_object_class_download` | Program spending + agency names |
| `vw_published_dabs_toptier_agency` | Agencies with published DABS submissions |

**Reference tables (usaspending):**

| Table | Purpose |
|-------|---------|
| `ref_population_cong_district` | Congressional district population by state/district |
| `ref_population_county` | County population by state/county |
| `ref_city_county_state_code` | City/county/state reference with FIPS codes |
| `ref_country_code` | Country code to country name mapping |
| `gtas_sf133_balances` | GTAS SF-133 budget data by TAS/fiscal year |
| `historic_parent_duns` | Historical parent DUNS mappings |
| `submission_attributes` | Submission tracking (submission_id, reporting_fiscal_year) |
| `download_job` | Download job tracking (job_id, status, file_url) |

**Agency lookup helpers:**

| Table | Purpose |
|-------|---------|
| `agency_by_subtier_and_optionally_toptier` | Resolve subtier→toptier agency |
| `agency_lookup` | Quick agency_id→agency_name lookup |

### SAM.gov (`sam_er`)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `sam_registrations` | Registered entities | `uei, duns, legal_business_name, dba_name, physical_address_line1, physical_city, physical_state, physical_country, physical_zip, mailing_city, mailing_state, primary_naics, naics_codes, psc_codes, registration_expiration, is_current, latitude, longitude, geom_point, corporate_url, purpose_of_registration` |

### IRS NGO (`irs_ng`)

Size warning: `bmf_organizations` ~1.2M rows. Ordering by revenue without filters is slow.

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `bmf_organizations` | Business Master File orgs | `ein, org_name_current, org_name_sec, ntee_irs, ntee_nccs, bmf_subsection_code, bmf_foundation_code, bmf_classification_code, bmf_organization_code, bmf_affiliation_code, bmf_group_exempt_num, bmf_income_code, bmf_asset_code, bmf_deductibility_code, org_fiscal_year, org_fiscal_period, f990_org_addr_street, f990_org_addr_city, f990_org_addr_state, f990_org_addr_zip, org_addr_full, f990_total_revenue_recent, f990_total_income_recent, f990_total_assets_recent, org_ruling_date, latitude, longitude, geom_point, is_current, census_state_abbr, census_county_name, geocoder_score, geocoder_match, geocoding_source, imported_at` |
| `form990_soi` | Form 990 SOI financials | `ein, org_name, tax_year, subseccd, is_501c3, ntee_code, state, total_revenue, total_expenses, total_assets, total_liabilities, net_assets, contributions, grants_paid, program_service_revenue, investment_income, royalty_income, net_rental_income, net_gains_losses, gaming_income, tax_exempt_interest, unrelated_business_income, filed_990t, compensation_officers, other_salaries_wages, employee_benefits, payroll_taxes, professional_fundraising, legal_fees, accounting_fees, management_fees, travel, occupancy, office_expenses, depreciation, interest_expense, insurance, pension_contributions, total_reportable_comp, total_estimated_comp, individuals_over_100k, num_employees, investments_end, land_buildings_equipment, cash_end, asset_size, revenue_less_expenses, total_support, foreign_offices, political_activities, lobbying_activities, operates_hospital, donor_advised_funds, num_orgs, non_pf_reason, source_file` |
| `form990_soi_private_foundation` | Private foundation 990s | `ein, tax_year, total_revenue, total_expenses, total_assets, total_liabilities` |
| `form990t_details` | Form 990-T (UBI) | `ein, tax_year, unrelated_business_income, total_tax, deductions` |
| `form990_details` | Detailed 990 data | `ein, tax_year, total_revenue, total_expenses, total_assets` |
| `form990_schedule_o` | Schedule O narratives | `ein, tax_year, schedule_o_text` |
| `form990n_small_orgs` | 990-N e-Postcards | `ein, tax_year, org_name` |
| `form990_xml_import_log` | Import tracking | `ein, org_name, import_date, file_status` |
| `political_orgs_527` | 527 political orgs | `ein, org_name, city, state, status, filing_type, address, zip, filing_date, total_contributions, total_expenditures, latitude, longitude, geom_point, geocoding_source` |
| `pub78_eligible` | Pub 78 deductibility list | `ein, org_name, city, state, deductibility_status` |
| `revoked_organizations` | Auto-revoked orgs | `ein, org_name, revocation_date, reinstatement_date` |
| `census_demographics` | ACS census data | `geoid, geo_type, year, total_population, median_household_income, poverty_count, white_count, black_count, hispanic_count, bachelors_count, housing_units, median_housing_value, source_file` |

**Views (irs_ng):**

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `v_org_financial_profile` | Org financial profile | `ein, org_name, years_filed, avg_revenue, revenue_trend, avg_expenses` |
| `v_org_multi_year` | Multi-year financials | `ein, org_name, multi_year_revenue, multi_year_expenses` |
| `v_political_orgs` | Political orgs summary | `ein, org_name, city, state, total_contributions, total_expenditures` |

### Congress-Legislators (`us_project_cl`)

The `legislators` table contains static biographical data. Party, state, district, chamber, and dates are in `legislator_terms`.

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `legislators` | Biographical info | `bioguide_id, first_name, last_name, middle_name, nickname, suffix, official_full, birthday, gender, is_current, first_term_start, last_term_end, thomas_id, govtrack_id, opensecrets_id, votesmart_id, wikipedia_page, ballotpedia_page, cspan_id, fec_ids, google_entity_id, house_history_id, icpsr_id, lis_id, maplight_id, wikidata_id, bioguide_previous` |
| `legislator_terms` | Terms of service | `term_id, bioguide_id, state, district, party, term_type, term_start, term_end, congress_start, congress_end, class, state_rank, how, end_type, address, office, phone, fax, contact_form, url, rss_url` |
| `committee_membership` | Committee assignments | `membership_id, bioguide_id, committee_thomas_id, legislator_name, rank, title, party` |
| `committees` | Committee definitions | `committee_thomas_id, committee_name, chamber, jurisdiction, house_committee_id, senate_committee_id, committee_type, url, minority_url, address, phone, rss_url, youtube_id, congresses, is_current` |
| `subcommittees` | Subcommittee definitions | `subcommittee_thomas_id, subcommittee_name, parent_committee` |
| `district_offices` | Local offices | `bioguide_id, office_key, city, state, address, suite, building, zip, phone, fax, hours, latitude, longitude, geom_point` |
| `legislator_social_media` | Social media accounts | `bioguide_id, twitter, twitter_id, facebook, facebook_id, youtube, youtube_id, instagram, instagram_id` |
| `legislator_other_names` | Alternate/former names | `bioguide_id, name, name_type` |
| `executives` | Executive branch officials | `bioguide_id, first_name, middle_name, last_name, suffix, birthday, gender, govtrack_id, icpsr_prez_id` |
| `executive_terms` | Executive terms of office | `term_id, bioguide_id, term_type, start_date, end_date, party, how` |

### Congressional Districts (`ucla_polysci_cdmaps`)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `congressional_districts` | District boundaries | `id, statename, district, congress_number, geom, county, district_id, startcong, endcong, statefp, bestdec, fromcounty, page, note, finalnote, law, source_file` |

## Views Guide

Views are created for expensive cross-table aggregations. ETL pipelines keep them current automatically.

### View: `v_org_financial_profile`

**Database:** irs_ng
**Purpose:** Multi-year financial profile per nonprofit.

```bash
GET /ngopen/irs_ng/v_org_financial_profile?select=*&ein=eq.123456789
```

### View: `v_org_multi_year`

**Database:** irs_ng
**Purpose:** Multi-year financial aggregation.

```bash
GET /ngopen/irs_ng/v_org_multi_year?select=*&ein=eq.123456789
```

### View: `v_political_orgs`

**Database:** irs_ng
**Purpose:** Political organization spending summary.

```bash
GET /ngopen/irs_ng/v_political_orgs?select=*&order=total_expenditures.desc&limit=100
```

## Spatial RPC Functions

Functions for geographic queries. Use POST with JSON body.

### `rpc_find_district`

Find congressional district for a lat/lng point.

**Endpoint:** `/ngopen/up_cdmaps/rpc/rpc_find_district`

```bash
POST /ngopen/up_cdmaps/rpc/rpc_find_district
{"lat": 34.0522, "lng": -118.2437, "congress": 118}
```

Returns: `{id, statename, district, congress_number, geom, county}`

### `rpc_districts_in_bbox`

Find all districts within a bounding box.

**Endpoint:** `/ngopen/up_cdmaps/rpc/rpc_districts_in_bbox`

```bash
POST /ngopen/up_cdmaps/rpc/rpc_districts_in_bbox
{"min_lat": 33.5, "min_lng": -118.5, "max_lat": 34.5, "max_lng": -117.5, "congress": 118}
```

### `rpc_nonprofits_nearby`

Find nonprofits within a radius (km) of a point.

**Endpoint:** `/ngopen/irs_ng/rpc/rpc_nonprofits_nearby`

```bash
POST /ngopen/irs_ng/rpc/rpc_nonprofits_nearby
{"lat": 34.0522, "lng": -118.2437, "radius_km": 25}
```

Returns: `[ein, org_name_current, city, state, distance_km, total_revenue, ntee_irs]`

### `rpc_nonprofits_in_district`

Find all nonprofits within a congressional district.

**Endpoint:** `/ngopen/irs_ng/rpc/rpc_nonprofits_in_district`

```bash
POST /ngopen/irs_ng/rpc/rpc_nonprofits_in_district
{"state": "CA", "district": 34, "congress": 118}
```

## Investigative Playbooks

### A. Follow the Grant Money

**Goal:** Trace federal grant funding from agency to subrecipient.

```
1. Find grants by agency or keyword
   GET /ngopen/usaspending/financial_accounts_by_awards?select=fain,obligations_incurred_total_by_award_cpe,treasury_appropriation_account(toptier_agency(name))&fain=not.is.null&obligations_incurred_total_by_award_cpe=gt.10000000&order=obligations_incurred_total_by_award_cpe.desc&limit=10

2. Get recipient entity details via UEI crosswalk
   GET /ngopen/usaspending/uei_crosswalk?select=*&uei=eq.A1B2C3D4E5F6

3. Find subawards under this prime award
   GET /ngopen/usaspending/subawards?select=*&parent_award_id=eq.12345

4. Cross-reference subrecipients with SAM.gov registration
   GET /ngopen/samer/sam_registrations?select=*&uei=eq.A1B2C3D4E5F6

5. Check if subrecipient is a registered nonprofit
   GET /ngopen/irs_ng/bmf_organizations?select=ein,org_name_current,ntee_irs&org_name_current=ilike.*recipient*

6. Get entity award totals
   GET /ngopen/usaspending/entity_awards?select=*&uei=eq.A1B2C3D4E5F6
```

### B. Contractor Intelligence

**Goal:** Build profile of federal contractor.

```
1. Find all contracts for entity
   GET /ngopen/usaspending/prime_awards?select=*&recipient_uei=eq.A1B2C3D4E5F6&award_type=eq.contract

2. Get NAICS/PSC code definitions
   GET /ngopen/usaspending/naics?code=in.(541511,541512)
   GET /ngopen/usaspending/psc?code=ilike.*D307*

3. Check SAM.gov registration status
   GET /ngopen/samer/sam_registrations?select=*&uei=eq.A1B2C3D4E5F6

4. Find subcontractors
   GET /ngopen/usaspending/subawards?select=subaward_id,subaward_amount,subrecipient_name,subrecipient_uei&prime_recipient_uei=eq.A1B2C3D4E5F6

5. Get budget authority for relevant agency
   GET /ngopen/usaspending/budget_authority?select=*&agency_identifier=eq.097&order=year.desc
```

### C. Nonprofit Deep Dive

**Goal:** Comprehensive financial and operational profile of a nonprofit.

```
1. Get BMF registration
   GET /ngopen/irs_ng/bmf_organizations?select=*&ein=eq.123456789

2. Get SOI filing data
   GET /ngopen/irs_ng/form990_soi?select=*&ein=eq.123456789&order=tax_year.desc

3. Get financial profile view
   GET /ngopen/irs_ng/v_org_financial_profile?select=*&ein=eq.123456789

4. Check for unrelated business income (990-T)
   GET /ngopen/irs_ng/form990t_details?select=*&ein=eq.123456789

5. Check if also registered as 527 political org
   GET /ngopen/irs_ng/political_orgs_527?select=*&ein=eq.123456789

6. Check Pub 78 deductibility status
   GET /ngopen/irs_ng/pub78_eligible?select=*&ein=eq.123456789

7. Check revocation status
   GET /ngopen/irs_ng/revoked_organizations?select=*&ein=eq.123456789

8. Find government contracts/grants received
   GET /ngopen/usaspending/prime_awards?select=*&recipient_name=ilike.*org*name*&award_amount=gt.100000

9. Find nearby nonprofits (potential related entities)
   POST /ngopen/irs_ng/rpc/rpc_nonprofits_nearby
   {"lat": 34.0522, "lng": -118.2437, "radius_km": 10}
```

### D. Subcontractor Chain Analysis

**Goal:** Map subcontracting networks from prime to tier-N.

```
1. Start with prime award
   GET /ngopen/usaspending/subawards?select=*&parent_award_id=eq.12345

2. For each subaward, check if it's also a prime recipient elsewhere
   GET /ngopen/usaspending/prime_awards?select=*&recipient_uei=eq.SUBRECIPIENT_UEI

3. Recursively find sub-tier awards
   GET /ngopen/usaspending/subawards?select=subaward_id,subaward_amount,subrecipient_uei,subrecipient_name,prime_awards(prime_recipient_uei)&prime_recipient_uei=eq.SUBRECIPIENT_UEI

4. Build chain visualization data
   # Combine results into tree structure:
   # Prime → Sub1 → Sub1.1 → Sub1.1.1
   #              → Sub1.2
   #        → Sub2

5. Check each entity in chain for SAM registration
   GET /ngopen/samer/sam_registrations?select=uei,legal_business_name,is_current,registration_expiration&uei=in.(UEI1,UEI2,UEI3)
```

### E. District Spending Analysis

**Goal:** Analyze federal spending in a congressional district.

```
1. Get district boundary
   GET /ngopen/up_cdmaps/congressional_districts?select=*&statename=eq.California&district=eq.34&congress_number=eq.118

2. Find top recipients in district area (bounding box approximation)
   GET /ngopen/usaspending/recipient_geocode_index?select=*&and=(latitude.gte.34.0,latitude.lte.34.2,longitude.gte.-118.3,longitude.lte.-118.1)&latitude=not.is.null&limit=50

3. Get representative info (find bioguide_id first)
   GET /ngopen/usp_cl/legislator_terms?select=bioguide_id,state,district,party,term_start,term_end,legislators(first_name,last_name,official_full)&state=eq.CA&district=eq.34&term_end=gte.2026-01-01

4. Get representative's committee assignments (use bioguide_id from step 3)
   GET /ngopen/usp_cl/committee_membership?select=*&bioguide_id=eq.X000001&order=rank

5. Compare spending across districts (client-side aggregation)
   GET /ngopen/usaspending/prime_awards?select=pop_state,pop_congressional_district,award_amount&pop_state=not.is.null&limit=10000
   # Aggregate client-side: group by pop_state + pop_congressional_district, sum award_amount
   # Note: pop_congressional_district is just the number string (e.g., "11"), not "CA-11"
```

### F. Committee Power Mapping

**Goal:** Map committee influence over spending.

```
1. Get committee definition and jurisdiction
   GET /ngopen/usp_cl/committees?select=*&committee_thomas_id=eq.HSIF

2. Get current committee members
   GET /ngopen/usp_cl/committee_membership?select=*&committee_thomas_id=eq.HSIF&order=rank

3. For each member, get their district info (use bioguide_id from step 2)
   GET /ngopen/usp_cl/legislator_terms?select=*&bioguide_id=eq.X000001&term_end=gte.2026-01-01

4. Find spending in agencies under committee jurisdiction
   GET /ngopen/usaspending/budget_authority?select=*&agency_identifier=eq.097&order=year.desc

5. Identify top contractors in relevant agencies (client-side aggregation)
   GET /ngopen/usaspending/prime_awards?select=recipient_name,award_amount&awarding_agency=ilike.*energy*&limit=10000
   # Aggregate client-side: group by recipient_name, sum award_amount
```

### G. Revoked Org Red Flags

**Goal:** Identify nonprofits with revoked tax-exempt status.

```
1. Find revoked organizations
   GET /ngopen/irs_ng/revoked_organizations?select=*&revocation_date=gte.2023-01-01&limit=100

2. Get last known financial data
   GET /ngopen/irs_ng/form990_soi?select=*&ein=eq.123456789&order=tax_year.desc&limit=1

3. Check if still receiving federal funds
   GET /ngopen/usaspending/prime_awards?select=*&recipient_name=ilike.*org*name*&action_date=gt.2023-01-01

4. Check for related entities (same city/state)
   GET /ngopen/irs_ng/bmf_organizations?select=ein,org_name_current&f990_org_addr_city=eq.SAME_CITY&f990_org_addr_state=eq.SAME_STATE

5. Check SAM.gov for entity registration
   GET /ngopen/samer/sam_registrations?select=*&legal_business_name=ilike.*org*name*
```

### H. Geographic Hotspot Detection

**Goal:** Find geographic clusters of spending or nonprofits.

```
1. Get all awards in a state (use and=() for bounding box)
   GET /ngopen/usaspending/recipient_geocode_index?select=*&and=(latitude.gte.25.8,latitude.lte.36.5,longitude.gte.-106.6,longitude.lte.-93.5)&latitude=not.is.null&limit=1000

2. Find nonprofit density by state (fetch rows, count client-side)
   GET /ngopen/irs_ng/bmf_organizations?select=f990_org_addr_state&is_current=is.true&limit=5000
   # Count occurrences of each state client-side

3. Spatial query: nonprofits near large awards
   POST /ngopen/irs_ng/rpc/rpc_nonprofits_nearby
   {"lat": 30.2672, "lng": -97.7431, "radius_km": 50}

4. Cross-reference with district demographics
   GET /ngopen/up_cdmaps/congressional_districts?select=*&statename=eq.Texas&congress_number=eq.118
```

### I. 527 Political Organization Analysis

**Goal:** Track political spending by 527 organizations.

```
1. Get all 527 organizations
   GET /ngopen/irs_ng/political_orgs_527?select=*&order=total_expenditures.desc&limit=100

2. Get political orgs view (aggregated)
   GET /ngopen/irs_ng/v_political_orgs?select=*&order=total_expenditures.desc&limit=100

3. Find 527s also registered as nonprofits
   GET /ngopen/irs_ng/political_orgs_527?select=ein&status=eq.active
   # Cross-reference each EIN with bmf_organizations
   GET /ngopen/irs_ng/bmf_organizations?select=ein,org_name_current&ein=in.(EIN1,EIN2,...)

4. Geographic distribution (fetch rows, aggregate client-side)
   GET /ngopen/irs_ng/political_orgs_527?select=state,total_expenditures&limit=5000
   # Group by state and sum total_expenditures client-side
```

### J. Census-Contextualized Need

**Goal:** Compare federal spending with community need indicators.

```
1. Get demographics for a census tract
   GET /ngopen/irs_ng/census_demographics?select=*&geoid=eq.36061000100&geo_type=eq.tract&year=eq.2022

2. Get nonprofits in that area (use and=() for bounding box)
   GET /ngopen/irs_ng/bmf_organizations?select=ein,org_name_current,ntee_irs&and=(latitude.gte.40.7,latitude.lte.40.8,longitude.gte.-74.0,longitude.lte.-73.9)&is_current=is.true&latitude=not.is.null&limit=50

3. Get federal spending in area
   GET /ngopen/usaspending/recipient_geocode_index?select=*&and=(latitude.gte.40.7,latitude.lte.40.8,longitude.gte.-74.0,longitude.lte.-73.9)&latitude=not.is.null&limit=100

4. Compare with district-level data
   GET /ngopen/up_cdmaps/congressional_districts?select=*&statename=eq.New+York&congress_number=eq.118
```

## Red Flag Detection Patterns

### Financial Anomalies

```bash
# Revenue spikes - compare year-over-year in form990_soi
GET /ngopen/irs_ng/form990_soi?select=ein,tax_year,total_revenue&ein=eq.123456789&order=tax_year.desc

# Large unrelated business income (potential commercial activity)
GET /ngopen/irs_ng/form990t_details?select=*&unrelated_business_income=gt.1000000&order=unrelated_business_income.desc

# Nonprofit with Schedule O narratives (look for explanations)
GET /ngopen/irs_ng/form990_schedule_o?select=*&ein=eq.123456789&order=tax_year.desc
```

### Entity Anomalies

```bash
# Expired SAM registration still receiving awards
GET /ngopen/samer/sam_registrations?select=uei,registration_expiration&uei=eq.XXX&registration_expiration=lt.2024-01-01
GET /ngopen/usaspending/prime_awards?select=*&recipient_uei=eq.XXX&action_date=gt.2024-01-01

# Multiple entities at same address (potential shell companies)
GET /ngopen/samer/sam_registrations?select=uei,legal_business_name,physical_city,physical_state&physical_city=eq.CITY&physical_state=eq.ST
```

### Geographic Anomalies

```bash
# Awards to entities in high-risk jurisdictions
GET /ngopen/usaspending/prime_awards?select=*&recipient_country=not.eq.USA&award_amount=gt.1000000

# Concentration: single entity getting majority of district funding (client-side aggregation)
GET /ngopen/usaspending/prime_awards?select=recipient_name,award_amount&pop_state=eq.TX&limit=10000
# Group by recipient_name and sum award_amount client-side
```

### Subcontracting Anomalies

```bash
# Subaward > prime award (data error or pass-through scheme)
GET /ngopen/usaspending/subawards?select=subaward_id,subaward_amount,subrecipient_name,prime_award_amount&subaward_amount=gt.1000000&order=subaward_amount.desc

# Circular subcontracting (A→B→A)
GET /ngopen/usaspending/subawards?select=subaward_id,subrecipient_uei,subrecipient_name&prime_recipient_uei=eq.XXX
GET /ngopen/usaspending/prime_awards?select=*&recipient_uei=eq.SUBRECIPIENT_UEI
```

### Political Activity

```bash
# 527 org with nonprofit status (dual-status red flag)
GET /ngopen/irs_ng/political_orgs_527?select=ein&status=eq.active
# Cross-reference each EIN with bmf_organizations
GET /ngopen/irs_ng/bmf_organizations?select=ein,org_name_current&ein=in.(EIN1,EIN2,...)

# Revoked org still active
GET /ngopen/irs_ng/revoked_organizations?select=*&reinstatement_date=is.null
```

## Performance Best Practices

### Table Size Warnings

| Table | Approximate Size | Notes |
|-------|-----------------|-------|
| `financial_accounts_by_awards` | ~820M+ rows | Will timeout without filters. Always filter by `fain`, `piid`, or `treasury_appropriation_account` |
| `prime_awards` | ~50M+ rows | Needs filters. Use `recipient_uei`, `action_date`, `awarding_agency`, or `pop_state` |
| `bmf_organizations` | ~1.2M rows | Ordering by revenue without filters is slow. Filter by `ein`, `state`, or `is_current` first |
| `subawards` | ~40M+ rows | Filter by `parent_award_id`, `prime_recipient_uei`, or `fiscal_year` |
| `form990_soi` | ~2M+ rows | Filter by `ein` or `tax_year` |

### Query Optimization

1. **Always use indexed columns for filters**: `uei`, `ein`, `award_id`, `entity_id`, `action_date`, `state`, `district`
2. **Limit result sets**: Use `limit=100` even when you expect fewer results
3. **Select only needed columns**: `select=col1,col2` instead of `select=*`
4. **Use views** for aggregations instead of computing on the fly
5. **Use spatial RPC functions** instead of manual ST_Contains queries
6. **Paginate with offset** or cursor-based pagination for large result sets
7. **Use `and=()` for range queries** on the same column (e.g., bounding boxes)
8. **No server-side GROUP BY**: PostgREST does not support `group=` parameter. Fetch rows and aggregate client-side, or use pre-computed views.

### Index-Aware Querying

The following columns have B-tree indexes - prefer these for filtering:

- `usaspending_db`: `uei`, `duns`, `award_id`, `action_date`, `awarding_agency`, `recipient_name`, `award_type`, `piid`, `fain`, `recipient_uei`, `pop_state`
- `sam_er`: `uei`, `legal_business_name`, `is_current`, `registration_expiration`
- `irs_ng`: `ein`, `org_name_current`, `f990_org_addr_state`, `f990_org_addr_city`, `tax_year`, `ntee_irs`
- `us_project_cl`: `bioguide_id`, `state`, `district`, `committee_thomas_id`
- `ucla_polysci_cdmaps`: `statename`, `district`, `congress_number`

### When to Use Each Database

| Question | Start With | Then Join |
|----------|-----------|-----------|
| Who got federal money? | usaspending | samer (entity details), irs_ng (nonprofit status) |
| Is this entity legitimate? | samer | usaspending (award history), irs_ng (tax status) |
| How is this nonprofit doing? | irs_ng | usaspending (gov revenue), up_cdmaps (district context) |
| What's happening in this district? | up_cdmaps | usaspending (spending), irs_ng (nonprofits), usp_cl (rep) |
| Who represents this area? | usp_cl | up_cdmaps (district data), usaspending (spending in district) |

## Common Pitfalls

1. **UEI vs DUNS**: Pre-2022 awards use DUNS, post-2022 use UEI. Use `uei_crosswalk` to match across the transition.
2. **Name matching is unreliable**: Always prefer UEI/EIN/DUNS over name matching. When names are the only option, normalize case and strip punctuation.
3. **Action date vs fiscal year**: `action_date` is a `YYYY-MM-DD` string; `fiscal_year` is an integer. They may differ for multi-year awards.
4. **Subaward amounts don't sum to prime**: Subawards may not cover the full prime award value (some funds retained by prime).
5. **Nonprofit EIN ≠ UEI**: No direct link between IRS and SAM databases. Cross-reference by name + location.
6. **527 organizations are NOT nonprofits**: They are political organizations. Do not confuse with 501(c)(3) status.
7. **District boundaries change**: Redistricting occurs every 10 years. Always specify `congress_number` parameter for district queries.
8. **Views are ETL-managed**: Views are refreshed by data import pipelines and are always current.
9. **Spatial queries require PostGIS**: Use the RPC functions rather than raw SQL geometry operations.
10. **PostgREST returns arrays for embedded joins**: When embedding `table(cols)`, the result is an array even for 1:1 relationships.
11. **Null vs missing**: PostgREST distinguishes `null` values from missing fields. Use `col=is.null` to find nulls.
12. **Table names in URLs**: Use exact table names from OpenAPI spec (e.g., `sam_registrations` not `entity`, `political_orgs_527` not `f527_orgs`, `congressional_districts` not `districts`).
13. **Embedding syntax uses parentheses**: Use `table(col1,col2)` not `table{col1,col2}`.
14. **Range queries need `and=()`**: `latitude=gte.34.0&latitude=lte.34.2` is invalid (second overwrites first). Use `and=(latitude.gte.34.0,latitude.lte.34.2)`.
15. **Legislator party/state/district are in `legislator_terms`**: The `legislators` table only has biographical data (`first_name`, `last_name`, `official_full`, `birthday`, etc.).
16. **`committee_membership` has no `committee_name`**: Only `committee_thomas_id`. Join to `committees` table for names, or use `legislator_name` which is denormalized.
17. **Huge tables will timeout**: `financial_accounts_by_awards` (~820M rows) and `prime_awards` (~50M rows) require filters. Always include at least one selective filter.
18. **No server-side GROUP BY**: PostgREST does not support `group=` query parameter. Aggregate client-side or use materialized views.
19. **`pop_congressional_district` is just the number**: Stored as `"11"` not `"CA-11"`. Combine with `pop_state` for full district ID.
20. **`executives` uses `bioguide_id` not `name`**: Query by `bioguide_id`, `first_name`, `last_name` — not by `name` or `title`. Executive terms are in `executive_terms` with `bioguide_id`, `term_type`, `party`, `how`.
