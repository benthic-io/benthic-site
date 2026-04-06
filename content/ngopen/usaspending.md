---
title: "USASpending"
---

## https://benthic.io/ngopen/usaspending/

The core theme of this database is awards/transactions, financial accounts, agencies, appropriations, references (CFDA programs, NAICS/PSC codes), and reporting overviews for federal contract, grant, and loan recipients.

## Spending Tables

### financial_accounts_by_awards

Award-level spending data linked to Treasury Accounts. This is the central fact table connecting federal financial data to individual awards (contracts, grants, loans, etc.). Each row represents a financial transaction record for a specific award.

| Column | Type | Description |
|---|---|---|
| `financial_accounts_by_awards_id` | integer | Primary key |
| `submission_id` | integer | FK to submission_attributes |
| `treasury_account_id` | integer | FK to treasury_appropriation_account |
| `object_class_id` | integer | FK to object_class |
| `program_activity_id` | integer | FK to ref_program_activity |
| `award_id` | integer | Award ID (internal) |
| `distinct_award_key` | text | Unique award identifier key |
| `program_activity_reporting_key` | text | Program activity reporting key |
| `disaster_emergency_fund_code` | text | Disaster/emergency fund code (e.g. L = CARES Act) |
| `piid` | text | Procurement Instrument Identifier (contracts) |
| `parent_award_id` | text | Parent award PIID |
| `fain` | text | Federal Award Identification Number (grants) |
| `uri` | text | Unique Record Identifier |
| `prior_year_adjustment` | text | Prior year adjustment indicator |
| `obligations_delivered_orders_unpaid_total_cpe` | numeric | Obligations for delivered orders unpaid (CPE) |
| `obligations_delivered_orders_unpaid_total_fyb` | numeric | Obligations for delivered orders unpaid (FYB) |
| `obligations_undelivered_orders_unpaid_total_cpe` | numeric | Obligations for undelivered orders unpaid (CPE) |
| `obligations_undelivered_orders_unpaid_total_fyb` | numeric | Obligations for undelivered orders unpaid (FYB) |
| `obligations_incurred_total_by_award_cpe` | numeric | Total obligations incurred by award (CPE) |
| `gross_outlay_amount_by_award_cpe` | numeric | Gross outlay amount by award (CPE) |
| `gross_outlay_amount_by_award_fyb` | numeric | Gross outlay amount by award (FYB) |
| `gross_outlays_delivered_orders_paid_total_cpe` | numeric | Gross outlays for delivered orders paid (CPE) |
| `gross_outlays_delivered_orders_paid_total_fyb` | numeric | Gross outlays for delivered orders paid (FYB) |
| `gross_outlays_undelivered_orders_prepaid_total_cpe` | numeric | Gross outlays for undelivered orders prepaid (CPE) |
| `gross_outlays_undelivered_orders_prepaid_total_fyb` | numeric | Gross outlays for undelivered orders prepaid (FYB) |
| `transaction_obligated_amount` | numeric | Transaction obligated amount |
| `reporting_period_start` | date | Reporting period start |
| `reporting_period_end` | date | Reporting period end |
| `certified_date` | date | Certification date |
| `last_modified_date` | date | Last modified date |
| `drv_obligations_incurred_total_by_award` | numeric | Derived obligations incurred |
| `drv_award_id_field_type` | text | Derived award ID field type |
| `data_source` | text | Data source indicator |
| `deobligations_recoveries_refunds_of_prior_year_by_award_cpe` | numeric | Prior year deobligations/recoveries |
| `ussgl480100_undelivered_orders_obligations_unpaid_cpe` | numeric | USSGL 4801.00 (CPE) |
| `ussgl490100_delivered_orders_obligations_unpaid_cpe` | numeric | USSGL 4901.00 (CPE) |
| `ussgl490200_delivered_orders_obligations_paid_cpe` | numeric | USSGL 4902.00 (CPE) |
| `create_date` | timestamp | Record creation time |
| `update_date` | timestamp | Record update time |

**Note:** This table contains 60+ USSGL (U.S. Government Standard General Ledger) account columns. Use `?select=` to retrieve only the columns you need.

### Example queries

```bash
# Get recent award transactions for a FAIN (grant)
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?fain=eq.12345&select=financial_accounts_by_awards_id,fain,obligations_incurred_total_by_award_cpe,gross_outlay_amount_by_award_cpe,reporting_period_end&order=reporting_period_end.desc&limit=25"

# Get recent award transactions for a PIID (contract)
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?piid=eq.ABC123&select=financial_accounts_by_awards_id,piid,obligations_incurred_total_by_award_cpe,gross_outlay_amount_by_award_cpe&order=reporting_period_end.desc&limit=25"

# Get awards with CARES Act funding
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?disaster_emergency_fund_code=eq.L&select=piid,fain,obligations_incurred_total_by_award_cpe,reporting_period_end&limit=25"

# Get awards for a specific treasury account
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?treasury_account_id=eq.12345&select=piid,fain,obligations_incurred_total_by_award_cpe,gross_outlay_amount_by_award_cpe&order=obligations_incurred_total_by_award_cpe.desc&limit=50"

# Large obligations
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?obligations_incurred_total_by_award_cpe=gte.100000000&select=piid,fain,obligations_incurred_total_by_award_cpe,reporting_period_end&order=obligations_incurred_total_by_award_cpe.desc&limit=25"
```
&nbsp;

### financial_accounts_by_program_activity_object_class

Spending by program activity and object class within Treasury Accounts. This is the "Schedule B" level detail showing how money is spent by function and category.

