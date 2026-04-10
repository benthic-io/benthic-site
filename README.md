# benthic.io

*Benthic: living in or relating to the lowest levels of the ocean or other body of water.*

benthic.io is a free, open data platform. The mission: ensure data capable of public good remains freely available to the public, forever.

## The Site

This repository contains the Hugo-based static site for benthic.io. It provides documentation for the API collection and serves as the public-facing web presence.

## Data

NGOpen is the debut dataset — government spending, nonprofit, contractor, legislative, and geographic data accessible via public REST APIs. More datasets will be added over time.

## Tech Stack

- Hugo (static site generator)
- PostgreSQL + PostGIS (databases)
- PostgREST (RESTful API layer)
- Photon (geocoding)

## Development

```bash
# Build the site
hugo -D

# Run local server
hugo server
```

## Contact

- Email: brian@benthic.io
- X/Twitter: @otherdrums