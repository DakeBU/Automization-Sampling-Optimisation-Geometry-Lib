#!/usr/bin/env python3
"""Deterministically fingerprint the live SampleWiki source for ASTIS.

The watcher is intentionally not a prose mirror. It records same-origin page
structure, bounded headings, semantic-block metadata, and hashes so source
changes become reviewable Git diffs before mathematical cases are admitted into
the ASTIS Lean graph.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

ROOT_URL = "https://samplewiki.morning-recipe-422a.workers.dev/"
SOURCE_ID = "SAMPLEWIKI"
CRAWLER_VERSION = 1
DEFAULT_OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "research-wiki"
    / "source-index"
    / "SampleWiki_manifest.json"
)
USER_AGENT = (
    "ASTIS-SampleWiki-Watcher/1.0 "
    "(+https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib)"
)
SEMANTIC_KEYWORDS = (
    "problem",
    "theorem",
    "lemma",
    "proposition",
    "corollary",
    "example",
    "exercise",
    "proof",
    "claim",
)
SKIP_EXTENSIONS = {
    ".7z",
    ".avi",
    ".css",
    ".csv",
    ".doc",
    ".docx",
    ".gif",
    ".gz",
    ".ico",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".m4a",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".svg",
    ".tar",
    ".tgz",
    ".wav",
    ".webm",
    ".webp",
    ".xls",
    ".xlsx",
    ".xml",
    ".zip",
}
SPACE_RE = re.compile(r"\s+")
KEYWORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(value) for value in SEMANTIC_KEYWORDS) + r")\b",
    flags=re.IGNORECASE,
)


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize_text(value: str) -> str:
    return SPACE_RE.sub(" ", value).strip()


def bounded_text(value: str, limit: int) -> str:
    value = normalize_text(value)
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"


def canonicalize(url: str, *, base: str = ROOT_URL) -> str | None:
    absolute = urllib.parse.urljoin(base, url)
    parsed = urllib.parse.urlsplit(absolute)
    root = urllib.parse.urlsplit(ROOT_URL)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc.lower() != root.netloc.lower():
        return None
    path = parsed.path or "/"
    # Preserve query-string routes, but remove fragments: block anchors are
    # represented separately by semantic-block metadata.
    query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query.sort()
    normalized_query = urllib.parse.urlencode(query)
    normalized = urllib.parse.urlunsplit(
        (root.scheme, root.netloc, path, normalized_query, "")
    )
    suffix = Path(path).suffix.lower()
    if suffix in SKIP_EXTENSIONS:
        return None
    return normalized


@dataclass
class SemanticCapture:
    kind: str
    anchor: str
    depth: int
    ordinal: int
    text_parts: list[str] = field(default_factory=list)


class PageParser(HTMLParser):
    def __init__(self, page_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.page_url = page_url
        self.depth = 0
        self.skip_depth = 0
        self.title_depth = 0
        self.heading_level = ""
        self.heading_depth = 0
        self.heading_parts: list[str] = []
        self.title_parts: list[str] = []
        self.visible_parts: list[str] = []
        self.links: set[str] = set()
        self.headings: list[dict[str, str]] = []
        self.active_captures: list[SemanticCapture] = []
        self.semantic_blocks: list[dict[str, object]] = []
        self.kind_ordinals: dict[str, int] = {}

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): value or "" for key, value in attrs}

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        self.depth += 1
        attrs_map = self._attrs(attrs)

        if tag in {"script", "style", "noscript", "svg", "template"}:
            self.skip_depth += 1

        if tag == "title":
            self.title_depth = self.depth

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_level = tag
            self.heading_depth = self.depth
            self.heading_parts = []

        if tag == "a":
            href = attrs_map.get("href", "")
            candidate = canonicalize(href, base=self.page_url)
            if candidate:
                self.links.add(candidate)

        semantic_blob = " ".join(
            (
                attrs_map.get("id", ""),
                attrs_map.get("class", ""),
                attrs_map.get("role", ""),
                attrs_map.get("data-type", ""),
                attrs_map.get("data-kind", ""),
            )
        )
        match = KEYWORD_RE.search(semantic_blob)
        if match:
            kind = match.group(1).lower()
            ordinal = self.kind_ordinals.get(kind, 0) + 1
            self.kind_ordinals[kind] = ordinal
            self.active_captures.append(
                SemanticCapture(
                    kind=kind,
                    anchor=attrs_map.get("id", ""),
                    depth=self.depth,
                    ordinal=ordinal,
                )
            )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        cleaned = normalize_text(data)
        if not cleaned:
            return
        self.visible_parts.append(cleaned)
        if self.title_depth:
            self.title_parts.append(cleaned)
        if self.heading_depth:
            self.heading_parts.append(cleaned)
        for capture in self.active_captures:
            capture.text_parts.append(cleaned)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()

        closing = [
            capture
            for capture in self.active_captures
            if capture.depth == self.depth
        ]
        for capture in closing:
            full_text = normalize_text(" ".join(capture.text_parts))
            if full_text:
                stable_suffix = (
                    f"#{capture.anchor}"
                    if capture.anchor
                    else f"::{capture.kind}::{capture.ordinal}"
                )
                self.semantic_blocks.append(
                    {
                        "id": "SWBLOCK-"
                        + sha256_text(self.page_url + stable_suffix)[:16],
                        "kind": capture.kind,
                        "anchor": capture.anchor,
                        "text_sha256": sha256_text(full_text),
                        "char_count": len(full_text),
                    }
                )
            self.active_captures.remove(capture)

        if self.heading_depth == self.depth and tag == self.heading_level:
            text = bounded_text(" ".join(self.heading_parts), 180)
            if text:
                self.headings.append({"level": tag, "text": text})
            self.heading_level = ""
            self.heading_depth = 0
            self.heading_parts = []

        if self.title_depth == self.depth and tag == "title":
            self.title_depth = 0

        if tag in {"script", "style", "noscript", "svg", "template"}:
            self.skip_depth = max(0, self.skip_depth - 1)

        self.depth = max(0, self.depth - 1)

    def finish(self) -> dict[str, object]:
        visible_text = normalize_text(" ".join(self.visible_parts))
        title = bounded_text(" ".join(self.title_parts), 180)
        heading_blob = " ".join(item["text"] for item in self.headings)
        discovery_blob = " ".join((self.page_url, title, heading_blob))
        candidate_kinds = sorted(
            {match.group(1).lower() for match in KEYWORD_RE.finditer(discovery_blob)}
            | {str(block["kind"]) for block in self.semantic_blocks}
        )
        return {
            "title": title,
            "headings": self.headings[:40],
            "visible_text_sha256": sha256_text(visible_text),
            "visible_char_count": len(visible_text),
            "candidate_kinds": candidate_kinds,
            "semantic_blocks": sorted(
                self.semantic_blocks,
                key=lambda block: (str(block["kind"]), str(block["id"])),
            ),
            "links": sorted(self.links),
        }


def request_bytes(url: str, *, timeout: float) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.2",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        payload = response.read(6_000_000)
    return payload, content_type


def decode_html(payload: bytes, content_type: str) -> str:
    charset_match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type)
    charset = charset_match.group(1) if charset_match else "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")


def sitemap_urls(*, timeout: float) -> list[str]:
    sitemap_url = urllib.parse.urljoin(ROOT_URL, "/sitemap.xml")
    try:
        payload, _ = request_bytes(sitemap_url, timeout=timeout)
    except urllib.error.HTTPError as error:
        if error.code in {404, 410}:
            return []
        raise
    except urllib.error.URLError:
        return []
    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        return []
    values: set[str] = set()
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1].lower() != "loc" or not element.text:
            continue
        url = canonicalize(element.text)
        if url:
            values.add(url)
    return sorted(values)


def fetch_page(url: str, *, timeout: float) -> tuple[dict[str, object], list[str]]:
    payload, content_type = request_bytes(url, timeout=timeout)
    if "html" not in content_type.lower() and not payload.lstrip().startswith(b"<"):
        raise ValueError(f"non-HTML response for {url}: {content_type}")
    html_text = decode_html(payload, content_type)
    parser = PageParser(url)
    parser.feed(html_text)
    parser.close()
    parsed = parser.finish()
    record = {
        "id": "SWPAGE-" + sha256_text(url)[:16],
        "url": url,
        "title": parsed["title"],
        "html_sha256": hashlib.sha256(payload).hexdigest(),
        "visible_text_sha256": parsed["visible_text_sha256"],
        "visible_char_count": parsed["visible_char_count"],
        "headings": parsed["headings"],
        "candidate_kinds": parsed["candidate_kinds"],
        "semantic_blocks": parsed["semantic_blocks"],
        "links": parsed["links"],
    }
    return record, list(parsed["links"])


def crawl(*, max_pages: int, timeout: float, delay: float) -> dict[str, object]:
    root = canonicalize(ROOT_URL)
    assert root is not None
    seeds = [root]
    for url in sitemap_urls(timeout=timeout):
        if url not in seeds:
            seeds.append(url)

    queue: deque[str] = deque(seeds)
    queued = set(seeds)
    visited: set[str] = set()
    pages: list[dict[str, object]] = []

    while queue and len(pages) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        try:
            record, links = fetch_page(url, timeout=timeout)
        except urllib.error.HTTPError as error:
            if error.code in {404, 410} and url != root:
                continue
            raise RuntimeError(f"HTTP {error.code} while crawling {url}") from error
        except (urllib.error.URLError, TimeoutError, ValueError) as error:
            raise RuntimeError(f"failed to crawl {url}: {error}") from error
        pages.append(record)
        for link in links:
            if link not in visited and link not in queued:
                queued.add(link)
                queue.append(link)
        if delay > 0:
            time.sleep(delay)

    pages.sort(key=lambda page: str(page["url"]))
    tree_payload = {
        "source_id": SOURCE_ID,
        "root_url": ROOT_URL,
        "crawler_version": CRAWLER_VERSION,
        "truncated": bool(queue),
        "pages": pages,
    }
    tree_sha256 = sha256_text(
        json.dumps(tree_payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    )
    semantic_block_count = sum(len(page["semantic_blocks"]) for page in pages)
    candidate_page_count = sum(bool(page["candidate_kinds"]) for page in pages)
    return {
        "schema_version": 1,
        "source_id": SOURCE_ID,
        "root_url": ROOT_URL,
        "crawler_version": CRAWLER_VERSION,
        "snapshot_policy": "structural metadata and fingerprints; no wholesale prose mirror",
        "truncated": bool(queue),
        "page_count": len(pages),
        "candidate_page_count": candidate_page_count,
        "semantic_block_count": semantic_block_count,
        "tree_sha256": tree_sha256,
        "pages": pages,
    }


def load_existing(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"existing manifest is not an object: {path}")
    return raw


def summarize_diff(
    previous: dict[str, object] | None, current: dict[str, object]
) -> dict[str, object]:
    if previous is None:
        return {
            "first_snapshot": True,
            "added_pages": current["page_count"],
            "removed_pages": 0,
            "changed_pages": 0,
        }
    previous_pages = {
        str(page["url"]): page for page in previous.get("pages", []) if isinstance(page, dict)
    }
    current_pages = {
        str(page["url"]): page for page in current.get("pages", []) if isinstance(page, dict)
    }
    common = previous_pages.keys() & current_pages.keys()
    changed = sum(
        previous_pages[url].get("html_sha256") != current_pages[url].get("html_sha256")
        or previous_pages[url].get("visible_text_sha256")
        != current_pages[url].get("visible_text_sha256")
        for url in common
    )
    return {
        "first_snapshot": False,
        "added_pages": len(current_pages.keys() - previous_pages.keys()),
        "removed_pages": len(previous_pages.keys() - current_pages.keys()),
        "changed_pages": changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write the manifest")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--max-pages", type=int, default=500)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--delay", type=float, default=0.05)
    args = parser.parse_args()

    if args.max_pages <= 0:
        parser.error("--max-pages must be positive")
    output = Path(args.output)
    previous = load_existing(output)

    try:
        current = crawl(
            max_pages=args.max_pages,
            timeout=args.timeout,
            delay=args.delay,
        )
    except Exception as error:
        print(f"SampleWiki source crawl failed: {error}", file=sys.stderr)
        return 2

    diff = summarize_diff(previous, current)
    print(
        "SampleWiki snapshot:",
        f"pages={current['page_count']}",
        f"candidate_pages={current['candidate_page_count']}",
        f"semantic_blocks={current['semantic_block_count']}",
        f"tree={str(current['tree_sha256'])[:16]}",
    )
    print("Source diff:", json.dumps(diff, sort_keys=True))

    if current["truncated"]:
        print(
            f"warning: crawl reached --max-pages={args.max_pages}; manifest is marked truncated",
            file=sys.stderr,
        )

    if not args.write:
        return 0

    serialized = json.dumps(current, indent=2, ensure_ascii=False) + "\n"
    old_text = output.read_text(encoding="utf-8") if output.exists() else ""
    if old_text == serialized:
        print("SampleWiki manifest unchanged.")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(serialized, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
