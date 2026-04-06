---
title: "Docs"
---
### https://benthic.io/ngopen/irs_ng/
This database provides geocoded versions of IRS Exempt Organizations Business Master File, Form 990/990-EZ/990-PF SOI financials, Publication 78 deductibility eligibility, auto-revocation list, Form 990-N e-Postcard, Form 990 XML filings with Schedule O narratives and Schedule R flags, Section 527 political organizations, and ACS census demographics.
## Tables

### bmf_organizations

Core table. One row per exempt organization from the IRS Business Master File (BMF), merged across monthly NCCS archive releases. Geocoded via Photon API.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | Employer Identification Number |
| `org_name_current` | text | Current organization name |
| `org_name_sec` | text | Secondary/sort name |
| `ntee_irs` | varchar(10) | NTEE code (IRS version) |
| `nccs_level_1` | varchar(100) | NTEE major group name (e.g. "Education") |
| `bmf_subsection_code` | varchar(10) | IRC subsection (e.g. `03` = 501(c)(3)) |
| `bmf_status_code` | varchar(10) | IRS status code |
| `bmf_foundation_code` | varchar(10) | Foundation classification code |
| `bmf_deductibility_code` | varchar(10) | Deductibility contribution code |
| `f990_org_addr_street` | text | Street address |
| `f990_org_addr_city` | varchar(100) | City |
| `f990_org_addr_state` | varchar(10) | State abbreviation |
| `f990_org_addr_zip` | varchar(20) | ZIP code |
| `org_addr_full` | text | Full concatenated address |
| `latitude` | decimal(10,8) | Geocoded latitude |
| `longitude` | decimal(11,8) | Geocoded longitude |
| `geocoder_score` | decimal(5,2) | Photon geocoder confidence score |
| `geocoder_match` | varchar(100) | Geocoder matched location name |
| `geocoding_source` | varchar(50) | `photon_api`, `photon_failed`, or null |
| `geom_point` | geometry(Point, 4326) | PostGIS point geometry (auto-populated from lat/lon) |
| `f990_total_revenue_recent` | bigint | Most recent revenue from BMF |
| `f990_total_income_recent` | bigint | Most recent income from BMF |
| `f990_total_assets_recent` | bigint | Most recent assets from BMF |
| `org_ruling_date` | varchar(20) | IRS ruling date |
| `org_ruling_year` | varchar(10) | IRS ruling year |
| `bmf_affiliation_code` | varchar(10) | Affiliation code |
| `bmf_classification_code` | varchar(10) | Classification code |
| `bmf_organization_code` | varchar(10) | Organization type code |
| `bmf_group_exempt_num` | varchar(50) | Group exemption number |
| `is_current` | boolean | TRUE for the latest BMF version of this EIN+name |
| `imported_at` | timestamp | When this row was last updated |

**Indexes:** `ein`, `is_current`, `f990_org_addr_state`, `ntee_irs`, geocoded/not-geocoded partial indexes.

#### Example queries

```bash
# Find organizations in California with 501(c)(3) status
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?f990_org_addr_state=eq.CA&bmf_subsection_code=eq.03&is_current=is.true&limit=10"

# Search by EIN
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?ein=eq.123456789"

# Get geocoded orgs in a bounding box
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?latitude=gte.40.0&latitude=lte.41.0&longitude=gte.-74.0&longitude=lte.-73.0&latitude=not.is.null&limit=100"

# Select only specific columns
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?select=ein,org_name_current,f990_org_addr_state,latitude,longitude&is_current=is.true&limit=50"

# Filter by NTEE major group letter
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?ntee_irs=like.E*&is_current=is.true&limit=20"

# Count organizations per state
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?select=f990_org_addr_state,count&is_current=is.true&groupby=f990_org_addr_state"
```

### bmf_organization_snapshots

