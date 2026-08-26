#!/usr/bin/env python3
"""Regenerate unsigned manifest.summary.json files from signed manifests.

Summaries are convenience documents and are intentionally NOT signed (see
SPEC.md §8): everything they contain is derived from the manifest itself.
Run this after any manifest is re-signed so the two never disagree.

Usage: python3 scripts/regen_summaries.py [--check]
"""

import argparse
import json
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parent.parent
BDP_DIR = SITE_ROOT / "static" / "bdp" / "ngopen"
DATASETS = ["usaspending", "samer", "irs_ng", "up_cdmaps", "usp_cl"]


def build_summary(
    manifest: dict, manifest_bytes: int, manifest_url: str, prev: dict
) -> dict:
    rels = manifest["schema_definition"]
    compact = [
        {
            "name": r["name"],
            "column_count": len(r.get("columns", [])),
            "provenance": r["provenance"],
            "queryable": r.get("queryable", True),
            "relation_type": r["relation_type"],
        }
        for r in rels
    ]
    etl = manifest["etl_provenance"]
    # Older manifests omit description/title/license; carry them over from the
    # previous summary so regeneration never loses prose written at sign time.
    return {
        "author_identity": manifest["author_identity"],
        "author_pubkey": manifest["author_pubkey"],
        "collection": manifest.get("collection"),
        "column_count": sum(len(r.get("columns", [])) for r in rels),
        "commit_hash": etl["commit_hash"],
        "dataset_name": manifest["dataset_name"],
        "description": manifest.get("description") or prev.get("description"),
        "endpoints": [
            {"base_url": e["base_url"], "transport_type": e["transport_type"]}
            for e in manifest["endpoints"]
        ],
        "license": manifest.get("license") or prev.get("license"),
        "manifest_bytes": manifest_bytes,
        "manifest_payload_hash": manifest["cryptographic_signature"]["payload_hash"],
        "manifest_url": manifest_url,
        "migration_status": etl["migration_status"],
        "queryable_relation_count": sum(1 for r in rels if r.get("queryable", True)),
        "relation_count": len(rels),
        "relations": compact,
        "repository_url": etl["repository_url"],
        "title": manifest.get("title") or prev.get("title"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 if any summary would change (CI guard)",
    )
    args = ap.parse_args()

    rc = 0
    for name in DATASETS:
        d = BDP_DIR / name
        mp = d / "manifest.json"
        sp = d / "manifest.summary.json"
        raw = mp.read_bytes()
        manifest_url = f"https://benthic.io/bdp/ngopen/{name}/manifest.json"
        prev = json.loads(sp.read_text()) if sp.exists() else {}
        summary = build_summary(json.loads(raw), len(raw), manifest_url, prev)
        out = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if sp.read_text() != out:
                print(f"{sp.relative_to(SITE_ROOT)}: would change")
                rc = 1
        else:
            sp.write_text(out)
            print(
                f"{sp.relative_to(SITE_ROOT)}: written "
                f"(migration_status={summary['migration_status']})"
            )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