| Column | Type | Description |
|---|---|---|
| `financial_accounts_by_program_activity_object_class_id` | integer | Primary key |
| `submission_id` | integer | FK to submission_attributes |
| `treasury_account_id` | integer | FK to treasury_appropriation_account |
| `object_class_id` | integer | FK to object_class |
| `program_activity_id` | integer | FK to ref_program_activity |
| `program_activity_reporting_key` | text | Program activity reporting key |
| `disaster_emergency_fund_code` | text | Disaster/emergency fund code |
| `obligations_delivered_orders_unpaid_total_cpe` | numeric | Delivered orders unpaid |
| `obligations_undelivered_orders_unpaid_total_cpe` | numeric | Undelivered orders unpaid |
| `obligations_incurred_by_program_object_class_cpe` | numeric | Obligations incurred |
| `gross_outlay_amount_by_program_object_class_cpe` | numeric | Gross outlays |
| `deobligations_recoveries_refund_pri_program_object_class_cpe` | numeric | Deobligations/recoveries |
| `reporting_period_start` | date | Reporting period start |
| `reporting_period_end` | date | Reporting period end |
| `certified_date` | date | Certification date |
| `last_modified_date` | date | Last modified date |
| `create_date` | timestamp | Record creation time |
| `update_date` | timestamp | Record update time |

### Example queries

```bash
# Get spending by program for a treasury account
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_program_activity_object_class?treasury_account_id=eq.12345&select=obligations_incurred_by_program_object_class_cpe,gross_outlay_amount_by_program_object_class_cpe,program_activity_id&order=obligations_incurred_by_program_object_class_cpe.desc&limit=25"
```
&nbsp;


### appropriation_account_balances

Treasury Account-level budget authority and obligation balances (Schedule A). Each row represents a Treasury Account's financial position for a reporting period.

| Column | Type | Description |
|---|---|---|
| `appropriation_account_balances_id` | integer | Primary key |
| `treasury_account_identifier` | integer | FK to treasury_appropriation_account |
| `submission_id` | integer | FK to submission_attributes |
| `adjustments_to_unobligated_balance_brought_forward_cpe` | numeric | Adjustments to unobligated balance brought forward |
| `borrowing_authority_amount_total_cpe` | numeric | Borrowing authority |
| `budget_authority_appropriated_amount_cpe` | numeric | Budget authority appropriated |
| `budget_authority_unobligated_balance_brought_forward_fyb` | numeric | Unobligated balance brought forward |
| `contract_authority_amount_total_cpe` | numeric | Contract authority |
| `deobligations_recoveries_refunds_by_tas_cpe` | numeric | Deobligations/recoveries/refunds |
| `gross_outlay_amount_by_tas_cpe` | numeric | Gross outlays |
| `obligations_incurred_total_by_tas_cpe` | numeric | Total obligations incurred |
| `other_budgetary_resources_amount_cpe` | numeric | Other budgetary resources |
| `spending_authority_from_offsetting_collections_amount_cpe` | numeric | Spending authority from offsetting collections |
| `status_of_budgetary_resources_total_cpe` | numeric | Total status of budgetary resources |
| `total_budgetary_resources_amount_cpe` | numeric | Total budgetary resources |
| `unobligated_balance_cpe` | numeric | Unobligated balance |
| `final_of_fy` | boolean | Final submission of fiscal year |
| `reporting_period_start` | date | Reporting period start |
| `reporting_period_end` | date | Reporting period end |
| `certified_date` | date | Certification date |
| `create_date` | timestamp | Record creation time |
| `update_date` | timestamp | Record update time |

### Example queries

```bash
# Get balances for a treasury account
curl "https://benthic.io/ngopen/usaspending/appropriation_account_balances?treasury_account_identifier=eq.12345&select=budget_authority_appropriated_amount_cpe,obligations_incurred_total_by_tas_cpe,gross_outlay_amount_by_tas_cpe,unobligated_balance_cpe,reporting_period_end&order=reporting_period_end.desc&limit=25"

# Get final balances for a fiscal year
curl "https://benthic.io/ngopen/usaspending/appropriation_account_balances?final_of_fy=is.true&select=treasury_account_identifier,budget_authority_appropriated_amount_cpe,obligations_incurred_total_by_tas_cpe,gross_outlay_amount_by_tas_cpe&limit=50"
```
&nbsp;

### historical_appropriation_account_balances

Historical Treasury Account-level budget data predating DABS submissions.

| Column | Type | Description |
|---|---|---|
| `historical_appropriation_account_balances_id` | integer | Primary key |
| `agency_id` | text | Agency identifier |
| `main_account_code` | text | Main account code |
| `sub_account_code` | text | Sub-account code |
| `account_title` | text | Account title |
| `obligations_incurred_total_by_tas_cpe` | numeric | Total obligations |
| `deobligations_recoveries_refunds_by_tas_cpe` | numeric | Deobligations |
| `gross_outlay_amount_by_tas_cpe` | numeric | Gross outlays |
| `total_budgetary_resources_amount_cpe` | numeric | Total budgetary resources |
| `budget_function_code` | text | Budget function code |
| `budget_subfunction_code` | text | Budget sub-function code |
| `fr_entity_code` | text | FR entity code |
| `owning_toptier_agency_id` | integer | FK to toptier_agency |
| `reporting_fiscal_year` | integer | Fiscal year |
| `reporting_fiscal_quarter` | integer | Fiscal quarter |
| `reporting_fiscal_period` | integer | Fiscal period |
| `tas_rendering_label` | text | TAS rendering label |


## Agency and Account Reference Tables

### toptier_agency