Historical monthly snapshots of BMF data. Each row represents an organization's record from a specific BMF release date. Allows tracking changes over time (name changes, status changes, address moves, revenue shifts).

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `release_date` | date | BMF archive release date (YYYY-MM-01) |
| `release_source` | varchar(255) | Source filename |
| `org_name` | varchar(500) | Organization name at that release |
| `bmf_status_code` | varchar(10) | Status code at that release |
| `bmf_subsection_code` | varchar(10) | IRC subsection |
| `ntee_irs` | varchar(10) | NTEE code |
| `f990_org_addr_city` | varchar(100) | City |
| `f990_org_addr_state` | varchar(10) | State |
| `f990_org_addr_street` | text | Street address |
| `f990_org_addr_zip` | varchar(20) | ZIP |
| `f990_total_revenue` | bigint | Revenue |
| `f990_total_income` | bigint | Income |
| `f990_total_assets` | bigint | Assets |
| `org_ruling_date` | varchar(20) | Ruling date |
| `org_year_first` | varchar(10) | First year on file |
| `org_year_last` | varchar(10) | Last year on file |

**Unique key:** `(ein, release_date, release_source)`

#### Example queries

```bash
# Get all snapshots for an EIN (shows history)
curl "https://benthic.io/ngopen/irs_ng/bmf_organization_snapshots?ein=eq.123456789&order=release_date"

# Get BMF releases for a specific month
curl "https://benthic.io/ngopen/irs_ng/bmf_organization_snapshots?release_date=eq.2024-01-01&limit=50"
```

### form990_soi

Per-EIN annual financial data from IRS Statistics of Income (SOI) extracts. Covers Form 990 and Form 990-EZ filers. One row per EIN per tax year.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `tax_year` | integer | Tax year |
| `form_type` | varchar(10) | `990` or `990ez` |
| `subseccd` | varchar(5) | IRC subsection code |
| `is_501c3` | boolean | TRUE if 501(c)(3) |
| `total_revenue` | bigint | Total revenue |
| `total_expenses` | bigint | Total functional expenses |
| `total_assets` | bigint | Total assets (EOY) |
| `total_liabilities` | bigint | Total liabilities (EOY) |
| `net_assets` | bigint | Net assets |
| `contributions` | bigint | Contributions and grants received |
| `grants_paid` | bigint | Grants paid |
| `compensation_officers` | bigint | Officer compensation |
| `total_program_revenue` | bigint | Program service revenue |
| `investment_income` | bigint | Investment income |
| `royalty_income` | bigint | Royalty income |
| `net_rental_income` | bigint | Net rental income |
| `net_gains_losses` | bigint | Net gains/losses from sale of assets |
| `fundraising_income` | bigint | Gross fundraising income |
| `gaming_income` | bigint | Gross gaming income |
| `tax_exempt_interest` | bigint | Tax-exempt bond interest |
| `legal_fees` | bigint | Legal fees |
| `accounting_fees` | bigint | Accounting fees |
| `professional_fundraising` | bigint | Professional fundraising fees |
| `management_fees` | bigint | Management fees |
| `investment_mgmt_fees` | bigint | Investment management fees |
| `advertising` | bigint | Advertising expense |
| `office_expenses` | bigint | Office expenses |
| `occupancy` | bigint | Occupancy/rent |
| `travel` | bigint | Travel |
| `insurance` | bigint | Insurance |
| `depreciation` | bigint | Depreciation |
| `interest_expense` | bigint | Interest expense |
| `other_salaries_wages` | bigint | Other salaries/wages |
| `pension_contributions` | bigint | Pension plan contributions |
| `employee_benefits` | bigint | Employee benefits |
| `payroll_taxes` | bigint | Payroll taxes |
| `total_reportable_comp` | bigint | Total reportable compensation |
| `total_estimated_comp` | bigint | Total estimated compensation |
| `individuals_over_100k` | integer | Count of individuals compensated >$100k |
| `land_buildings_equipment` | bigint | Land, buildings, equipment (EOY) |
| `investments_end` | bigint | Investments (EOY) |
| `cash_end` | bigint | Cash (EOY) |
| `num_employees` | integer | Number of employees |
| `num_orgs` | integer | Number of organizations (group returns) |
| `total_support` | bigint | Total support |
| `non_pf_reason` | varchar(5) | Reason not a private foundation |
| `filed_990t` | boolean | Filed Form 990-T (UBIT) |
| `unrelated_business_income` | boolean | Has unrelated business income |
| `foreign_offices` | boolean | Has foreign offices |
| `political_activities` | boolean | Political campaign activities |
| `lobbying_activities` | boolean | Lobbying activities |
| `operates_hospital` | boolean | Operates a hospital |
| `donor_advised_funds` | boolean | Maintains donor-advised funds |
| `asset_size` | varchar | Asset size category |
| `ntee_code` | varchar | NTEE classification code |
| `org_name` | varchar | Organization name |
| `state` | varchar | State abbreviation |
| `revenue_less_expenses` | bigint | Revenue minus expenses |
| `total_programs` | bigint | Total program count |

