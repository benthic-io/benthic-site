---
title: "Benthic Data Provenance"
---

### Benthic Data Provenance (BDP)

Every dataset published here is accompanied by a signed **manifest**: a JSON document that states who built the dataset, which code built it, what shape the data is in, and where it can be reached. The manifest is signed with an Ed25519 key. Anyone can verify it without asking benthic.io for permission, without an API key, and without trusting this server.

The point is auditability. If a dataset claims to be the output of a public ETL pipeline, you should be able to check that claim yourself — read the pipeline source, read the manifest, confirm the signature, and decide for yourself whether the two match.

BDP is transport-agnostic. A manifest describes _endpoints_, and an endpoint may be a live query API or a static file. Today benthic.io publishes a single live PostgREST endpoint per dataset. Parquet and GeoParquet transports are defined in the schema and will be added without any change to the protocol.

&nbsp;

### Discovery

Start at the index and follow the chain. Every step is a plain JSON file over HTTPS.

```bash
# 1. the discovery root: what collections exist here
curl https://benthic.io/bdp/index.json

# 2. a collection: its members, their pinned hashes, and how they join
curl https://benthic.io/bdp/ngopen/collection.json
curl https://benthic.io/bdp/parts/collection.json

# 3. a dataset manifest: full schema, provenance, endpoints, signature
curl https://benthic.io/bdp/ngopen/usaspending/manifest.json
curl https://benthic.io/bdp/parts/nhtsa/manifest.json
```

Manifests carry a complete column-level schema, so some are large. For cheap discovery each one has a summary alongside it, which lists relations and column counts and pins the hash of the full manifest:

```bash
curl https://benthic.io/bdp/ngopen/samer/manifest.summary.json
```

Read the summary, decide whether the dataset is interesting, then fetch and verify the full manifest. The summary is deliberately unsigned — it makes no claim of its own, it only points at a document that does.

&nbsp;

### Published documents

| Document                                                           | Purpose                                                               |
| ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| [`/bdp/index.json`](/bdp/index.json)                               | Discovery root. Lists collections. Unsigned by design.                |
| [`/bdp/keys.json`](/bdp/keys.json)                                 | Active and revoked signing keys.                                      |
| [`/bdp/ngopen/collection.json`](/bdp/ngopen/collection.json)       | The NGOpen collection. **Signed.** Pins each member manifest by hash. |
| [`/bdp/parts/collection.json`](/bdp/parts/collection.json)         | The Parts collection. **Signed.** Pins each member manifest by hash.  |
| [`/bdp/v1/manifest.schema.json`](/bdp/v1/manifest.schema.json)     | JSON Schema (Draft 2020-12) for manifests.                            |
| [`/bdp/v1/collection.schema.json`](/bdp/v1/collection.schema.json) | JSON Schema (Draft 2020-12) for collections.                          |

Dataset manifests, all signed:

| Dataset                 | Manifest                                               | Summary                                                  |
| ----------------------- | ------------------------------------------------------ | -------------------------------------------------------- |
| USAspending             | [manifest.json](/bdp/ngopen/usaspending/manifest.json) | [summary](/bdp/ngopen/usaspending/manifest.summary.json) |
| SAM.gov                 | [manifest.json](/bdp/ngopen/samer/manifest.json)       | [summary](/bdp/ngopen/samer/manifest.summary.json)       |
| IRS Nonprofits          | [manifest.json](/bdp/ngopen/irs_ng/manifest.json)      | [summary](/bdp/ngopen/irs_ng/manifest.summary.json)      |
| Congress Legislators    | [manifest.json](/bdp/ngopen/usp_cl/manifest.json)      | [summary](/bdp/ngopen/usp_cl/manifest.summary.json)      |
| Congressional Districts | [manifest.json](/bdp/ngopen/up_cdmaps/manifest.json)   | [summary](/bdp/ngopen/up_cdmaps/manifest.summary.json)   |
| NHTSA vPIC              | [manifest.json](/bdp/parts/nhtsa/manifest.json)        | [summary](/bdp/parts/nhtsa/manifest.summary.json)        |

&nbsp;

### Verifying a signature

A manifest is signed over the SHA-256 digest of its own canonical form, with the signature block removed. Canonicalization is [RFC 8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785). The digest is recorded in the manifest as `payload_hash`, which makes it a standalone content address you can log, publish, and compare across mirrors.

```python
import base64, hashlib, json, urllib.request
import rfc8785
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

url = "https://benthic.io/bdp/ngopen/samer/manifest.json"
doc = json.load(urllib.request.urlopen(url))

sig = doc.pop("cryptographic_signature")          # detach, do not null it
digest = hashlib.sha256(rfc8785.dumps(doc)).digest()

assert digest.hex() == sig["payload_hash"]         # content matches its hash

Ed25519PublicKey.from_public_bytes(
    base64.b64decode(doc["author_pubkey"])
).verify(base64.b64decode(sig["signature_base64"]), digest)

print("verified:", doc["dataset_name"])
```

Two things trip people up:

- `author_pubkey` is a **raw 32-byte Ed25519 public key in standard Base64** — not `ssh-ed25519` wire format, not PEM SPKI.
- The signature covers the **raw 32 digest bytes**, never the hex string.

Or use the reference tool:

```bash
pip install git+https://github.com/benthic-io/bdp
curl -s https://benthic.io/bdp/ngopen/samer/manifest.json | bdp verify -
```

&nbsp;

### Provenance is graded

Being honest about where data comes from matters more than making every relation look equally authoritative. Each relation in a manifest declares one of three provenance values:

| Value       | Meaning                                                                                                                                  |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `upstream`  | Shipped by the original publisher. Present as-is.                                                                                        |
| `derived`   | Built by a benthic.io ETL pipeline you can read.                                                                                         |
| `recovered` | Exists in the live database, built by hand, with no ETL source. Recovered from the catalog and published as SQL so it can be reproduced. |

Relations also declare `queryable`. A large upstream source table may appear in a manifest as the provenance root of a derived view while being marked unreachable through the API — visible as lineage, honestly marked as not directly queryable.

Manifests additionally carry `etl_provenance.migration_status`. All five NGOpen datasets are now `migrated`: each pipeline-built candidate has been swapped into serving and re-verified. The git history of these manifests is the audit trail.

&nbsp;

### Source

- **Provenance specification and reference tooling** — [github.com/benthic-io/bdp](https://github.com/benthic-io/bdp)
- **The NGOpen pipelines** — [github.com/benthic-io/ngopen-bdp-pipelines](https://github.com/benthic-io/ngopen-bdp-pipelines)
- **The Parts pipelines** — [github.com/otherdrums/parts-pipelines](https://github.com/otherdrums/parts-pipelines)

Questions, corrections, and criticism are all welcome at [brian@benthic.io](mailto:brian@benthic.io).