Top-level federal agencies (e.g. Department of Defense, Department of Health and Human Services).

| Column | Type | Description |
|---|---|---|
| `toptier_agency_id` | integer | Primary key |
| `toptier_code` | text | CGAC/FREC agency code |
| `name` | text | Agency name |
| `abbreviation` | text | Agency abbreviation |
| `mission` | text | Mission statement |
| `website` | varchar(200) | Agency website |

### subtier_agency

Sub-tier agencies within top-tier agencies (e.g. U.S. Army under DoD).

| Column | Type | Description |
|---|---|---|
| `subtier_agency_id` | integer | Primary key |
| `subtier_code` | text | Sub-tier code |
| `name` | text | Sub-tier agency name |
| `abbreviation` | text | Abbreviation |

### agency

Links top-tier and sub-tier agencies.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `toptier_agency_id` | integer | FK to toptier_agency |
| `subtier_agency_id` | integer | FK to subtier_agency |
| `toptier_flag` | boolean | TRUE if this represents the top-tier agency |
| `user_selectable` | boolean | TRUE if user-selectable in USAspending |

### federal_account

Federal accounts that aggregate Treasury Accounts.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `account_title` | text | Account title |
| `agency_identifier` | text | Agency identifier |
| `main_account_code` | text | Main account code |
| `federal_account_code` | text | Federal account code (agency + main) |
| `parent_toptier_agency_id` | integer | FK to toptier_agency |

### treasury_appropriation_account

Individual Treasury Accounts (TAS). The most granular budget account level.

| Column | Type | Description |
|---|---|---|
| `treasury_account_identifier` | integer | Primary key |
| `agency_id` | text | Agency identifier |
| `main_account_code` | text | Main account code |
| `sub_account_code` | text | Sub-account code |
| `account_title` | text | Account title |
| `reporting_agency_id` | text | Reporting agency ID |
| `reporting_agency_name` | text | Reporting agency name |
| `budget_function_code` | text | Budget function code |
| `budget_function_title` | text | Budget function title |
| `budget_subfunction_code` | text | Budget sub-function code |
| `budget_subfunction_title` | text | Budget sub-function title |
| `budget_bureau_code` | text | Bureau code |
| `budget_bureau_name` | text | Bureau name |
| `fr_entity_code` | text | FR entity code |
| `allocation_transfer_agency_id` | text | Allocation transfer agency |
| `availability_type_code` | text | Availability type code |
| `beginning_period_of_availability` | text | Beginning period of availability |
| `ending_period_of_availability` | text | Ending period of availability |
| `federal_account_id` | integer | FK to federal_account |
| `funding_toptier_agency_id` | integer | FK to toptier_agency (funding) |
| `awarding_toptier_agency_id` | integer | FK to toptier_agency (awarding) |
| `tas_rendering_label` | text | TAS display label |

#### Example queries

```bash
# Get treasury accounts for an agency
curl "https://benthic.io/ngopen/usaspending/treasury_appropriation_account?funding_toptier_agency_id=eq.123&select=treasury_account_identifier,account_title,tas_rendering_label,budget_function_title&limit=50"

# Look up a TAS by label
curl "https://benthic.io/ngopen/usaspending/treasury_appropriation_account?tas_rendering_label=eq.075-0512&select=account_title,funding_toptier_agency_id,budget_function_title"
```
&nbsp;

## Classification Reference Tables

### cgac

Common Government-wide Accounting Classification (CGAC) agency codes.

| Column | Type | Description |
|---|---|---|
| `cgac_code` | text | Primary key. CGAC code |
| `agency_name` | text | Agency name |
| `agency_abbreviation` | text | Abbreviation |
| `is_frec_agency` | boolean | TRUE if using FRAC code instead |

### frec

Federal Reserve Entity Codes (FREC) — alternative agency codes.

| Column | Type | Description |
|---|---|---|
| `frec_code` | text | Primary key |
| `agency_name` | text | Agency name |
| `agency_abbreviation` | text | Abbreviation |
| `associated_cgac_code` | text | Associated CGAC code |

### naics

North American Industry Classification System codes.

| Column | Type | Description |
|---|---|---|
| `code` | text | Primary key. NAICS code |
| `description` | text | Short description |
| `long_description` | text | Full description |
| `year` | integer | NAICS edition year |
| `year_retired` | integer | Year retired (if applicable) |

### psc

Product and Service Codes used in federal procurement.

| Column | Type | Description |
|---|---|---|
| `code` | varchar(4) | Primary key. PSC code |
| `description` | text | Short description |
| `length` | integer | Code length |
| `start_date` | date | Effective start date |
| `end_date` | date | Effective end date |
| `full_name` | text | Full name |
| `includes` | text | What this code includes |
| `excludes` | text | What this code excludes |
| `notes` | text | Additional notes |

### object_class

Budget object class definitions (how money is spent).

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `major_object_class` | text | Major object class code |
| `major_object_class_name` | text | Major object class name |
| `object_class` | text | Object class code |
| `object_class_name` | text | Object class name |
| `direct_reimbursable` | text | Direct/reimbursable indicator |
| `direct_reimbursable_name` | text | Direct/reimbursable name |

### ref_program_activity

Program activity definitions.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `program_activity_code` | text | Program activity code |
| `program_activity_name` | text | Program activity name |
| `budget_year` | text | Budget year |
| `responsible_agency_id` | text | Responsible agency |
| `main_account_code` | text | Main account code |

### references_cfda