**Unique key:** `(ein, tax_year)`

#### Example queries

```bash
# Get financials for a specific EIN across years
curl "https://benthic.io/ngopen/irs_ng/form990_soi?ein=eq.123456789&order=tax_year"

# Largest organizations by revenue in 2022
curl "https://benthic.io/ngopen/irs_ng/form990_soi?select=ein,total_revenue,total_expenses,total_assets&tax_year=eq.2022&order=total_revenue.desc&limit=25"

# 501(c)(3) organizations with lobbying activities
curl "https://benthic.io/ngopen/irs_ng/form990_soi?is_501c3=is.true&lobbying_activities=is.true&tax_year=eq.2022&limit=50"

# Organizations by NTEE code
curl "https://benthic.io/ngopen/irs_ng/form990_soi?ntee_code=eq.E&tax_year=eq.2022&select=ein,org_name,ntee_code,total_revenue&order=total_revenue.desc&limit=25"

# Filter by state and asset size
curl "https://benthic.io/ngopen/irs_ng/form990_soi?state=eq.CA&asset_size=eq.L&tax_year=eq.2022&select=ein,org_name,total_revenue,total_expenses&order=total_revenue.desc&limit=25"
```

### form990_soi_private_foundation

Per-EIN annual financial data for private foundations from IRS SOI extracts (Form 990-PF). One row per EIN per tax year.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `tax_year` | integer | Tax year |
| `tax_period` | varchar(6) | Tax period (YYYYMM) |
| `operating_cd` | varchar(5) | Operating foundation code |
| `is_operating` | boolean | TRUE if operating foundation |
| `fair_market_value` | bigint | Fair market value of all assets |
| `gross_contributions` | bigint | Gross contributions received |
| `interest_revenue` | bigint | Interest revenue |
| `dividends` | bigint | Dividends |
| `gross_rents` | bigint | Gross rents |
| `total_receipts_books` | bigint | Total receipts per books |
| `compensation_officers` | bigint | Officer compensation |
| `total_expenses_books` | bigint | Total expenses per books |
| `contributions_paid` | bigint | Contributions, gifts, grants paid |
| `net_investment_income` | bigint | Net investment income |
| `total_assets` | bigint | Total assets (EOY) |
| `total_liabilities` | bigint | Total liabilities |
| `fund_net_worth` | bigint | Fund balance/net worth |
| `distributions` | bigint | Qualifying distributions |
| `undistributed_income` | bigint | Undistributed income |
| `minimum_investment_return` | bigint | Minimum investment return |
| `grants_approved_future` | bigint | Grants approved for future payment |
| `excise_tax` | bigint | Excise tax on investment income |

**Unique key:** `(ein, tax_year)`

### form990_details

