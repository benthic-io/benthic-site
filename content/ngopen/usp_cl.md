---
title: "Docs"
---
### https://benthic.io/ngopen/usp_cl/ – U.S. legislators, executives, committees & district offices

The core theme of this database, created using the wonderful congress-legislators dataset made available by the [@unitedstates project](https://unitedstates.github.io/), is political structure. 

## Tables

### legislators

Current and historical members of the U.S. Congress. One row per person. Links to terms, social media, district offices, and committee membership via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `bioguide_id` | varchar(10) | **Primary key.** Biographical Directory ID |
| `thomas_id` | varchar(10) | THOMAS/LIS ID (legacy) |
| `lis_id` | varchar(10) | LIS ID (Senate) |
| `govtrack_id` | integer | GovTrack ID |
| `opensecrets_id` | varchar(20) | OpenSecrets ID |
| `votesmart_id` | integer | Vote Smart ID |
| `cspan_id` | integer | C-SPAN ID |
| `wikipedia_page` | varchar(255) | Wikipedia page title |
| `ballotpedia_page` | varchar(255) | Ballotpedia page |
| `maplight_id` | integer | MapLight ID |
| `house_history_id` | bigint | House History ID |
| `icpsr_id` | integer | ICPSR ID |
| `wikidata_id` | varchar(20) | Wikidata ID |
| `google_entity_id` | varchar(100) | Google Knowledge Graph ID |
| `pictorial_id` | integer | Congress pictorial ID |
| `fec_ids` | text[] | FEC candidate IDs (array) |
| `bioguide_previous` | text[] | Previous bioguide IDs (array) |
| `first_name` | varchar(100) | First name |
| `middle_name` | varchar(100) | Middle name |
| `last_name` | varchar(100) | Last name |
| `suffix` | varchar(20) | Name suffix (Jr., Sr., etc.) |
| `nickname` | varchar(100) | Nickname |
| `official_full` | varchar(255) | Official full name |
| `birthday` | date | Date of birth |
| `gender` | char(1) | Gender (M/F) |
| `is_current` | boolean | TRUE if currently serving |
| `first_term_start` | date | Date of first term start |
| `last_term_end` | date | Date of most recent term end |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get all current members
curl "https://benthic.io/ngopen/usp_cl/legislators?is_current=is.true&select=bioguide_id,official_full,last_name,first_name&order=last_name&limit=200"

# Look up a specific legislator
curl "https://benthic.io/ngopen/usp_cl/legislators?bioguide_id=eq.P000197&select=official_full,birthday,gender,govtrack_id"

# Search by name
curl "https://benthic.io/ngopen/usp_cl/legislators?official_full=ilike.*schumer*&select=bioguide_id,official_full,is_current"

# Count current members by gender
curl "https://benthic.io/ngopen/usp_cl/legislators?select=gender,count&is_current=is.true&groupby=gender"
```


### legislator_terms

Service terms for members of Congress. One row per term. Links to `legislators` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `term_id` | integer | Primary key |
| `bioguide_id` | varchar(10) | FK to legislators |
| `congress_start` | varchar(3) | Starting Congress number |
| `congress_end` | varchar(3) | Ending Congress number |
| `term_start` | date | Term start date |
| `term_end` | date | Term end date |
| `term_type` | varchar(10) | `rep`, `sen`, or `prez` |
| `state` | char(2) | State abbreviation |
| `district` | integer | Congressional district number |
| `class` | integer | Senate class (1, 2, or 3) |
| `state_rank` | varchar(10) | Senate rank (`junior`/`senior`) |
| `party` | varchar(50) | Political party |
| `url` | varchar(500) | Official website URL |
| `address` | text | Office address |
| `phone` | varchar(50) | Office phone |
| `fax` | varchar(50) | Office fax |
| `contact_form` | varchar(500) | Contact form URL |
| `office` | varchar(255) | Office location |
| `rss_url` | varchar(500) | RSS feed URL |
| `how` | varchar(50) | How the term ended (appointment, election, etc.) |
| `end_type` | varchar(50) | End type |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get all terms for a legislator
curl "https://benthic.io/ngopen/usp_cl/legislator_terms?bioguide_id=eq.P000197&order=term_start"

# Get all current Senate terms
curl "https://benthic.io/ngopen/usp_cl/legislator_terms?term_type=eq.sen&term_end=gte.2026-01-01&select=bioguide_id,state,state_rank,party&order=state"

# Get representatives for a state
curl "https://benthic.io/ngopen/usp_cl/legislator_terms?state=eq.CA&term_type=eq.rep&term_end=gte.2026-01-01&select=bioguide_id,district,party&order=district"

# Get all terms in a specific Congress (118th = 2023-2025)
curl "https://benthic.io/ngopen/usp_cl/legislator_terms?congress_start=eq.118&select=bioguide_id,term_type,state,district,party&limit=600"

# Count members by party for current terms
curl "https://benthic.io/ngopen/usp_cl/legislator_terms?select=party,count&term_end=gte.2026-01-01&groupby=party"
```


### legislator_social_media

Social media accounts for legislators. One row per legislator. Links to `legislators` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `social_id` | integer | Primary key |
| `bioguide_id` | varchar(10) | FK to legislators |
| `twitter` | varchar(100) | Twitter/X handle |
| `twitter_id` | varchar(50) | Twitter/X numeric ID |
| `facebook` | varchar(100) | Facebook page |
| `facebook_id` | bigint | Facebook numeric ID |
| `youtube` | varchar(100) | YouTube channel |
| `youtube_id` | varchar(100) | YouTube channel ID |
| `instagram` | varchar(100) | Instagram handle |
| `instagram_id` | bigint | Instagram numeric ID |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get social media for a legislator
curl "https://benthic.io/ngopen/usp_cl/legislator_social_media?bioguide_id=eq.P000197&select=twitter,facebook,youtube,instagram"

# Find legislators with Instagram
curl "https://benthic.io/ngopen/usp_cl/legislator_social_media?instagram=not.is.null&select=bioguide_id,twitter,instagram&limit=100"
```


### legislator_other_names

Alternate and former names for legislators. One row per name variant. Links to `legislators` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `name_id` | integer | Primary key |
| `bioguide_id` | varchar(10) | FK to legislators |
| `first_name` | varchar(100) | Alternate first name |
| `middle_name` | varchar(100) | Alternate middle name |
| `last_name` | varchar(100) | Alternate last name |
| `suffix` | varchar(20) | Name suffix |
| `start_date` | date | Name usage start date |
| `end_date` | date | Name usage end date |
| `created_at` | timestamp | Record creation time |


### district_offices

Geocoded district office locations for members of Congress. One row per office. Links to `legislators` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `office_id` | integer | Primary key |
| `bioguide_id` | varchar(10) | FK to legislators |
| `office_key` | varchar(100) | Unique office key |
| `address` | text | Street address |
| `suite` | varchar(255) | Suite number |
| `building` | varchar(255) | Building name |
| `city` | varchar(100) | City |
| `state` | char(2) | State |
| `zip` | varchar(20) | ZIP code |
| `latitude` | double precision | Geocoded latitude |
| `longitude` | double precision | Geocoded longitude |
| `geom_point` | geometry(Point, 4326) | PostGIS point geometry (auto-populated from lat/lon) |
| `phone` | varchar(50) | Office phone |
| `fax` | varchar(50) | Office fax |
| `hours` | text | Office hours |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get district offices for a legislator
curl "https://benthic.io/ngopen/usp_cl/district_offices?bioguide_id=eq.P000197&select=address,city,state,zip,phone,latitude,longitude"

# Get all geocoded offices in a state
curl "https://benthic.io/ngopen/usp_cl/district_offices?state=eq.TX&latitude=not.is.null&select=bioguide_id,city,latitude,longitude&limit=50"

# Find offices near a coordinate
curl "https://benthic.io/ngopen/usp_cl/district_offices?latitude=gte.38.0&latitude=lte.39.0&longitude=gte.-77.0&longitude=lte.-76.0&latitude=not.is.null"
```


### executives

Presidents and executive branch officials. One row per person. Links to `executive_terms` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `bioguide_id` | varchar(10) | Primary key |
| `govtrack_id` | integer | GovTrack ID |
| `icpsr_prez_id` | integer | ICPSR president ID |
| `first_name` | varchar(100) | First name |
| `middle_name` | varchar(100) | Middle name |
| `last_name` | varchar(100) | Last name |
| `suffix` | varchar(20) | Name suffix |
| `birthday` | date | Date of birth |
| `gender` | char(1) | Gender |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# List all presidents
curl "https://benthic.io/ngopen/usp_cl/executives?select=bioguide_id,last_name,first_name,birthday&order=last_name"
```


### executive_terms

Terms of office for presidents. Links to `executives` via `bioguide_id`.

| Column | Type | Description |
|---|---|---|
| `term_id` | integer | Primary key |
| `bioguide_id` | varchar(10) | FK to executives |
| `term_type` | varchar(20) | Term type (e.g. `prez`) |
| `start_date` | date | Term start date |
| `end_date` | date | Term end date |
| `party` | varchar(50) | Political party |
| `how` | varchar(50) | How obtained (election, succession) |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get presidential terms
curl "https://benthic.io/ngopen/usp_cl/executive_terms?select=bioguide_id,term_type,start_date,end_date,party&order=start_date.desc"
```


### committees

Congressional committees (standing, select, joint). One row per committee.

| Column | Type | Description |
|---|---|---|
| `committee_id` | integer | Primary key |
| `thomas_id` | varchar(20) | THOMAS committee ID |
| `house_committee_id` | varchar(10) | House committee ID |
| `senate_committee_id` | varchar(10) | Senate committee ID |
| `committee_type` | varchar(20) | Committee type (`house`, `senate`, `joint`) |
| `name` | varchar(255) | Committee name |
| `url` | varchar(500) | Committee website |
| `minority_url` | varchar(500) | Minority party website |
| `address` | text | Committee address |
| `phone` | varchar(50) | Committee phone |
| `jurisdiction` | text | Committee jurisdiction description |
| `rss_url` | varchar(500) | RSS feed URL |
| `youtube_id` | varchar(50) | YouTube channel ID |
| `congresses` | integer[] | Congress numbers when active (array) |
| `is_current` | boolean | TRUE if currently active |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get all current committees
curl "https://benthic.io/ngopen/usp_cl/committees?is_current=is.true&select=committee_id,name,committee_type&order=committee_type,name"

# Get Senate committees
curl "https://benthic.io/ngopen/usp_cl/committees?committee_type=eq.senate&is_current=is.true&select=name,url,phone"

# Search committees by name
curl "https://benthic.io/ngopen/usp_cl/committees?name=ilike.*appropriations*&select=committee_id,name,committee_type"
```


### subcommittees

Subcommittees under congressional committees. Links to `committees` via `committee_id`.

| Column | Type | Description |
|---|---|---|
| `subcommittee_id` | integer | Primary key |
| `committee_id` | integer | FK to committees |
| `thomas_id` | varchar(10) | THOMAS subcommittee ID |
| `name` | varchar(255) | Subcommittee name |
| `address` | text | Subcommittee address |
| `phone` | varchar(50) | Subcommittee phone |
| `congresses` | integer[] | Congress numbers when active (array) |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get subcommittees for a committee
curl "https://benthic.io/ngopen/usp_cl/subcommittees?committee_id=eq.26&select=subcommittee_id,name"
```


### committee_membership

Legislator assignments to committees and subcommittees. One row per assignment.

| Column | Type | Description |
|---|---|---|
| `membership_id` | integer | Primary key |
| `committee_thomas_id` | varchar(20) | THOMAS committee/subcommittee ID |
| `bioguide_id` | varchar(10) | Legislator bioguide ID |
| `legislator_name` | varchar(255) | Legislator name |
| `party` | varchar(20) | Political party |
| `rank` | integer | Seniority rank |
| `title` | varchar(100) | Title (Chair, Ranking Member, etc.) |
| `created_at` | timestamp | Record creation time |

#### Example queries

```bash
# Get committee members for a committee
curl "https://benthic.io/ngopen/usp_cl/committee_membership?committee_thomas_id=eq.SFIN&select=legislator_name,party,rank,title&order=rank"

# Get all committee assignments for a legislator
curl "https://benthic.io/ngopen/usp_cl/committee_membership?bioguide_id=eq.P000197&select=committee_thomas_id,party,rank,title"

# Get chairs of committees
curl "https://benthic.io/ngopen/usp_cl/committee_membership?title=ilike.*chair*&select=legislator_name,committee_thomas_id,title&limit=50"
```


## Views

### Embedding examples

PostgREST supports resource embedding via foreign key relationships:

```bash
# Get a legislator with all their terms
curl "https://benthic.io/ngopen/usp_cl/legislators?select=official_full,legislator_terms(term_type,state,district,party)&bioguide_id=eq.P000197"

# Get a legislator with social media
curl "https://benthic.io/ngopen/usp_cl/legislators?select=official_full,legislator_social_media(twitter,facebook,instagram)&bioguide_id=eq.P000197"

# Get a legislator with district offices
curl "https://benthic.io/ngopen/usp_cl/legislators?select=official_full,district_offices(city,state,phone,latitude,longitude)&bioguide_id=eq.P000197"

# Get a committee with its subcommittees
curl "https://benthic.io/ngopen/usp_cl/committees?select=name,subcommittees(name)&committee_id=eq.26"

# Get current senators with their terms embedded
curl "https://benthic.io/ngopen/usp_cl/legislators?select=official_full,legislator_terms!inner(state,state_rank,party)&legislator_terms.term_type=eq.sen&legislator_terms.term_end=gte.2026-01-01&is_current=is.true&order=official_full"
```


## PostgREST Query Reference

### Filtering

| Operator | Syntax | Example |
|---|---|---|
| Equals | `?col=value` | `?state=eq.CA` |
| Not equal | `?col=neq.value` | `?party=neq.Democrat` |
| Greater than | `?col=gt.value` | `?term_end=gt.2025-01-01` |
| Less than | `?col=lt.value` | `?birthday=lt.1960-01-01` |
| Greater/eq | `?col=gte.value` | `?term_end=gte.2026-01-01` |
| Less/eq | `?col=lte.value` | `?term_end=lte.2025-12-31` |
| ILIKE | `?col=ilike.PATTERN` | `?official_full=ilike.%25john%25` |
| IS null | `?col=is.null` | `?end_type=is.null` |
| IS NOT null | `?col=not.is.null` | `?twitter=not.is.null` |
| IN | `?col=in.(val1,val2)` | `?state=in.(CA,NY,TX)` |

### Selecting columns

```
?select=bioguide_id,official_full,state,party
```

### Ordering

```
?order=last_name.asc
?order=term_start.desc
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
?select=party,count&groupby=party
```

## Key Relationships

All tables link via **bioguide_id** or **committee_id/thomas_id**:

- `legislators.bioguide_id` = primary person identifier
- `legislator_terms.bioguide_id` -> `legislators.bioguide_id`
- `legislator_social_media.bioguide_id` -> `legislators.bioguide_id`
- `legislator_other_names.bioguide_id` -> `legislators.bioguide_id`
- `district_offices.bioguide_id` -> `legislators.bioguide_id`
- `executive_terms.bioguide_id` -> `executives.bioguide_id`
- `subcommittees.committee_id` -> `committees.committee_id`
- `committee_membership.bioguide_id` -> `legislators.bioguide_id` (logical, no FK constraint)
- `committee_membership.committee_thomas_id` -> `committees.thomas_id` (logical, no FK constraint)

Cross-dataset: `legislator_terms.state` + `district` matches `up_cdmaps.congressional_districts` for spatial district boundaries.