Catalog of Federal Domestic Assistance (CFDA) program catalog.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `program_number` | text | CFDA program number |
| `program_title` | text | Program title |
| `popular_name` | text | Popular name |
| `federal_agency` | text | Federal agency |
| `authorization` | text | Authorizing legislation |
| `objectives` | text | Program objectives |
| `types_of_assistance` | text | Types of assistance |
| `uses_and_use_restrictions` | text | Uses and restrictions |
| `applicant_eligibility` | text | Applicant eligibility |
| `beneficiary_eligibility` | text | Beneficiary eligibility |
| `website_address` | text | Program website |
| `related_programs` | text | Related programs |

### award_category

Award type reference codes.

| Column | Type | Description |
|---|---|---|
| `type_code` | text | Primary key. Award type code |
| `type_name` | text | Award type name (e.g. "Direct Loan", "Grant", "Insurance") |

### disaster_emergency_fund_code

Disaster and emergency funding codes (e.g. CARES Act, Infrastructure Investment).

| Column | Type | Description |
|---|---|---|
| `code` | text | Primary key. Fund code (e.g. L, N, O, U) |
| `public_law` | text | Public law reference |
| `title` | text | Descriptive title |
| `group_name` | text | Group name (e.g. "covid_19") |
| `urls` | text | Reference URLs |
| `earliest_public_law_enactment_date` | date | Earliest enactment date |

### bureau_title_lookup

Maps federal account codes to bureau titles.

| Column | Type | Description |
|---|---|---|
| `federal_account_code` | text | Federal account code |
| `bureau_title` | text | Bureau title |
| `bureau_slug` | text | URL slug |

### program_activity_park

Program Activity/PARK code lookup.

| Column | Type | Description |
|---|---|---|
| `code` | text | Primary key |
| `name` | text | Program activity name |

&nbsp;

## Population and Geographic Reference

### state_data

State population and median household income.

| Column | Type | Description |
|---|---|---|
| `id` | text | Primary key |
| `fips` | text | State FIPS code |
| `code` | text | State abbreviation |
| `name` | text | State name |
| `type` | text | Type |
| `year` | integer | Data year |
| `population` | bigint | Population |
| `pop_source` | text | Population source |
| `median_household_income` | numeric | Median household income |
| `mhi_source` | text | MHI source |

### ref_country_code

Country code reference.

| Column | Type | Description |
|---|---|---|
| `country_code` | text | Primary key |
| `country_name` | text | Country name |
| `valid_code_indicator` | text | Valid code indicator |
| `latest_population` | bigint | Latest population |

### ref_population_county

County population data.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `state_code` | varchar(2) | State code |
| `state_name` | text | State name |
| `county_number` | varchar(3) | County number |
| `county_name` | text | County name |
| `latest_population` | integer | Latest population |

### ref_population_cong_district

Congressional district population data.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `state_code` | varchar(2) | State code |
| `congressional_district` | text | District number |
| `state_abbreviation` | varchar(2) | State abbreviation |
| `state_name` | text | State name |
| `latest_population` | integer | Latest population |

### ref_city_county_state_code

City/county/state code reference from USGS GNIS.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `feature_id` | integer | GNIS feature ID |
| `state_alpha` | text | State abbreviation |
| `county_name` | text | County name |
| `feature_name` | text | Feature name |
| `feature_class` | text | Feature class |
| `primary_latitude` | numeric | Latitude |
| `primary_longitude` | numeric | Longitude |

&nbsp;

## Submission and Reporting Tables

### submission_attributes

DABS (Data Act Broker Submission) attributes.

| Column | Type | Description |
|---|---|---|
| `submission_id` | integer | Primary key |
| `submission_window_id` | integer | FK to dabs_submission_window_schedule |
| `quarter_format_flag` | boolean | TRUE if quarterly submission |
| `reporting_agency_name` | text | Reporting agency name |
| `toptier_code` | text | Top-tier agency code |
| `reporting_fiscal_year` | integer | Fiscal year |
| `reporting_fiscal_quarter` | integer | Fiscal quarter |
| `reporting_fiscal_period` | integer | Fiscal period |
| `published_date` | timestamp | Published date |
| `certified_date` | timestamp | Certified date |

### dabs_submission_window_schedule

DABS submission window schedule.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `submission_fiscal_year` | integer | Fiscal year |
| `submission_fiscal_quarter` | integer | Fiscal quarter |
| `submission_fiscal_month` | integer | Fiscal month |
| `period_start_date` | timestamp | Period start |
| `period_end_date` | timestamp | Period end |
| `submission_due_date` | timestamp | Submission due date |
| `certification_due_date` | timestamp | Certification due date |
| `is_quarter` | boolean | TRUE if quarterly window |

### reporting_agency_overview

Agency-level reporting summary.

| Column | Type | Description |
|---|---|---|
| `reporting_agency_overview_id` | integer | Primary key |
| `toptier_code` | text | Agency code |
| `fiscal_year` | integer | Fiscal year |
| `fiscal_period` | integer | Fiscal period |
| `total_budgetary_resources` | numeric | Total budgetary resources |
| `total_dollars_obligated_gtas` | numeric | Total obligated (GTAS) |
| `linked_procurement_awards` | integer | Linked procurement awards |
| `linked_assistance_awards` | integer | Linked assistance awards |
| `unlinked_procurement_c_awards` | integer | Unlinked procurement (C) |
| `unlinked_procurement_d_awards` | integer | Unlinked procurement (D) |
| `unlinked_assistance_c_awards` | integer | Unlinked assistance (C) |
| `unlinked_assistance_d_awards` | integer | Unlinked assistance (D) |

### reporting_agency_tas

TAS-level reporting discrepancies.

### reporting_agency_missing_tas