Parsed data from IRS Form 990 XML filings. Includes Schedule R flags indicating organizational complexity.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `tax_period` | varchar(10) | Tax period (YYYYMM) |
| `form_type` | varchar(10) | `990`, `990EZ`, or `990PF` |
| `filing_date` | date | Date filed |
| `total_revenue` | bigint | Total revenue |
| `contributions_received` | bigint | Contributions received |
| `program_service_revenue` | bigint | Program service revenue |
| `total_expenses` | bigint | Total expenses |
| `grants_paid` | bigint | Grants paid |
| `total_assets` | bigint | Total assets |
| `total_liabilities` | bigint | Total liabilities |
| `net_assets` | bigint | Net assets |
| `has_disregarded_entity` | boolean | Schedule R: has disregarded entity |
| `has_related_entity` | boolean | Schedule R: has related entity |
| `has_related_org_control` | boolean | Schedule R: related org controls entity |
| `has_transfer_to_noncharitable` | boolean | Schedule R: transfer to non-charitable related org |
| `has_partnership_activity` | boolean | Schedule R: partnership activities |
| `xml_path` | varchar(500) | Path to source XML file |

**Unique key:** `(ein, tax_period)`

#### Example queries

```bash
# Filings with complex organizational structures (Schedule R flags)
curl "https://benthic.io/ngopen/irs_ng/form990_details?has_related_entity=is.true&has_disregarded_entity=is.true&limit=50"

# Recent filings for an EIN
curl "https://benthic.io/ngopen/irs_ng/form990_details?ein=eq.123456789&order=tax_period.desc"
```

### form990t_details

Unrelated Business Income Tax (UBIT) data parsed from IRS Form 990-T XML filings. Organizations with unrelated business income must file this form. Useful for identifying nonprofits engaged in commercial activities.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `ein` | varchar(20) | EIN |
| `tax_period` | varchar(10) | Tax period (YYYYMM) |
| `filing_date` | date | Date filed |
| `organization_501c_type` | varchar(10) | 501(c) subsection type |
| `book_value_assets_eoy` | bigint | Book value of assets at end of year |
| `total_ubti_computed` | bigint | Total unrelated business taxable income (computed) |
| `total_ubti` | bigint | Total unrelated business taxable income |
| `taxable_corporation` | bigint | Taxable corporation indicator |
| `total_tax_computation` | bigint | Total tax computation |
| `total_tax` | bigint | Total tax due |
| `estimated_tax_payments` | bigint | Estimated tax payments |
| `specific_deduction` | bigint | Specific deduction |
| `total_deduction` | bigint | Total deduction |
| `charitable_contributions_ded` | bigint | Charitable contributions deduction |
| `capital_gain_net_income` | bigint | Net capital gain income |
| `total_ordinary_gain_loss` | bigint | Total ordinary gain/loss |
| `total_prtshp_scorp_income` | bigint | Total partnership/S-corp income |
| `other_income` | bigint | Other income |
| `interest_deduction` | bigint | Interest deduction |
| `other_deductions` | bigint | Other deductions |
| `total_deductions` | bigint | Total deductions |
| `unrelated_bus_income` | bigint | Unrelated business income |
| `principal_business_activity_cd` | varchar(10) | Principal business activity code |
| `trade_or_business_desc` | text | Trade or business description |
| `source_file` | varchar(500) | Source filename |
| `xml_path` | varchar(500) | Path to source XML file |
| `imported_at` | timestamp | Import timestamp |

**Unique key:** `(ein, tax_period)`

#### Example queries

```bash
# Organizations with high UBIT
curl "https://benthic.io/ngopen/irs_ng/form990t_details?total_ubti=gt.1000000&select=ein,tax_period,total_ubti,total_tax,trade_or_business_desc&order=total_ubti.desc&limit=25"

# Find nonprofits engaged in specific business activities
curl "https://benthic.io/ngopen/irs_ng/form990t_details?trade_or_business_desc=ilike.*real%20estate*&select=ein,tax_period,trade_or_business_desc,total_ubti&limit=25"

# Organizations with large estimated tax payments
curl "https://benthic.io/ngopen/irs_ng/form990t_details?estimated_tax_payments=gt.100000&select=ein,estimated_tax_payments,total_tax&order=estimated_tax_payments.desc&limit=25"
```

### form990_schedule_o

Narrative text from Form 990 Schedule O (Supplemental Information). Contains program accomplishments, governance descriptions, and other supplemental disclosures.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `tax_period` | varchar(6) | Tax period (YYYYMM) |
| `form_type` | varchar(10) | Form type |
| `program_accomplishments` | text | Program accomplishments narrative |
| `governance_text` | text | Governance descriptions |
| `supplemental_info` | text | Other supplemental information |

