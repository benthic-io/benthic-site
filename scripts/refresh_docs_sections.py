#!/usr/bin/env python3
"""One-shot helper: insert the canonical "At a glance" and "Related" sections
into each API reference page, with values read from the signed manifests.

This exists because writing those tables by hand is how they go stale — a row
count that was right in August and wrong in November is worse than no table.
Run it after re-signing a manifest, then commit the result.

The committed page text is the source of truth for prose; this only manages the
two sections that are pure metadata, and it refuses to duplicate a section that
already exists.

    python3 scripts/refresh_docs_sections.py          # insert or update
    python3 scripts/refresh_docs_sections.py --check  # report drift only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("refresh_docs_sections: PyYAML is required (pip install pyyaml)")

SITE_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = SITE_ROOT / "data" / "datasets.yaml"
BDP_DIR = SITE_ROOT / "static" / "bdp"
CONTENT = SITE_ROOT / "content"

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
URL_HEADING = re.compile(r"^https?://")


def load_registry() -> dict:
    with REGISTRY.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def manifest_facts(collection: str, slug: str) -> dict:
    with (BDP_DIR / collection / slug / "manifest.summary.json").open(
        encoding="utf-8"
    ) as handle:
        summary = json.load(handle)
    with (BDP_DIR / collection / slug / "manifest.json").open(
        encoding="utf-8"
    ) as handle:
        manifest = json.load(handle)
    etl = manifest.get("etl_provenance", {}) or {}
    return {
        "summary": summary,
        "manifest": manifest,
        "etl": etl,
    }


def human_cadence(cadence: str) -> str:
    return {
        "monthly": "Monthly",
        "weekly": "Weekly",
        "never": "Static — published once, never refreshed",
    }.get(cadence, cadence)


def thousands(value) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def at_a_glance(dataset: dict, collection_info: dict, facts: dict) -> str:
    slug = dataset["slug"]
    collection = dataset["collection"]
    summary = facts["summary"]
    etl = facts["etl"]
    pipeline = dataset["pipeline"]

    relations = summary.get("relation_count", "—")
    queryable = summary.get("queryable_relation_count", "—")
    rel_cell = thousands(relations)
    if queryable != relations:
        rel_cell = f"{thousands(queryable)} queryable of {thousands(relations)}"

    licence = summary.get("license") or "—"
    if licence.startswith("http"):
        # The manifests carry a bare URL for upstream terms. Show the host so
        # the cell is readable; the full URL stays in the href.
        host = re.sub(r"^https?://(www\.)?", "", licence).split("/")[0]
        licence = f"[Upstream terms]({licence}) — `{host}`"
    elif len(licence) > 60:
        licence = f"{licence[:57]}..."

    commit = (etl.get("commit_hash") or "")[:10]
    provenance = (
        f"`{etl.get('migration_status', 'unknown')}` "
        f"{str(etl.get('migrated_at'))[:10]}"
        + (f", commit `{commit}`" if commit else "")
    )

    sources = etl.get("source_attribution", []) or []
    if len(sources) == 1:
        name = str(sources[0].get("name") or "").strip()
        # Some manifests record the dataset slug as the source name, which
        # tells a reader nothing. Fall back to the host in that case.
        if not name or name.lower() == slug.lower():
            url = str(sources[0].get("url") or "")
            host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
            name = f"{host} (upstream)"
        source_cell = f"[{name}]({sources[0].get('url')})"
    elif sources:
        source_cell = (
            f"{len(sources)} upstream feeds (see [Data sources](#data-sources))"
        )
    else:
        source_cell = "—"

    rows = [
        ("Collection", f"{collection_info['title']}"),
        (
            "Endpoint",
            f"[`{dataset['api_path']}/`](https://benthic.io{dataset['api_path']}/)",
        ),
        ("OpenAPI", f"[`{dataset['spec']}.json`](/api/{dataset['spec']}.json)"),
        (
            "Manifest",
            f"[`{collection}/{slug}`](https://benthic.io/bdp/{collection}/{slug}/manifest.json)",
        ),
        ("Provenance", provenance),
        ("Relations", rel_cell),
        ("Columns", thousands(summary.get("column_count", "—"))),
        ("Updated", human_cadence(dataset.get("cadence", "—"))),
        ("Licence", licence),
        ("Source", source_cell),
        (
            "Pipeline",
            f"[{pipeline['repo']}/{pipeline['readme']}]"
            f"(https://github.com/benthic-io/{pipeline['repo']}/blob/"
            f"{pipeline.get('branch', 'main')}/{pipeline['readme']})",
        ),
    ]

    out = ["## At a glance", "", "| | |", "|---|---|"]
    for label, value in rows:
        out.append(f"| {label} | {value} |")
    out.append("")
    return "\n".join(out)


def related(dataset: dict, collection_info: dict, all_datasets: list) -> str:
    slug = dataset["slug"]
    siblings = [
        d
        for d in all_datasets
        if d["collection"] == dataset["collection"] and d["slug"] != slug
    ]
    cross = [d for d in all_datasets if d["collection"] != dataset["collection"]]

    out = ["## Related", ""]
    out.append(
        f"- [Swagger explorer](https://benthic.io/swagger/{dataset['swagger_page']}/) "
        f"— interactive API browser for `{dataset['api_path']}`"
    )
    out.append(
        f"- [Signed manifest](https://benthic.io/bdp/{dataset['collection']}/{slug}/manifest.json) "
        f"— every relation, column, and licence, signed with the publisher's "
        f"Ed25519 key"
    )
    out.append(
        f"- [Pipeline README](https://github.com/benthic-io/"
        f"{dataset['pipeline']['repo']}/blob/{dataset['pipeline'].get('branch', 'main')}/"
        f"{dataset['pipeline']['readme']}) — how this dataset is actually built"
    )
    out.append(
        "- [BDP specification](https://benthic.io/bdp/) — what the manifest "
        "signature proves, and how to verify it offline"
    )
    out.append(
        "- [Documentation map](https://benthic.io/docs/map/) — every dataset on "
        "benthic.io and where its documentation lives"
    )
    out.append(
        "- [APIs overview](https://benthic.io/apis/) — join paths between "
        "datasets and worked cross-collection queries"
    )
    if siblings:
        links = ", ".join(
            f"[{d['title']}](https://benthic.io/docs/{d['docs_page']}/)"
            for d in siblings
        )
        out.append(f"- Also in {collection_info['title']}: {links}")
    if cross:
        links = ", ".join(
            f"[{d['title']}](https://benthic.io/docs/{d['docs_page']}/)" for d in cross
        )
        out.append(f"- In {cross[0]['collection'].title()}: {links}")
    out.append("")
    return "\n".join(out)


def find_insertion_point(lines: list[str]) -> int:
    """Index of the first heading that is not the page's URL/description line."""

    for i, line in enumerate(lines):
        m = HEADING.match(line)
        if not m:
            continue
        if URL_HEADING.match(m.group(2).strip()):
            continue
        return i
    return len(lines)


