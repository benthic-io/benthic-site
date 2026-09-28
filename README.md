# benthic.io

**Benthic** / bĕn′thĭk / _adjective_: living in or relating to the lowest levels of the ocean or other body of water.

benthic.io is a free, open data platform. The mission: ensure data capable of
public good remains freely available to the public, forever.

---

## The collection

Two collections, six datasets. This repository holds the website, the reference
documentation, and the signed provenance documents — not the data itself.

| Collection | Datasets                                                                                            | Manifest                                                                  |
| ---------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **NGOpen** | USAspending, IRS Nonprofits, SAM Entity Registry, Congress Legislators, Congressional District Maps | [`ngopen/collection.json`](https://benthic.io/bdp/ngopen/collection.json) |
| **Parts**  | NHTSA vPIC Vehicle Information                                                                      | [`parts/collection.json`](https://benthic.io/bdp/parts/collection.json)   |

Every dataset is documented four ways in parallel, and the front page links all
four together:

```
https://benthic.io/ngopen/<dataset>/                 the live PostgREST API
https://benthic.io/docs/<dataset>/                   hand-written reference
https://benthic.io/bdp/<collection>/<dataset>/       signed provenance manifest
github.com/benthic-io/<pipeline>/pipelines/<ds>/README.md   how it is built
```

The authoritative index is the generated
[documentation map](https://benthic.io/docs/map/), built from
[`data/datasets.yaml`](data/datasets.yaml).

### Repositories

| Repository                                                                      | What it holds                               |
| ------------------------------------------------------------------------------- | ------------------------------------------- |
| [benthic-io/benthic-site](https://github.com/benthic-io/benthic-site)           | This repository. Site, docs, BDP documents. |
| [benthic-io/ngopen-pipelines](https://github.com/benthic-io/ngopen-pipelines)   | The five NGOpen ETL pipelines.              |
| [benthic-io/partout-pipelines](https://github.com/benthic-io/partout-pipelines) | The Parts (NHTSA) ETL pipeline.             |
| [benthic-io/bdp](https://github.com/benthic-io/bdp)                             | The BDP manifest and signing specification. |

---

## Quick start

```bash
# Build the site
hugo

# Run a local server with drafts enabled
hugo server -D
```

---

## Commands

Everything under `scripts/` takes a `--check` mode that fails rather than
writes, so it can gate a build.

| Command                                      | Does                                                                                                                                                                                                          |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `python3 scripts/check_docs.py`              | **Start here.** Verifies every dataset in the registry is documented, the docs pages match the required structure, no heading levels skip, every code fence has a language, and every internal link resolves. |
| `python3 scripts/check_docs.py --strict`     | Also fail on advisory notes.                                                                                                                                                                                  |
| `python3 scripts/gen_docmap.py`              | Regenerate `content/docs/map.md` from the registry and the signed manifests.                                                                                                                                  |
| `python3 scripts/gen_docmap.py --check`      | Fail if the committed map is stale.                                                                                                                                                                           |
| `python3 scripts/refresh_docs_sections.py`   | Rewrite the `At a glance` and `Related` sections of each reference page from the manifests. Run after a re-sign.                                                                                              |
| `python3 scripts/patch_api_specs.py`         | Regenerate `static/api/*.json` from the live catalogs.                                                                                                                                                        |
| `python3 scripts/regen_summaries.py`         | Regenerate `static/bdp/**/manifest.summary.json` from the signed manifests.                                                                                                                                   |
| `python3 scripts/regen_summaries.py --check` | Fail if any summary disagrees with its manifest.                                                                                                                                                              |

### Adding a dataset

1. Add an entry to [`data/datasets.yaml`](data/datasets.yaml). Copy the casing
   comment at the top of that file — it is the one thing that goes wrong
   routinely.
2. Add the reference page `content/docs/<slug>.md` and the explorer page
   `content/swagger/<slug>.md`.
3. Add the OpenAPI spec at `static/api/<spec>.json`.
4. Sign the manifest and drop it at `static/bdp/<collection>/<slug>/manifest.json`.
5. Run `python3 scripts/regen_summaries.py` and `python3 scripts/gen_docmap.py`.
6. Run `python3 scripts/check_docs.py` — it will tell you what you missed.

Membership in a collection is _not_ declared in `datasets.yaml`. It comes from
the signed `collection.json`, so a published dataset with no docs fails
`check_docs.py` even if you forget step 1.

---

## Configuration

`hugo.toml` holds the site title, description, contact parameters, the main
menu, and two rendering settings:

- `markup.goldmark.renderer.unsafe = true` — required for the raw HTML in
  `content/about.md` and the `&nbsp;` spacers used for layout in `content/apis.md`.
- `disableKinds = ["taxonomy", "term"]` — no page uses tags or categories, and
  Hugo was otherwise generating empty `/tags/` and `/categories/` pages and
  listing them in `sitemap.xml`.

Menu entries live in `[menu]`. The weight gap at 20 used to be where an "APIs"
entry had been; it now points at `/docs/`.

---

## BDP publication boundary

This repository **owns** BDP publication. It holds the signed manifests and
collection documents under `static/bdp/`, the OpenAPI specifications under
`static/api/`, and the human-readable explanation at
[content/bdp.md](content/bdp.md).

The pipeline repositories **own** the databases and the ETL that fills them.
They publish a `partout.toml` / `ngopen.toml` and a pipeline README; they do not
sign manifests.

The [BDP specification](https://github.com/benthic-io/bdp) is a separate
repository, and `content/bdp.md` links to all three. Neither the site README nor
the pipeline READMEs used to link to each other, which is why the front page
once linked to GitHub directories that rendered nothing.

---

## Tech Stack

- Hugo — static site generator
- PostgreSQL + PostGIS — the databases
- PostgREST — the RESTful API layer
- Photon — geocoding
- BDP — Ed25519-signed provenance manifests, canonicalized per RFC 8785 and
  hashed with SHA-256. See <https://benthic.io/bdp/>

---

## Development

```bash
hugo -D                              # build with drafts
hugo server                          # local server

python3 -m pip install pyyaml        # the doc tools need it
python3 scripts/check_docs.py        # documentation structure and coverage
python3 scripts/gen_docmap.py --check
python3 scripts/regen_summaries.py --check
```

`[.github/workflows/docs.yml](.github/workflows/docs.yml)` runs all of the
above plus a Hugo build on every push and pull request, and additionally checks
that `check_docs.py` passes in both pipeline repositories.

---

## Layout

```text
content/                 site content
  _index.md              home page
  apis.md                cross-dataset overview: join paths, use cases
  bdp.md                 the BDP explanation and verification instructions
  ngopen/_index.md       NGOpen collection landing page
  about.md               about the project
  docs/                  per-dataset reference pages + _index.md
  docs/map.md            GENERATED documentation map
  swagger/               one explorer page per dataset
data/
  datasets.yaml          THE dataset registry
layouts/                 Hugo templates
  index.html             front page, with the per-dataset status dashboard
  shortcodes/openapi.html  the Swagger UI embed
static/
  api/*.json             OpenAPI specifications, one per dataset
  bdp/                   signed manifests, collections, summaries, schemas
  AGENTS.md              machine-readable guide for coding agents
scripts/                 the maintenance and checking tools
.github/workflows/docs.yml   CI for everything above
hugo.toml
```

---

## Documentation

| Document                                                                               | What it covers                                                            |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [README.md](README.md)                                                                 | This file.                                                                |
| [data/datasets.yaml](data/datasets.yaml)                                               | The dataset registry — the single source of truth.                        |
| [content/docs/map.md](content/docs/map.md)                                             | The generated documentation map.                                          |
| [static/AGENTS.md](static/AGENTS.md)                                                   | Guide for coding agents: schema, pitfalls, playbooks.                     |
| [house style](https://github.com/benthic-io/ngopen-pipelines/blob/main/HOUSE-STYLE.md) | Required structure for every document across the benthic.io repositories. |
| [BDP specification](https://github.com/benthic-io/bdp)                                 | The manifest and signing protocol.                                        |
| [ngopen-pipelines](https://github.com/benthic-io/ngopen-pipelines)                     | The NGOpen ETL.                                                           |
| [partout-pipelines](https://github.com/benthic-io/partout-pipelines)                   | The Parts ETL.                                                            |

---

## License

MIT. See [LICENSE](LICENSE).

---

## Contact

- Email: brian@benthic.io
- X/Twitter: [@otherdrums](https://x.com/otherdrums)
