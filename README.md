# benthic.io

*Benthic: living in or relating to the lowest levels of the ocean or other body of water.*

benthic.io is a free, open data platform providing public access to government spending, nonprofit, contractor, legislative, and geographic data. The mission is to ensure data capable of public good remains freely available to the public, forever.

## NGOpen API Collection

The debut API collection consists of five PostgREST APIs backed by PostgreSQL/PostGIS databases:

| API | Database | Data |
|-----|----------|------|
| [USAspending](https://benthic.io/ngopen/usaspending/) | usaspending_db | Federal grants, contracts, loans, subawards |
| [SAM.gov](https://benthic.io/ngopen/samer/) | sam_er | Entity registrations, NAICS/PSC codes |
| [IRS NGO](https://benthic.io/ngopen/irs_ng/) | irs_ng | 501(c)(3 nonprofits, Form 990, 527 political orgs |
| [Congress-Leg](https://benthic.io/ngopen/usp_cl/) | us_project_cl | Legislators, committees, district offices |
| [CD Maps](https://benthic.io/ngopen/up_cdmaps/) | ucla_polysci_cdmaps | Congressional district boundaries |

### Key Features

- **Geocoded data**: All datasets include latitude/longitude coordinates and PostGIS geometry columns
- **No authentication required**: Free public access via REST
- **Cross-database joins**: Pre-documented join paths between datasets
- **Spatial queries**: Point-in-polygon, proximity searches, distance calculations

### API Endpoints

```
https://benthic.io/ngopen/usaspending/
https://benthic.io/ngopen/samer/
https://benthic.io/ngopen/irs_ng/
https://benthic.io/ngopen/usp_cl/
https://benthic.io/ngopen/up_cdmaps/
```

### OpenAPI Schemas

Full JSON schemas available at `/api/*.json`:
- [usaspending.json](/api/usaspending.json)
- [samer.json](/api/samer.json)
- [irs_ng.json](/api/irs_ng.json)
- [usp_cl.json](/api/usp_cl.json)
- [up_cdmaps.json](/api/up_cdmaps.json)

## Documentation

- [API Reference](/apis/) - Complete API documentation with join paths, use cases, and query examples
- [PostgREST Syntax](https://docs.postgrest.org/) - External reference for query operators

## Quick Examples

### Find federal grants over $10M to nonprofits

```bash
curl "https://benthic.io/ngopen/usaspending/financial_accounts_by_awards?select=fain,obligations_incurred_total_by_award_cpe&obligations_incurred_total_by_award_cpe=gt.10000000&order=obligations_incurred_total_by_award_cpe.desc&limit=10"
```

### Look up a nonprofit's Form 990 financials

```bash
curl "https://benthic.io/ngopen/irs_ng/form990_soi?ein=eq.123456789&select=tax_year,total_revenue,total_expenses,total_assets&order=tax_year.desc"
```

### Find legislators on the Appropriations Committee

```bash
curl "https://benthic.io/ngopen/usp_cl/committee_membership?committee_thomas_id=eq.SAPP&select=legislator_name,party,rank&order=rank"
```

### Get congressional district boundary

```bash
curl "https://benthic.io/ngopen/up_cdmaps/congressional_districts?statename=eq.California&district=eq.20&congress_number=eq.118&select=geom"
```

## Tech Stack

- **Hugo** - Static site generator
- **PostgREST** - RESTful API server
- **PostgreSQL** - Database with PostGIS extension
- **Photon** - Geocoding (OpenStreetMap-based)

## Development

```bash
# Build the site
hugo -D

# Run local server
hugo server
```

## License

Public domain data. Built with open source tools. Dedicated to the public good.

## Contact

- **Email**: [brian@benthic.io](mailto:brian@benthic.io)
- **X / Twitter**: [@otherdrums](https://x.com/otherdrums)