Missing TAS reporting records.

### gtas_sf133_balances

GTAS SF-133 Report on Budget Execution and Budgetary Resources.

### budget_authority

Budget authority by agency and year.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `agency_identifier` | text | Agency identifier |
| `year` | integer | Fiscal year |
| `amount` | bigint | Budget authority amount |
| `fr_entity_code` | text | FR entity code |

### overall_totals

Fiscal year overall totals.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `fiscal_year` | integer | Fiscal year |
| `total_budget_authority` | numeric | Total budget authority |
&nbsp;


## Other Tables

### recipient_geocode_index

Geocoded recipient coordinates. Links spending to geographic locations.

| Column | Type | Description |
|---|---|---|
| `source_id` | bigint | Primary key |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `geom_point` | geometry(Point, 4326) | PostGIS point geometry (GIST-indexed) |
| `geocode_date` | timestamp | Geocoding date |
| `geocode_system` | varchar(50) | Geocoding system |

**Index:** `idx_rgi_geom_point` (GIST on `geom_point` WHERE `geom_point IS NOT NULL`)

### historic_parent_duns

Historical DUNS parent company linkage.

| Column | Type | Description |
|---|---|---|
| `broker_historic_duns_id` | integer | Primary key |
| `awardee_or_recipient_uniqu` | text | DUNS number |
| `ultimate_parent_unique_ide` | text | Parent DUNS |
| `ultimate_parent_legal_enti` | text | Parent legal entity name |
| `legal_business_name` | text | Entity legal name |
| `year` | integer | Data year |

### uei_crosswalk / uei_crosswalk_2021

DUNS to UEI (Unique Entity Identifier) crosswalk tables.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `awardee_or_recipient_uniqu` | text | DUNS number |
| `uei` | text | UEI |

### office

Contract and financial assistance office lookup.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `agency_code` | text | Agency code |
| `sub_tier_code` | text | Sub-tier code |
| `office_code` | text | Office code |
| `office_name` | text | Office name |
| `contract_awards_office` | boolean | Contract awards office |
| `contract_funding_office` | boolean | Contract funding office |
| `financial_assistance_awards_office` | boolean | Financial assistance awards office |
| `financial_assistance_funding_office` | boolean | Financial assistance funding office |

### references_definition

Data Act term definitions.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `term` | text | Term |
| `data_act_term` | text | DATA Act term |
| `plain` | text | Plain language definition |
| `official` | text | Official definition |

### rosetta

Rosetta reference documents (JSON).

| Column | Type | Description |
|---|---|---|
| `document_name` | text | Primary key |
| `document` | jsonb | Document content |

&nbsp;

## Award and Entity Tables

### prime_awards

Denormalized prime award records combining contract, grant, and loan data with recipient information, amounts, dates, agencies, NAICS/PSC codes, and COVID tracking. One row per award.

| Column | Type | Description |
|---|---|---|
| `award_id` | bigint | Award ID |
| `unique_award_id` | text | Unique award identifier |
| `piid` | text | Procurement Instrument Identifier |
| `fain` | text | Federal Award Identification Number |
| `uri` | text | Unique Record Identifier |
| `display_award_id` | text | Display-friendly award ID |
| `category` | text | Award category (contracts, grants, loans, other) |
| `award_type` | text | Award type code |
| `type_description` | text | Award type description |
| `award_amount` | numeric | Total award amount |
| `total_obligation` | numeric | Total obligated amount |
| `total_outlays` | numeric | Total outlays |
| `action_date` | date | Action date |
| `fiscal_year` | integer | Fiscal year |
| `date_signed` | date | Date signed |
| `recipient_name` | text | Recipient legal name |
| `recipient_duns` | text | Recipient DUNS |
| `recipient_uei` | text | Recipient UEI |
| `recipient_state` | text | Recipient state |
| `recipient_city` | text | Recipient city |
| `recipient_country` | text | Recipient country |
| `pop_state` | text | Place of performance state |
| `pop_city` | text | Place of performance city |
| `pop_country` | text | Place of performance country |
| `awarding_agency` | text | Awarding agency name |
| `awarding_agency_code` | text | Awarding agency code |
| `awarding_subtier_agency` | text | Awarding sub-tier agency |
| `funding_agency` | text | Funding agency name |
| `funding_agency_code` | text | Funding agency code |
| `naics_code` | text | NAICS code |
| `naics_description` | text | NAICS description |
| `product_or_service_code` | text | PSC code |
| `product_or_service_description` | text | PSC description |
| `cfda_number` | text | CFDA program number |
| `cfda_program_title` | text | CFDA program title |
| `description` | text | Award description |
| `disaster_emergency_fund_codes` | text[] | DEFC codes (array) |
| `total_covid_obligation` | numeric | Total COVID obligations |
| `total_covid_outlay` | numeric | Total COVID outlays |

#### Example queries

```bash
# Top awards by obligation
curl "https://benthic.io/ngopen/usaspending/prime_awards?select=display_award_id,recipient_name,total_obligation,awarding_agency&order=total_obligation.desc&limit=25"

# COVID-related awards
curl "https://benthic.io/ngopen/usaspending/prime_awards?total_covid_obligation=gt.0&select=display_award_id,recipient_name,total_covid_obligation,awarding_agency&order=total_covid_obligation.desc&limit=25"

# Awards to a specific recipient
curl "https://benthic.io/ngopen/usaspending/prime_awards?recipient_name=ilike.*lockheed*&select=display_award_id,award_type,total_obligation,action_date&order=action_date.desc&limit=25"

# Awards by NAICS code
curl "https://benthic.io/ngopen/usaspending/prime_awards?naics_code=eq.541512&select=display_award_id,recipient_name,total_obligation,awarding_agency&order=total_obligation.desc&limit=25"
```