**Unique key:** `(ein, tax_period, form_type)`

### form990_xml_import_log

Tracks XML filing import jobs. Records when Form 990/990-T/Schedule O XML files were processed and how many records were imported.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `zip_filename` | varchar | Source ZIP filename |
| `xml_count` | integer | Number of XML files in source |
| `records_imported` | integer | Total records imported |
| `records_990` | integer | Form 990 records imported |
| `records_990t` | integer | Form 990-T records imported |
| `schedule_o_count` | integer | Schedule O records imported |
| `import_started_at` | timestamp | Import job start time |
| `import_completed_at` | timestamp | Import job completion time |
| `import_status` | varchar | Job status |
| `notes` | text | Import notes/errors |

### pub78_eligible

Organizations eligible to receive tax-deductible charitable contributions (IRS Publication 78).

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN (unique) |
| `org_name` | varchar(500) | Organization name |
| `city` | varchar(100) | City |
| `state` | varchar(10) | State |
| `is_deductible` | boolean | Eligible for deductible contributions |

#### Example queries

```bash
# Check if an org is Pub78 eligible
curl "https://benthic.io/ngopen/irs_ng/pub78_eligible?ein=eq.123456789"

# Search by name
curl "https://benthic.io/ngopen/irs_ng/pub78_eligible?org_name=ilike.*red%20cross*&limit=20"
```

### revoked_organizations

Organizations whose federal tax-exempt status has been automatically revoked by the IRS (typically for failure to file for 3 consecutive years).

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN (unique) |
| `org_name` | varchar(500) | Organization name |
| `revocation_date` | date | Date of revocation |
| `revocation_reason` | varchar(255) | Reason for revocation |

#### Example queries

```bash
# Check if an org was revoked
curl "https://benthic.io/ngopen/irs_ng/revoked_organizations?ein=eq.123456789"

# Revoked in a date range
curl "https://benthic.io/ngopen/irs_ng/revoked_organizations?revocation_date=gte.2024-01-01&revocation_date=lte.2024-12-31&limit=100"
```

### form990n_small_orgs

Small tax-exempt organizations filing Form 990-N (e-Postcard). These are organizations with gross receipts normally $50,000 or less.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN (unique) |
| `org_name` | varchar(500) | Organization name |
| `tax_period` | varchar(20) | Most recent tax period |
| `website` | varchar(500) | Organization website |


### political_orgs_527

Political organizations registered under IRC Section 527, from IRS Form 8871 filings.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `org_name` | varchar(500) | Organization name |
| `filing_type` | varchar(10) | Filing type (e.g. `8871`) |
| `org_type` | varchar(200) | Organization type description |
| `address` | varchar(500) | Mailing address |
| `city` | varchar(100) | City |
| `state` | varchar(10) | State |
| `zip` | varchar(20) | ZIP code |
| `filing_date` | date | Date of filing |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `geocoding_source` | varchar(50) | Geocoding source |

**Unique key:** `(ein, filing_type)`

#### Example queries

```bash
# All 527 orgs in a state
curl "https://benthic.io/ngopen/irs_ng/political_orgs_527?state=eq.TX&limit=50"

# Geocoded 527 orgs
curl "https://benthic.io/ngopen/irs_ng/political_orgs_527?latitude=not.is.null&limit=100"
```

### census_demographics

ACS 5-year estimates for census tracts and counties (2009-2024). Useful for contextualizing nonprofit locations with socioeconomic data.

| Column | Type | Description |
|---|---|---|
| `geoid` | varchar(20) | Census GEOID (11-digit for tracts, 5-digit for counties) |
| `geo_type` | varchar(10) | `tract` or `county` |
| `year` | integer | ACS survey year |
| `total_population` | integer | Total population |
| `median_household_income` | integer | Median household income |
| `poverty_count` | integer | Population below poverty line |
| `white_count` | integer | White alone population |
| `black_count` | integer | Black or African American alone population |
| `hispanic_count` | integer | Hispanic or Latino population |
| `bachelors_count` | integer | Bachelor's degree or higher (2012+) |
| `housing_units` | integer | Total housing units |
| `median_housing_value` | integer | Median housing value (owner-occupied) |

