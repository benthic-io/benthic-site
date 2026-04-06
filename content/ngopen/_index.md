---
title: "APIs"
---

### NGOpen API Collection

Benthic.io's debut API collection, dubbed NGOpen, consists of five PostgREST APIs exposed directly at the listed root URLs.  They return OpenAPI JSON specs and expose standard public REST endpoints to provide structured, queryable access to geospatially enhanced versions of major U.S. government datasets. Each has been enhanced with latitude/longitude and PostGIS geometry columns. They also include census linkages, NAICS/PSC/CFDA crosswalks, and reference tables for ZIPs/congressional districts. This enables spatial filtering, proximity searches, point-in-polygon lookups, distance calculations, and mapping capabilities absent from the original sources. These APIs aim turn raw government data and other publically available information into a geographically intelligent investigative toolkit. If something is missing, broken, or you have any ideas to expand functionality please do not hesitate to contact me via one of the channels listed at the bottom of the page. 

- **https://benthic.io/ngopen/usaspending/** – [USAspending.gov](https://www.usaspending.gov/) database enhanced with geocoding data. - [Documentation](/ngopen/usaspending/)

- **https://benthic.io/ngopen/samer/** – SAM.gov entity registrations for federal contractors & vendors enhanced with geocoding data.- [Documentation](/ngopen/samer/)

- **https://benthic.io/ngopen/up_cdmaps/** – UCLA Polysci's comprehesive congressional district maps & boundaries for every congress to present day. - [Documentation](/ngopen/up_cdmaps/)

- **https://benthic.io/ngopen/usp_cl/** – [@unitedstatesproject](https://unitedstates.github.io/)'s congress-legislators provides detailed data on members of Congress past & present.  - [Documentation](/ngopen/usp_cl/)

- **https://benthic.io/ngopen/irs_ng/** – Geocoded versions of IRS Exempt Organizations Business Master File, Form 990/990-EZ/990-PF SOI financials, Publication 78 deductibility eligibility, auto-revocation list, Form 990-N e-Postcard, Form 990 XML filings with Schedule O narratives and Schedule R flags, Section 527 political organizations, and ACS census demographics. - [Documentation](/ngopen/irs_ng/)