def replace_section(text: str, title: str, body: str) -> str:
    """Replace an existing '## Title' section, or append if absent."""

    pattern = re.compile(rf"^## {re.escape(title)}\s*$", re.M)
    match = pattern.search(text)
    if not match:
        return text.rstrip("\n") + "\n\n" + body

    end = text.find("\n## ", match.end())
    if end == -1:
        end = len(text)
    return text[: match.start()] + body.rstrip("\n") + "\n" + text[end + 1 :]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    registry = load_registry()
    collections = registry.get("collections", {})
    datasets = registry.get("datasets", [])
    drift = 0

    for dataset in datasets:
        slug = dataset["slug"]
        collection = dataset["collection"]
        path = CONTENT / "docs" / f"{dataset['docs_page']}.md"
        if not path.exists():
            print(f"missing reference page: {path}", file=sys.stderr)
            return 1

        facts = manifest_facts(collection, slug)
        info = collections[collection]
        text = path.read_text(encoding="utf-8")

        glance = at_a_glance(dataset, info, facts)
        rel = related(dataset, info, datasets)

        new = replace_section(text, "At a glance", glance)
        new = replace_section(new, "Related", rel)

        if new == text:
            print(f"  ok    {slug}")
            continue

        # When At a glance is newly inserted, place it before the first real
        # section rather than at the end of the file.
        if "## At a glance" not in text:
            lines = text.splitlines()
            at = find_insertion_point(lines)
            block = glance.rstrip("\n").splitlines()
            lines[at:at] = block + [""]
            new = "\n".join(lines) + "\n"
            new = replace_section(new, "Related", rel)

        drift += 1
        if args.check:
            print(f"  STALE {slug}: run without --check")
        else:
            path.write_text(new, encoding="utf-8")
            print(f"  wrote {slug}")

    if args.check and drift:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