**Unique key:** `(geoid, year, geo_type)`

#### Example queries

```bash
# Get demographics for a specific tract
curl "https://benthic.io/ngopen/irs_ng/census_demographics?geoid=eq.06075010100&geo_type=eq.tract&year=eq.2022"

# Counties with highest median income
curl "https://benthic.io/ngopen/irs_ng/census_demographics?select=geoid,total_population,median_household_income&geo_type=eq.county&year=eq.2022&order=median_household_income.desc&limit=20"
```

## Views

### v_org_financial_profile

Joins `bmf_organizations` (current records only) with `form990_soi` to provide a combined organizational + financial profile. Left join means BMF organizations appear even without SOI data.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `org_name_current` | text | Current organization name |
| `f990_org_addr_state` | varchar(10) | State |
| `ntee_irs` | varchar(10) | NTEE code |
| `bmf_subsection_code` | varchar(10) | IRC subsection |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `tax_year` | integer | Tax year |
| `form_type` | varchar(10) | Form type |
| `total_revenue` | bigint | Total revenue |
| `total_expenses` | bigint | Total expenses |
| `total_assets` | bigint | Total assets |
| `contributions` | bigint | Contributions received |
| `compensation_officers` | bigint | Officer compensation |
| `grants_paid` | bigint | Grants paid |
| `investment_income` | bigint | Investment income |
| `total_program_revenue` | bigint | Program service revenue |
| `num_employees` | integer | Number of employees |
| `filed_990t` | boolean | Filed Form 990-T |
| `unrelated_business_income` | boolean | Has unrelated business income |

```bash
# Get combined profile for an EIN
curl "https://benthic.io/ngopen/irs_ng/v_org_financial_profile?ein=eq.123456789"

# Top revenue organizations with location data
curl "https://benthic.io/ngopen/irs_ng/v_org_financial_profile?select=ein,org_name_current,f990_org_addr_state,total_revenue,latitude,longitude&total_revenue=gt.10000000&order=total_revenue.desc&limit=25"

# 501(c)(3) organizations with UBIT filings
curl "https://benthic.io/ngopen/irs_ng/v_org_financial_profile?bmf_subsection_code=eq.03&filed_990t=is.true&select=ein,org_name_current,total_revenue,total_expenses&order=total_revenue.desc&limit=25"
```

### v_org_multi_year

Financial trends for organizations with 2+ years of SOI data. Includes computed `net_income` (revenue - expenses) and `margin_pct` (net income as percentage of revenue).

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `tax_year` | integer | Tax year |
| `total_revenue` | bigint | Total revenue |
| `total_expenses` | bigint | Total expenses |
| `total_assets` | bigint | Total assets |
| `net_income` | bigint | Computed: revenue - expenses |
| `margin_pct` | numeric | Computed: net income / revenue * 100 |
| `contributions` | bigint | Contributions received |
| `grants_paid` | bigint | Grants paid |
| `compensation_officers` | bigint | Officer compensation |

```bash
# Multi-year trend for an EIN
curl "https://benthic.io/ngopen/irs_ng/v_org_multi_year?ein=eq.123456789&order=tax_year"

# Organizations with declining revenue (negative net income)
curl "https://benthic.io/ngopen/irs_ng/v_org_multi_year?net_income=lt.0&select=ein,tax_year,total_revenue,total_expenses,net_income,margin_pct&order=net_income&limit=25"

# Highest margin organizations
curl "https://benthic.io/ngopen/irs_ng/v_org_multi_year?select=ein,tax_year,total_revenue,net_income,margin_pct&margin_pct=gt.50&order=margin_pct.desc&limit=25"
```

### v_political_orgs

