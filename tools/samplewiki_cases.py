#!/usr/bin/env python3
"""Extract SampleWiki comparison-table rows into ASTIS case candidates.

The case manifest is deliberately provenance-heavy and prose-light.  It keeps
short row identity fields, mathematical headline cells, source links, and
cryptographic fingerprints.  Long explanatory source prose is represented by a
hash and must be rewritten as an original ASTIS source card during semantic
review.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT_URL = "https://samplewiki.morning-recipe-422a.workers.dev/"
SOURCE_ID = "SAMPLEWIKI"
CASE_SCHEMA_VERSION = 1
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "research-wiki"
    / "source-index"
    / "SampleWiki_cases.json"
)
USER_AGENT = (
    "ASTIS-SampleWiki-CaseExtractor/1.0 "
    "(+https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib)"
)
SETTING_SLUGS = (
    "setting-convex-body-membership",
    "setting-functional-inequality-smooth",
    "setting-holder-smooth-log-concave",
    "setting-log-concave-smooth",
    "setting-nonlogconcave-fisher",
    "setting-stochastic-finite-sum",
    "setting-strongly-log-concave-smooth",
)
EXPECTED_COLUMNS = (
    "Result",
    "Algorithm or model",
    "Complexity",
    "Guarantee",
    "Oracle / start",
    "Assumptions and notes",
    "Review",
    "Sources",
)
SPACE_RE = re.compile(r"\s+")
SLUG_RE = re.compile(r"[^a-z0-9]+")


def normalize_text(value: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(value)).strip()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    value = SLUG_RE.sub("-", normalize_text(value).lower()).strip("-")
    return value or "row"


def same_origin_url(href: str, base: str) -> str:
    return urllib.parse.urljoin(base, href)


@dataclass
class LinkRecord:
    label_parts: list[str] = field(default_factory=list)
    href: str = ""


@dataclass
class CellRecord:
    tag: str
    text_parts: list[str] = field(default_factory=list)
    links: list[LinkRecord] = field(default_factory=list)
    active_link: LinkRecord | None = None


class TableParser(HTMLParser):
    """Minimal table parser preserving text plus cell-local links."""

    def __init__(self, page_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.table_depth = 0
        self.row_depth = 0
        self.cell_depth = 0
        self.current_row: list[CellRecord] | None = None
        self.current_cell: CellRecord | None = None
        self.rows: list[list[CellRecord]] = []
        self.h1_depth = 0
        self.h1_parts: list[str] = []

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): value or "" for key, value in attrs}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        if tag == "h1" and not self.h1_depth:
            self.h1_depth = 1
            self.h1_parts = []
            return
        if self.h1_depth:
            self.h1_depth += 1

        if tag == "table":
            self.table_depth += 1
            return
        if not self.table_depth:
            return
        if tag == "tr":
            self.row_depth += 1
            if self.row_depth == 1:
                self.current_row = []
            return
        if self.current_row is None:
            return
        if tag in {"th", "td"}:
            self.cell_depth += 1
            if self.cell_depth == 1:
                self.current_cell = CellRecord(tag=tag)
            return
        if self.current_cell is not None and tag == "a":
            href = self.attrs_dict(attrs).get("href", "")
            link = LinkRecord(href=same_origin_url(href, self.page_url))
            self.current_cell.links.append(link)
            self.current_cell.active_link = link

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        cleaned = normalize_text(data)
        if not cleaned:
            return
        if self.h1_depth:
            self.h1_parts.append(cleaned)
        if self.current_cell is not None:
            self.current_cell.text_parts.append(cleaned)
            if self.current_cell.active_link is not None:
                self.current_cell.active_link.label_parts.append(cleaned)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self.current_cell is not None and tag == "a":
            self.current_cell.active_link = None

        if tag in {"th", "td"} and self.cell_depth:
            if self.cell_depth == 1 and self.current_cell is not None:
                assert self.current_row is not None
                self.current_row.append(self.current_cell)
                self.current_cell = None
            self.cell_depth -= 1

        if tag == "tr" and self.row_depth:
            if self.row_depth == 1 and self.current_row is not None:
                if self.current_row:
                    self.rows.append(self.current_row)
                self.current_row = None
            self.row_depth -= 1

        if tag == "table" and self.table_depth:
            self.table_depth -= 1

        if self.h1_depth:
            self.h1_depth -= 1

    @property
    def title(self) -> str:
        return normalize_text(" ".join(self.h1_parts))


def fetch_html(url: str, timeout: float) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.2",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read(6_000_000)
        content_type = response.headers.get("Content-Type", "")
    match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type)
    encoding = match.group(1) if match else "utf-8"
    try:
        return payload.decode(encoding, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def cell_text(cell: CellRecord) -> str:
    return normalize_text(" ".join(cell.text_parts))


def cell_links(cell: CellRecord) -> list[dict[str, str]]:
    values: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for link in cell.links:
        label = normalize_text(" ".join(link.label_parts)).removesuffix("↗").strip()
        href = link.href.strip()
        if not href:
            continue
        key = (label, href)
        if key in seen:
            continue
        seen.add(key)
        values.append({"label": label, "url": href})
    return values


def parse_setting(slug: str, timeout: float) -> tuple[dict[str, object], list[dict[str, object]]]:
    page_url = urllib.parse.urljoin(ROOT_URL, f"/wiki/{slug}")
    source = fetch_html(page_url, timeout)
    parser = TableParser(page_url)
    parser.feed(source)
    parser.close()
    if not parser.rows:
        raise RuntimeError(f"no comparison table found at {page_url}")

    header = tuple(cell_text(cell) for cell in parser.rows[0])
    if header != EXPECTED_COLUMNS:
        raise RuntimeError(
            f"comparison-table schema changed at {page_url}: {header!r}"
        )

    page_meta: dict[str, object] = {
        "setting_slug": slug,
        "source_page": page_url,
        "setting_title": parser.title,
        "row_count": max(0, len(parser.rows) - 1),
        "table_sha256": sha256_text(
            "\n".join("\u241f".join(cell_text(cell) for cell in row) for row in parser.rows)
        ),
    }

    cases: list[dict[str, object]] = []
    identity_counts: dict[str, int] = {}
    for row_index, row in enumerate(parser.rows[1:], start=1):
        if len(row) != len(EXPECTED_COLUMNS):
            raise RuntimeError(
                f"unexpected {len(row)}-cell row {row_index} at {page_url}"
            )
        values = [cell_text(cell) for cell in row]
        (
            result_class,
            algorithm_model,
            complexity,
            guarantee,
            oracle_start,
            assumptions_notes,
            review_state,
            _sources_text,
        ) = values
        identity_base = f"{slug}:{slugify(result_class)}:{slugify(algorithm_model)}"
        ordinal = identity_counts.get(identity_base, 0) + 1
        identity_counts[identity_base] = ordinal
        identity_key = identity_base if ordinal == 1 else f"{identity_base}:{ordinal}"
        case_id = "ASTIS-SW-" + slugify(identity_key).upper()
        row_payload = "\u241f".join(values)
        source_refs = cell_links(row[-1])
        cases.append(
            {
                "id": case_id,
                "source_id": SOURCE_ID,
                "setting_slug": slug,
                "setting_title": parser.title,
                "source_page": page_url,
                "source_row": row_index,
                "result_class": result_class,
                "algorithm_or_model": algorithm_model,
                "complexity": complexity,
                "guarantee": guarantee,
                "review_state": review_state,
                "source_refs": source_refs,
                "oracle_start_sha256": sha256_text(oracle_start),
                "assumptions_notes_sha256": sha256_text(assumptions_notes),
                "row_sha256": sha256_text(row_payload),
                "verification_stage": "sourcePinned",
                "astis_restatement": None,
                "lean_declarations": [],
                "proof_techniques": [],
                "dependency_status": "untriaged",
            }
        )
    return page_meta, cases


def build_manifest(timeout: float) -> dict[str, object]:
    pages: list[dict[str, object]] = []
    cases: list[dict[str, object]] = []
    for slug in SETTING_SLUGS:
        page_meta, page_cases = parse_setting(slug, timeout)
        pages.append(page_meta)
        cases.extend(page_cases)

    ids = [str(case["id"]) for case in cases]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate SampleWiki case IDs detected")

    payload = {
        "schema_version": CASE_SCHEMA_VERSION,
        "source_id": SOURCE_ID,
        "root_url": ROOT_URL,
        "case_unit": "comparison-table row",
        "truth_boundary": (
            "sourcePinned candidates are not Lean-verified or semantically reviewed"
        ),
        "setting_count": len(pages),
        "case_count": len(cases),
        "pages": pages,
        "cases": cases,
    }
    fingerprint_payload = json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    payload["case_tree_sha256"] = sha256_text(fingerprint_payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    output = Path(args.output)
    try:
        manifest = build_manifest(args.timeout)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, RuntimeError) as error:
        print(f"SampleWiki case extraction failed: {error}", file=sys.stderr)
        return 2

    print(
        "SampleWiki cases:",
        f"settings={manifest['setting_count']}",
        f"cases={manifest['case_count']}",
        f"tree={str(manifest['case_tree_sha256'])[:16]}",
    )
    by_setting: dict[str, int] = {}
    for case in manifest["cases"]:
        slug = str(case["setting_slug"])
        by_setting[slug] = by_setting.get(slug, 0) + 1
    print("Cases by setting:", json.dumps(by_setting, sort_keys=True))

    if not args.write:
        return 0
    serialized = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    old = output.read_text(encoding="utf-8") if output.exists() else ""
    if serialized == old:
        print("SampleWiki case manifest unchanged.")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialized, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
