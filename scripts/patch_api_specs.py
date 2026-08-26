#!/usr/bin/env python3
"""Post-process PostgREST-generated OpenAPI specs for public serving.

The raw specs exported from PostgREST expose internal dev hosts
(127.0.0.1:300X), generic titles, and every function present in the
public schema -- including hundreds of PostGIS/extension helpers that
are not part of any published contract. This script rewrites the served
metadata and strips non-contract RPC paths so /api/*.json reflects what
is actually documented and granted to web_anon.

Usage: python3 scripts/patch_api_specs.py [--check]

--check exits 1 if any spec would change (CI guard against re-exporting
raw PostgREST output over a patched spec).
"""

import argparse
import json
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
API_DIR = SITE_ROOT / "static" / "api"

BASE_HOST = "benthic.io"
BASE_PATH = "/ngopen/{name}"

# The four spatial RPCs documented on the site and granted EXECUTE.
ALLOWED_RPC = {
    "rpc_districts_in_bbox",
    "rpc_find_district",
    "rpc_nonprofits_in_district",
    "rpc_nonprofits_nearby",
}

# Relation paths that are database internals, never part of a public contract.
PATH_DENYLIST_EXACT = {
    "geography_columns",
    "geometry_columns",
    "spatial_ref_sys",
    "pg_stat_statements",
    "pg_stat_statements_info",
}
PATH_DENYLIST_PREFIX = (
    "django_",
    "auth_",
    "rest_framework_",
    "_staging_",
)

DATASETS = {
    "usaspending": {
        "title": "USAspending API",
        "description": (
            "Federal spending data from USAspending.gov: prime awards, subawards, "
            "financial accounts, agency references, and geocoded recipients, "
            "published by benthic.io as part of the NGOpen collection."
        ),
    },
    "samer": {
        "title": "SAM Entity Registry API",
        "description": (
            "SAM.gov entity registrations for federal contractors and vendors, "
            "enhanced with Photon/OpenStreetMap geocoding, published by "
            "benthic.io as part of the NGOpen collection."
        ),
    },
    "irs_ng": {
        "title": "IRS Nonprofits API",
        "description": (
            "IRS Exempt Organizations Business Master File, Form 990 SOI "
            "financials, Publication 78, auto-revocations, Form 990-N e-Postcards, "
            "990 XML filings, Section 527 political organizations, and ACS census "
            "demographics, published by benthic.io as part of the NGOpen collection."
        ),
    },
    "up_cdmaps": {
        "title": "Congressional District Maps API",
        "description": (
            "UCLA PolySci congressional district maps and boundaries for every "
            "congress, served over PostGIS with point-in-polygon and bbox RPCs, "
            "published by benthic.io as part of the NGOpen collection."
        ),
    },
    "usp_cl": {
        "title": "Congress Legislators API",
        "description": (
            "The unitedstates/congress-legislators dataset: members of Congress "
            "past and present with terms, committees, social accounts, and "
            "district offices, published by benthic.io as part of the NGOpen collection."
        ),
    },
}


def patch_spec(name: str, meta: dict) -> dict:
    path = API_DIR / f"{name}.json"
    original = path.read_text()
    spec = json.loads(original)

    spec["host"] = BASE_HOST
    spec["schemes"] = ["https"]
    spec["basePath"] = BASE_PATH.format(name=name)
    spec["info"]["title"] = meta["title"]
    spec["info"]["description"] = meta["description"]

    dropped = []
    for p in list(spec.get("paths", {})):
        rel = p.strip("/")
        if rel == "" or rel.startswith("rpc/"):
            if p.startswith("/rpc/") and p[5:] not in ALLOWED_RPC:
                dropped.append(p)
                del spec["paths"][p]
            continue
        if rel in PATH_DENYLIST_EXACT or rel.startswith(PATH_DENYLIST_PREFIX):
            dropped.append(p)
            del spec["paths"][p]

    patched = json.dumps(spec, indent=1) + "\n"
    changed = patched != original
    return {"changed": changed, "dropped": dropped, "patched": patched, "path": path}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any spec would change; do not write",
    )
    args = ap.parse_args()

    rc = 0
    for name, meta in DATASETS.items():
        result = patch_spec(name, meta)
        label = f"static/api/{name}.json"
        if not result["changed"]:
            print(f"{label}: up to date")
            continue
        if args.check:
            print(f"{label}: NEEDS PATCHING ({len(result['dropped'])} stale paths)")
            rc = 1
            continue
        result["path"].write_text(result["patched"])
        print(
            f"{label}: patched metadata, dropped {len(result['dropped'])} non-contract rpc paths"
        )
    return rc


if __name__ == "__main__":
    sys.exit(main())