Joins `political_orgs_527` with `bmf_organizations` to show 527 political organizations alongside any BMF records with the same EIN. Useful for identifying nonprofits that also operate as political organizations.

| Column | Type | Description |
|---|---|---|
| `ein` | varchar(20) | EIN |
| `political_name` | varchar(500) | 527 organization name |
| `filing_type` | varchar(10) | Filing type |
| `org_type` | varchar(200) | Organization type description |
| `city` | varchar(100) | City |
| `state` | varchar(10) | State |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `bmf_name` | text | BMF organization name (if matched) |
| `bmf_state` | varchar(10) | BMF state (if matched) |

```bash
# All 527 orgs with BMF matches
curl "https://benthic.io/ngopen/irs_ng/v_political_orgs?bmf_name=not.is.null&select=ein,political_name,bmf_name,state"

# 527 orgs in a state
curl "https://benthic.io/ngopen/irs_ng/v_political_orgs?state=eq.FL&select=ein,political_name,org_type,latitude,longitude&limit=50"
```

## PostgREST Query Reference

### Filtering

| Operator | Syntax | Example |
|---|---|---|
| Equals | `?col=value` | `?f990_org_addr_state=eq.CA` |
| Not equal | `?col=neq.value` | `?bmf_subsection_code=neq.03` |
| Greater than | `?col=gt.value` | `?total_revenue=gt.1000000` |
| Less than | `?col=lt.value` | `?tax_year=lt.2022` |
| Greater/eq | `?col=gte.value` | `?latitude=gte.40.0` |
| Less/eq | `?col=lte.value` | `?latitude=lte.41.0` |
| LIKE | `?col=like.PATTERN` | `?org_name_current=like.*Foundation*` |
| ILIKE | `?col=ilike.PATTERN` | `?org_name=ilike.%25red%20cross%25` |
| IS null | `?col=is.null` | `?latitude=is.null` |
| IS NOT null | `?col=not.is.null` | `?latitude=not.is.null` |
| IN | `?col=in.(val1,val2)` | `?f990_org_addr_state=in.(CA,NY,TX)` |

### Selecting columns

```
?select=ein,org_name_current,latitude,longitude
```

### Ordering

```
?order=total_revenue.desc
?order=tax_year.asc,ein.asc
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
?select=f990_org_addr_state,count&groupby=f990_org_addr_state
```

## Joining Tables (Embedding)

PostgREST supports resource embedding via foreign key relationships. Use the `select` parameter with embedded resource notation:

```bash
# Get an org from BMF with its SOI financials embedded
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?select=ein,org_name_current,form990_soi(tax_year,total_revenue,total_expenses)&ein=eq.123456789"

# Get SOI data with BMF org name
curl "https://benthic.io/ngopen/irs_ng/form990_soi?select=tax_year,total_revenue,bmf_organizations(org_name_current)&ein=eq.123456789"

# Get an org with its revocation status
curl "https://benthic.io/ngopen/irs_ng/bmf_organizations?select=ein,org_name_current,revoked_organizations(revocation_date)&ein=eq.123456789"
```

## Key Relationships

All tables link via **EIN** (Employer Identification Number). Join patterns:

- `bmf_organizations.ein` = primary organization identifier
- `form990_soi.ein` = annual financial data (one row per year)
- `form990_soi_private_foundation.ein` = foundation financials (one row per year)
- `form990_details.ein` = XML filing details (one row per period)
- `form990_schedule_o.ein` = narrative text
- `pub78_eligible.ein` = deductibility status
- `revoked_organizations.ein` = revocation status
- `form990n_small_orgs.ein` = small org filings
- `political_orgs_527.ein` = 527 political orgs
- `bmf_organization_snapshots.ein` = historical BMF snapshots

Cross-dataset: `census_demographics.geoid` can be derived from address components (state+county+tract FIPS codes).

## Data Sources