&nbsp;

### subawards

Subcontract and subgrant data. Follow the money down the supply chain — see which subcontractors receive federal funds under prime awards.

| Column | Type | Description |
|---|---|---|
| `subaward_id` | bigint | Primary key |
| `subaward_number` | text | Subaward number |
| `unique_award_key` | text | Unique award key |
| `prime_award_piid_fain` | text | Prime award PIID or FAIN |
| `subaward_type` | text | Subaward type (subcontract, subgrant) |
| `subaward_amount` | numeric | Subaward amount |
| `prime_award_amount` | numeric | Prime award amount |
| `sub_action_date` | date | Subaward action date |
| `fiscal_year` | text | Fiscal year |
| `sub_recipient_name` | text | Sub-recipient name |
| `sub_recipient_duns` | text | Sub-recipient DUNS |
| `sub_recipient_uei` | text | Sub-recipient UEI |
| `sub_state` | text | Sub-recipient state |
| `sub_city` | text | Sub-recipient city |
| `prime_recipient_name` | text | Prime recipient name |
| `prime_recipient_duns` | text | Prime recipient DUNS |
| `prime_recipient_uei` | text | Prime recipient UEI |
| `awarding_agency_name` | text | Awarding agency name |
| `funding_agency_name` | text | Funding agency name |
| `subaward_description` | text | Subaward description |
| `cfda_titles` | text | CFDA program titles |
| `sub_naics` | text | Sub-recipient NAICS |
| `pop_state` | text | Place of performance state |
| `pop_city` | text | Place of performance city |

#### Example queries

```bash
# Subawards for a prime recipient
curl "https://benthic.io/ngopen/usaspending/subawards?prime_recipient_name=ilike.*boeing*&select=subaward_number,sub_recipient_name,subaward_amount,sub_action_date&order=subaward_amount.desc&limit=25"

# Large subcontracts
curl "https://benthic.io/ngopen/usaspending/subawards?subaward_amount=gt.10000000&select=subaward_number,sub_recipient_name,subaward_amount,prime_recipient_name,awarding_agency_name&order=subaward_amount.desc&limit=25"

# Subgrants in a state
curl "https://benthic.io/ngopen/usaspending/subawards?sub_state=eq.TX&subaward_type=eq.subgrant&select=sub_recipient_name,subaward_amount,sub_action_date&order=subaward_amount.desc&limit=25"
```

&nbsp;

### all_entities

Entity registry with geocoded addresses, award aggregates, and geohash. Combines all recipients (contractors, grantees, loan recipients) into a single lookup.

| Column | Type | Description |
|---|---|---|
| `entity_id` | bigint | Primary key |
| `entity_type` | text | Entity type (recipient, sub-recipient, etc.) |
| `legal_business_name` | text | Legal business name |
| `duns` | text | DUNS number |
| `uei` | text | UEI |
| `parent_uei` | text | Parent UEI |
| `city` | text | City |
| `state` | text | State |
| `country_code` | text | Country code |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `geom_point` | geometry | PostGIS point geometry |
| `is_geocoded` | boolean | Has valid geocode |
| `geohash_6` | text | 6-character geohash |
| `award_count` | bigint | Total award count |
| `total_obligation` | numeric | Total obligated amount |
| `date_first_award` | date | First award date |
| `date_last_award` | date | Last award date |

#### Example queries

```bash
# Search entities by name
curl "https://benthic.io/ngopen/usaspending/all_entities?legal_business_name=ilike.*general%20dynamics*&select=entity_id,legal_business_name,uei,state,total_obligation&limit=25"

# Entities in a state with awards
curl "https://benthic.io/ngopen/usaspending/all_entities?state=eq.VA&total_obligation=gt.1000000&select=legal_business_name,uei,total_obligation,award_count&order=total_obligation.desc&limit=25"

# Geocoded entities near coordinates
curl "https://benthic.io/ngopen/usaspending/all_entities?latitude=gte.38.8&latitude=lte.39.0&longitude=gte.-77.1&longitude=lte.-76.9&is_geocoded=is.true&select=legal_business_name,latitude,longitude&limit=50"
```

&nbsp;

### entity_awards

Links entities to their individual awards with agency, amount, and classification data.

| Column | Type | Description |
|---|---|---|
| `entity_id` | bigint | Entity ID |
| `entity_name` | text | Entity name |
| `entity_uei` | text | Entity UEI |
| `entity_duns` | text | Entity DUNS |
| `entity_state` | text | Entity state |
| `award_id` | bigint | Award ID |
| `fiscal_year` | text | Fiscal year |
| `action_date` | date | Action date |
| `total_obligation` | numeric | Total obligation |
| `award_amount` | numeric | Award amount |
| `awarding_agency` | text | Awarding agency |
| `award_type` | text | Award type |
| `piid` | text | PIID (contracts) |
| `fain` | text | FAIN (grants) |
| `category` | text | Award category |
| `naics_code` | text | NAICS code |
| `description` | text | Award description |

#### Example queries

```bash
# All awards for an entity
curl "https://benthic.io/ngopen/usaspending/entity_awards?entity_uei=eq.ABCDEFGHIJK&select=award_id,award_type,total_obligation,awarding_agency,action_date&order=action_date.desc&limit=50"

# Awards by agency
curl "https://benthic.io/ngopen/usaspending/entity_awards?awarding_agency=ilike.*defense*&select=entity_name,award_type,total_obligation&order=total_obligation.desc&limit=25"
```