| Source | Description | Update frequency |
|---|---|---|
| IRS BMF (via NCCS) | Exempt Organization Business Master File | Monthly |
| IRS SOI | Statistics of Income per-EIN extracts | Annual |
| IRS Pub 78 | Deductibility eligibility list | Periodic |
| IRS Auto-Revocation | Revoked tax-exempt organizations | Periodic |
| IRS Form 990-N | e-Postcard for small organizations | Periodic |
| IRS Form 990 XML | Full XML filings (990, 990-EZ, 990-PF) | Rolling |
| IRS Form 8871 | 527 political organization registrations | Periodic |
| Census ACS | American Community Survey 5-year estimates | Annual |

All data originates from publicly available U.S. government sources.

## NTEE Code Reference

NTEE (National Taxonomy of Exempt Entities) codes classify organizations by purpose. The first letter indicates the major group:

| Code | Category |
|---|---|
| A | Arts, Culture, and Humanities |
| B | Education |
| C | Environmental Quality, Protection, and Beautification |
| D | Animal-Related |
| E | Health |
| F | Mental Health and Crisis Intervention |
| G | Diseases, Disorders, and Disciplines |
| H | Medical Research |
| I | Crime and Legal-Related |
| J | Employment |
| K | Food, Agriculture, and Nutrition |
| L | Housing and Shelter |
| M | Public Safety |
| N | Recreation and Sports |
| O | Youth Development |
| P | Human Services |
| Q | International, Foreign Affairs, and National Security |
| R | Civil Rights, Social Action, and Advocacy |
| S | Community Improvement and Capacity Building |
| T | Philanthropy, Voluntarism, and Grantmaking Foundations |
| U | Science and Technology Research Institutes |
| V | Social Science Research Institutes |
| W | Public and Societal Benefit |
| X | Religion-Related |
| Y | Mutual and Membership Benefit |
| Z | Unknown, Unclassified |

Use `bmf_organizations.ntee_irs` to filter by code or `bmf_organizations.nccs_level_1` to filter by the descriptive name.

## Common IRC Subsection Codes

| Code | Meaning |
|---|---|
| 01 | 501(c)(1) — Corporations organized under Act of Congress |
| 02 | 501(c)(2) — Title-holding corporations |
| 03 | 501(c)(3) — Charitable, religious, educational, scientific |
| 04 | 501(c)(4) — Social welfare organizations |
| 05 | 501(c)(5) — Labor, agricultural, horticultural organizations |
| 06 | 501(c)(6) — Business leagues, chambers of commerce |
| 07 | 501(c)(7) — Social and recreational clubs |
| 08 | 501(c)(8) — Fraternal beneficiary societies |
| 09 | 501(c)(9) — Voluntary employees' beneficiary associations |
| 10 | 501(c)(10) — Domestic fraternal societies |
| 11 | 501(c)(11) — Teachers' retirement fund associations |
| 12 | 501(c)(12) — Benevolent life insurance associations |
| 13 | 501(c)(13) — Cemetery companies |
| 14 | 501(c)(14) — State-chartered credit unions |
| 15 | 501(c)(15) — Mutual insurance companies |
| 17 | 501(c)(17) — Supplemental unemployment benefit trusts |
| 18 | 501(c)(18) — Employee funded pension trusts |
| 19 | 501(c)(19) — Veterans organizations |
| 21 | 501(c)(21) — Black lung benefit trusts |
| 22 | 501(c)(22) — Withdrawal liability payment fund |
| 23 | 501(c)(23) — Pre-1880 veterans organizations |
| 25 | 501(c)(25) — Title-holding corporations or trusts |
| 26 | 501(c)(26) — State-sponsored high risk health insurance |
| 27 | 501(c)(27) — State-sponsored workers' comp reinsurance |
| 29 | 501(c)(29) — CO-OP health insurance issuers |
| 40 | 501(d) — Religious and apostolic organizations |
| 50 | 501(e) — Cooperative hospital service organizations |
| 60 | 501(f) — Cooperative service organizations of operating educational orgs |
| 70 | 501(k) — Child care organizations |
| 71 | 501(n) — Charitable risk pools |
| 81 | 501(c)(1) — Instrumentality of US (state) |
| 92 | 4947(a)(1) — Nonexempt charitable trusts |