&nbsp;

### frec_map

Maps treasury appropriation accounts to FR (Federal Reserve) entity codes and sub-function codes.

| Column | Type | Description |
|---|---|---|
| `id` | integer | Primary key |
| `agency_identifier` | text | Agency identifier |
| `main_account_code` | text | Main account code |
| `treasury_appropriation_account_title` | text | TAS title |
| `sub_function_code` | text | Budget sub-function code |
| `fr_entity_code` | text | FR entity code |

&nbsp;

### zips_grouped

ZIP5 to state, county, and congressional district reference table.

| Column | Type | Description |
|---|---|---|
| `zips_grouped_id` | integer | Primary key |
| `zip5` | text | 5-digit ZIP code |
| `state_abbreviation` | text | State abbreviation |
| `county_number` | text | County FIPS number |
| `congressional_district_no` | text | Congressional district number |

#### Example queries

```bash
# Find congressional district for a ZIP
curl "https://benthic.io/ngopen/usaspending/zips_grouped?zip5=eq.10001&select=zip5,state_abbreviation,congressional_district_no"

# All ZIPs in a congressional district
curl "https://benthic.io/ngopen/usaspending/zips_grouped?congressional_district_no=eq.12&state_abbreviation=eq.NY&select=zip5,congressional_district_no&limit=50"
```

&nbsp;

### c_to_d_linkage_updates

Tracks C/D (contract to DUNS) linkage updates between financial accounts and awards.

| Column | Type | Description |
|---|---|---|
| `financial_accounts_by_awards_id` | integer | FK to financial_accounts_by_awards |
| `award_id` | integer | Linked award ID |

&nbsp;

## Views

### mv_agency_autocomplete

Materialized view for agency search autocomplete.

| Column | Type | Description |
|---|---|---|
| `agency_autocomplete_id` | integer | ID |
| `toptier_agency_id` | integer | Top-tier agency ID |
| `toptier_code` | text | Top-tier code |
| `toptier_name` | text | Top-tier name |
| `toptier_abbreviation` | text | Top-tier abbreviation |
| `subtier_name` | text | Sub-tier name |
| `subtier_abbreviation` | text | Sub-tier abbreviation |
| `toptier_flag` | boolean | Top-tier flag |
| `has_awarding_data` | boolean | Has awarding data |
| `has_funding_data` | boolean | Has funding data |

### mv_agency_office_autocomplete

Materialized view for agency + office search autocomplete.

| Column | Type | Description |
|---|---|---|
| `agency_office_autocomplete_id` | bigint | ID |
| `toptier_code` | text | Top-tier code |
| `toptier_name` | text | Top-tier name |
| `subtier_code` | text | Sub-tier code |
| `subtier_name` | text | Sub-tier name |
| `office_code` | text | Office code |
| `office_name` | text | Office name |
| `has_awarding_data` | boolean | Has awarding data |
| `has_funding_data` | boolean | Has funding data |

### tas_autocomplete_matview

Materialized view for Treasury Account search autocomplete.

| Column | Type | Description |
|---|---|---|
| `tas_autocomplete_id` | integer | ID |
| `tas_rendering_label` | text | TAS display label |
| `agency_id` | text | Agency ID |
| `main_account_code` | text | Main account code |
| `sub_account_code` | text | Sub-account code |

### vw_appropriation_account_balances_download

Download-optimized view of appropriation account balances with agency name joined in.

### vw_financial_accounts_by_awards_download

Download-optimized view of award-level financial data with agency name joined in.

### vw_financial_accounts_by_program_activity_object_class_download

Download-optimized view of program activity/object class data with agency name joined in.

### vw_published_dabs_toptier_agency

Agencies with published DABS submissions.

### agency_lookup / agency_by_subtier_and_optionally_toptier

Agency lookup helper views.

### mv_entity_spending_summary

Unified entity spending profile combining `all_entities` with most recent award context from `entity_awards`. Pre-joins entity aggregates with their latest awarding agency, award type, and action date. ~18M rows.

| Column | Type | Description |
|---|---|---|
| `entity_id` | bigint | Primary key |
| `legal_business_name` | text | Entity legal name |
| `uei` | text | Unique Entity Identifier |
| `duns` | text | DUNS number |
| `state` | text | Entity state |
| `city` | text | Entity city |
| `latitude` | numeric | Geocoded latitude |
| `longitude` | numeric | Geocoded longitude |
| `geom_point` | geometry | PostGIS point geometry |
| `award_count` | bigint | Total award count |
| `total_obligation` | numeric | Total obligated amount |
| `date_first_award` | date | First award date |
| `date_last_award` | date | Last award date |
| `prime_subaward_count` | bigint | Prime + subaward count |
| `prime_subaward_amount` | numeric | Prime + subaward amount |
| `top_awarding_agency` | text | Most recent awarding agency |
| `most_recent_award_type` | text | Most recent award type |
| `most_recent_action_date` | date | Most recent action date |

#### Example queries

```bash
# Top recipients by total obligation
curl "https://benthic.io/ngopen/usaspending/mv_entity_spending_summary?select=entity_id,legal_business_name,uei,total_obligation,top_awarding_agency&order=total_obligation.desc&limit=25"

# Entities in a state
curl "https://benthic.io/ngopen/usaspending/mv_entity_spending_summary?state=eq.VA&select=legal_business_name,uei,total_obligation,award_count&order=total_obligation.desc&limit=25"

# Search by name
curl "https://benthic.io/ngopen/usaspending/mv_entity_spending_summary?legal_business_name=ilike.*lockheed*&select=entity_id,legal_business_name,uei,state,total_obligation&limit=25"
```

### mv_district_spending

Pre-aggregated federal spending by congressional district and fiscal year. Joins `prime_awards` with `zips_grouped` for district assignment.

| Column | Type | Description |
|---|---|---|
| `state` | text | State abbreviation |
| `district` | text | Congressional district number |
| `fiscal_year` | integer | Fiscal year |
| `award_count` | bigint | Number of awards |
| `total_obligation` | numeric | Total obligations |
| `total_award_amount` | numeric | Total award amounts |
| `unique_recipients` | bigint | Unique recipient count |
| `unique_agencies` | bigint | Unique agency count |

#### Example queries

```bash
# Top districts by spending in FY2024
curl "https://benthic.io/ngopen/usaspending/mv_district_spending?fiscal_year=eq.2024&select=state,district,total_obligation,award_count,unique_recipients&order=total_obligation.desc&limit=25"

# Spending trend for a district
curl "https://benthic.io/ngopen/usaspending/mv_district_spending?state=eq.CA&district=eq.12&select=fiscal_year,total_obligation,award_count&order=fiscal_year"
```

### mv_covid_spending

Aggregated COVID-19 spending tracking by fiscal year from `prime_awards` disaster emergency fund codes.

| Column | Type | Description |
|---|---|---|
| `fiscal_year` | integer | Fiscal year |
| `award_count` | bigint | Number of COVID awards |
| `total_covid_obligation` | numeric | Total COVID obligations |
| `total_covid_outlay` | numeric | Total COVID outlays |
| `unique_recipients` | bigint | Unique recipients |
| `unique_agencies` | bigint | Unique agencies |

#### Example queries

```bash
# COVID spending by year
curl "https://benthic.io/ngopen/usaspending/mv_covid_spending?select=fiscal_year,total_covid_obligation,total_covid_outlay,award_count&order=fiscal_year"
```

## PostgREST Query Reference

### Filtering

| Operator | Syntax | Example |
|---|---|---|
| Equals | `?col=value` | `?piid=eq.ABC123` |
| Not equal | `?col=neq.value` | `?disaster_emergency_fund_code=neq.L` |
| Greater than | `?col=gt.value` | `?obligations_incurred_total_by_award_cpe=gt.1000000` |
| Less than | `?col=lt.value` | `?reporting_period_end=lt.2024-01-01` |
| Greater/eq | `?col=gte.value` | `?fiscal_year=gte.2022` |
| Less/eq | `?col=lte.value` | `?fiscal_year=lte.2024` |
| ILIKE | `?col=ilike.PATTERN` | `?account_title=ilike.%25defense%25` |
| IS null | `?col=is.null` | `?award_id=is.null` |
| IS NOT null | `?col=not.is.null` | `?fain=not.is.null` |
| IN | `?col=in.(val1,val2)` | `?disaster_emergency_fund_code=in.(L,N,O)` |

### Selecting columns

```
?select=piid,fain,obligations_incurred_total_by_award_cpe,gross_outlay_amount_by_award_cpe
```

### Ordering

```
?order=obligations_incurred_total_by_award_cpe.desc
?order=reporting_period_end.desc
```

### Pagination

```
?limit=100&offset=200
```

### Counting

```
Prefer: count=exact
```

### Grouping / aggregation

```
?select=disaster_emergency_fund_code,sum.obligations_incurred_total_by_award_cpe&groupby=disaster_emergency_fund_code
```

&nbsp;

## Joining Tables (Embedding)

PostgREST supports resource embedding via foreign key relationships:

```bash
# Get award data with treasury account details
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?select=piid,fain,obligations_incurred_total_by_award_cpe,treasury_appropriation_account(account_title,tas_rendering_label)&obligations_incurred_total_by_award_cpe=not.is.null&order=obligations_incurred_total_by_award_cpe.desc&limit=10"

# Get treasury account with federal account
curl "https://benthic.io/ngopen/usaspending/treasury_appropriation_account?select=tas_rendering_label,account_title,federal_account(account_title)&treasury_account_identifier=eq.12345"

# Get appropriation balances with TAS details
curl "https://benthic.io/ngopen/usaspending/appropriation_account_balances?select=budget_authority_appropriated_amount_cpe,obligations_incurred_total_by_tas_cpe,treasury_appropriation_account(account_title)&final_of_fy=is.true&limit=25"

# Get program spending with object class and program activity names
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_program_activity_object_class?select=obligations_incurred_by_program_object_class_cpe,object_class(object_class_name),ref_program_activity(program_activity_name)&treasury_account_id=eq.12345&limit=25"

# Look up agency info
curl "https://benthic.io/ngopen/usaspending/agency?select=id,toptier_agency(name,abbreviation),subtier_agency(name)&toptier_flag=is.true&limit=50"
```

## Key Relationships

### Spending data chain
`toptier_agency` -> `federal_account` -> `treasury_appropriation_account` -> `financial_accounts_by_awards` / `financial_accounts_by_program_activity_object_class` / `appropriation_account_balances`.

### Agency hierarchy
`toptier_agency` -> `agency` -> `subtier_agency`

### Classification
`treasury_appropriation_account` links to `cgac`/`frec` via agency codes
`financial_accounts_by_awards` links to `object_class`, `ref_program_activity`, `references_cfda`
`financial_accounts_by_awards` links to `submission_attributes` via `submission_id`

### Geographic
`recipient_geocode_index.source_id` links to award recipient identifiers
`ref_population_county` and `ref_population_cong_district` provide population denominators

