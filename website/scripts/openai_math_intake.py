#!/usr/bin/env python3
"""Render the pinned OpenAI Math intake across all seven reader libraries."""

from __future__ import annotations

import json
import posixpath
import shutil
from collections import Counter
from html import escape
from pathlib import Path

import astis_site


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "research-wiki" / "openai-math-textbook-coverage.json"
INTAKE = ROOT / "research-wiki" / "openai-math-2026-intake.json"
STYLE = ROOT / "website" / "static" / "openai-math-intake.css"
STYLE_NAME = STYLE.name
CENTRAL_PATH = "libraries/openai-math/index.html"
MARKER = 'data-openai-math-intake="1"'
EXPECTED_LIBRARIES = {
    "log-concave-sampling",
    "samplewiki",
    "riemannian-optimization",
    "optimisation",
    "statistical-optimal-transport",
    "discrete-sampling",
    "mcmc",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _load() -> dict:
    model = json.loads(DATA.read_text(encoding="utf-8"))
    _require(model.get("schema_version") == 1, "OpenAI Math coverage schema drift")
    upstream = model.get("upstream", {})
    _require(
        upstream.get("commit") == "adc7f1241b42e322a6451854ab7e4b4c146bf78a",
        "OpenAI Math coverage must remain pinned to the audited release",
    )
    _require(upstream.get("license") == "Apache-2.0", "OpenAI Math license drift")
    _require(upstream.get("catalogue_families") == 372, "OpenAI Math family count drift")
    _require(upstream.get("catalogue_manuscripts") == 722, "OpenAI Math manuscript count drift")

    libraries = model.get("libraries", [])
    library_ids = [entry.get("id") for entry in libraries]
    _require(set(library_ids) == EXPECTED_LIBRARIES, "OpenAI Math map must cover exactly seven reader libraries")
    _require(len(library_ids) == len(set(library_ids)), "duplicate OpenAI Math library id")
    by_library = {entry["id"]: entry for entry in libraries}

    allowed = set(model["truth_contract"]["verification_statuses"])
    items = model.get("items", [])
    item_ids = [item.get("id") for item in items]
    _require(len(items) >= 32, "OpenAI Math domain sweep unexpectedly shrank")
    _require(len(item_ids) == len(set(item_ids)), "duplicate OpenAI Math route id")
    for item in items:
        _require(item.get("verification") in allowed, f'{item.get("id")}: invalid verification status')
        _require(item.get("upstream_paths"), f'{item.get("id")}: upstream path missing')
        _require(item.get("scope_note"), f'{item.get("id")}: scope note missing')
        _require(item.get("placements"), f'{item.get("id")}: placement missing')
        reader = item.get("reader")
        if reader is not None:
            _validate_reader(item)
        for placement in item["placements"]:
            library = placement.get("library")
            _require(library in by_library, f'{item.get("id")}: unknown library {library}')
            _require(placement.get("reason"), f'{item.get("id")}: placement reason missing')
            chapters = placement.get("chapters", [])
            _require(chapters, f'{item.get("id")}: chapter placement missing')
            extensions = by_library[library].get("extended_chapters", {})
            for chapter in chapters:
                if str(chapter).startswith("E"):
                    _require(chapter in extensions, f'{item.get("id")}: unknown extension {library}/{chapter}')

    intake = json.loads(INTAKE.read_text(encoding="utf-8"))
    intake_ids = {cluster["id"] for cluster in intake.get("clusters", [])}
    _require(intake_ids.issubset(set(item_ids)), "an original OpenAI Math intake cluster disappeared")
    _require(
        model["truth_contract"].get("blue_requires_astis_owned_compiled_declaration") is True,
        "external material must not receive a blue ASTIS badge",
    )
    return model


def _validate_reader(item: dict) -> None:
    """Source-only readers cannot promote external evidence into local admission."""
    reader = item["reader"]
    path = reader.get("path", "")
    _require(path.startswith("example-cases/samplewiki/openai-math/")
             and path.endswith(".html") and ".." not in Path(path).parts
             and "\\" not in path, f'{item["id"]}: invalid source-reader path')
    _require(reader.get("status") == "source-reading-draft", "source reader cannot certify local Lean")
    _require(reader.get("review_status") in {"pending", "source-exposition-reviewed"}, "unknown exposition review")
    if reader["review_status"] == "source-exposition-reviewed":
        _require(all(reader.get("review", {}).get(key) for key in ("reviewer", "date", "scope", "accepted_boundary")),
                 "source exposition review needs bounded evidence")
    for key in ("source_blob_sha", "upstream_model_blob_sha", "upstream_main_blob_sha"):
        value = reader.get(key, "")
        _require(len(value) == 40 and all(c in "0123456789abcdef" for c in value), f"missing pinned {key}")
    for key in ("source_path", "source_anchor", "question", "takeaway", "model", "statement",
                "source_comparison", "source_comparison_boundary", "assembly", "lean_statement",
                "lean_proof", "lean_explanation", "next_boundary"):
        _require(bool(reader.get(key)), f'{item["id"]}: reader missing {key}')
    steps = reader.get("steps", [])
    _require(bool(steps), "source reader needs actual mathematical steps")
    ids = [step.get("id") for step in steps]
    _require(len(ids) == len(set(ids)) and all(ids), "reader step ids must be unique")
    for step in steps:
        _require(all(step.get(key) for key in ("title", "anchor", "text", "boundary")), "reader step incomplete")


def _href(current: str, target: str) -> str:
    return posixpath.relpath(target, start=posixpath.dirname(current) or ".")


def _upstream_url(commit: str, path: str) -> str:
    mode = "blob" if Path(path).suffix in {".md", ".lean", ".json", ".yaml", ".yml", ".pdf", ".tex", ".bib"} else "tree"
    return f"https://github.com/openai/math/{mode}/{commit}/{path}"


def _status_label(status: str) -> str:
    return {
        "comparator-backed": "Comparator-backed upstream endpoint",
        "comparator-backed-partial-family": "Comparator-backed, partial family",
        "comparator-doc-linked": "Comparator linked by upstream result note",
        "lean-present-not-comparator-audited": "Lean present; Comparator audit pending",
        "manuscript-only": "Manuscript only in this audit",
    }[status]


def _chapter_label(library: dict, chapter: str) -> str:
    extensions = library.get("extended_chapters", {})
    if chapter in extensions:
        return f"Extended {chapter}: {extensions[chapter]}"
    if chapter == "B":
        return "Appendix B"
    return f"Chapter {chapter}"


def _card(item: dict, model: dict, current: str, focus_library: str | None = None) -> str:
    commit = model["upstream"]["commit"]
    libraries = {entry["id"]: entry for entry in model["libraries"]}
    placements = [p for p in item["placements"] if focus_library is None or p["library"] == focus_library]
    placement_html = "".join(
        '<li><strong>' + escape(libraries[p["library"]]["label"]) + ":</strong> "
        + escape(", ".join(_chapter_label(libraries[p["library"]], str(ch)) for ch in p["chapters"]))
        + " — " + escape(p["reason"]) + "</li>"
        for p in placements
    )
    sources = "".join(
        f'<li><a href="{escape(_upstream_url(commit, path))}"><code>{escape(path)}</code></a></li>'
        for path in item["upstream_paths"]
    )
    declarations = item.get("declarations", [])
    lean = ""
    if declarations:
        lean = (
            '<details class="oai-lean"><summary>Upstream Lean endpoints (external; not callable ASTIS dependencies)</summary><ul>'
            + "".join(f"<li><code>{escape(name)}</code></li>" for name in declarations)
            + "</ul></details>"
        )
    reader_link = ""
    if item.get("reader"):
        reader_link = (f'<p><a class="button primary" href="{escape(_href(current, item["reader"]["path"]))}">'
                       'Read the result and proof ideas</a> <span class="muted">Source guide; local proof remains open</span></p>')
    results = ", ".join(f"{value:03d}" for value in item.get("catalogue_results", [])) or "technical substrate"
    return f'''<article class="oai-route-card" id="{escape(item["id"])}" data-oai-route="{escape(item["id"])}" data-local-proof-status="external-reference">
  <div class="oai-route-meta"><span class="oai-status status-{escape(item["verification"])}">{escape(_status_label(item["verification"]))}</span><span>OpenAI Math result {escape(results)}</span></div>
  <h3>{escape(item["title"])}</h3>
  <p>{escape(item["scope_note"])}</p>
  {reader_link}
  <h4>Samplinglib placement</h4><ul>{placement_html}</ul>
  <details><summary>Pinned upstream paths and provenance</summary><ul>{sources}</ul><p>Apache-2.0 upstream snapshot <code>{escape(commit)}</code>. Presence here is provenance, not local compilation.</p></details>
  {lean}
</article>'''


def _formula(value: str | None) -> str:
    return f'<div class="oai-formula">\\[{escape(value)}\\]</div>' if value else ""


def _reader_page(item: dict, model: dict) -> str:
    reader = item["reader"]
    rel = reader["path"]
    commit = model["upstream"]["commit"]
    source = _upstream_url(commit, reader["source_path"])
    main = _upstream_url(commit, "lean/OAI/Probability/LogConcave/Main.lean")
    review = reader.get("review", {})
    review_html = ""
    if review:
        review_html = ('<details><summary>Independent reading-level review scope</summary><p>'
                       + escape(review["reviewer"] + "; " + review["date"] + ". " + review["scope"])
                       + '</p><p>' + escape(review["accepted_boundary"]) + '</p></details>')
    step_html = "".join(
        f'<article class="oai-proof-step" id="step-{escape(step["id"])}">'
        f'<h3>{index}. {escape(step["title"])}</h3><p>{escape(step["text"])}</p>'
        + _formula(step.get("formula"))
        + f'<p class="oai-open-boundary"><strong>Verification boundary.</strong> {escape(step["boundary"])}</p>'
        + f'<details><summary>Source and Lean status for this step</summary><p>'
          f'<a href="{escape(source)}">Pinned source</a>: {escape(step["anchor"])}. '
          'This step has no admitted ASTIS source binding in this guide; no local Lean proof is fabricated.</p></details></article>'
        for index, step in enumerate(reader["steps"], 1)
    )
    body = f'''<section class="page-hero compact" {MARKER} data-oai-reader="{escape(item["id"])}" data-local-proof-status="external-reference">
  <div class="eyebrow">SampleWiki · result digestion · source-only reading guide</div>
  <h1>{escape(item["title"])}</h1><p class="lede">{escape(reader["question"])}</p>
  <p>{escape(reader["takeaway"])}</p>
  <p><a href="#result">Result</a> · <a href="#contribution">What changes?</a> · <a href="#proof-route">Proof ideas</a> · <a href="#verification">Verification and next step</a></p>
</section>
<section class="oai-truth"><h2>What has been absorbed?</h2>
  <p>The existing intake, chapter placement and external endpoint record are reused. This page adds a mathematical source guide, not an ASTIS theorem. Local source-specific proofs and semantic adapters remain open. Reading-level review is <strong>{escape(reader["review_status"])}</strong>; this is not a Lean compilation or exhaustive source-coverage certificate.</p>
  {review_html}
</section>
<section id="result"><h2>1. The exact problem and result</h2><p>{escape(reader["model"])}</p>
  {_formula(reader.get("model_formula"))}<h3>Main statement — attributed mathematical restatement</h3>
  <p>{escape(reader["statement"])}</p>{_formula(reader.get("statement_formula"))}
  <details class="oai-lean"><summary>Read the upstream Lean statement (external)</summary><p>{escape(reader["lean_explanation"])}</p>
    <pre><code class="language-lean">{escape(reader["lean_statement"])}</code></pre><p><a href="{escape(main)}">Exact upstream module</a>; not an ASTIS import.</p></details>
</section>
<section id="contribution"><h2>2. What mathematics does this add?</h2><p>{escape(reader["source_comparison"])}</p>
  <p class="oai-open-boundary">{escape(reader["source_comparison_boundary"])}</p>
</section>
<section id="proof-route"><h2>3. Follow the proof ideas</h2><p>The first five moves summarize the upper route; the information lower bound is a separate route. These are reading summaries, not a claim that every source paragraph is covered or locally verified.</p>{step_html}
  <article class="oai-proof-step"><h3>Assemble the final statement</h3><p>{escape(reader["assembly"])}</p>
    <details class="oai-lean"><summary>Read the upstream assembly proof (external)</summary>
    <pre><code class="language-lean">{escape(reader["lean_proof"])}</code></pre><p>{escape(reader["lean_explanation"])}</p></details>
  </article>
</section>
<section id="verification"><h2>4. Where Lean comes next</h2><p>{escape(reader["next_boundary"])}</p>
  <p><a href="{escape(_href(rel, CENTRAL_PATH))}#oai-logconcave">Existing intake and seven-library placement</a> · <a href="{escape(source)}">Pinned manuscript source</a></p>
  <details><summary>Source provenance and attribution</summary><p>OpenAI, <em>Subpolynomial query complexity for well-conditioned log-concave sampling</em>, September 26, 2026. ASTIS-authored explanation, not reproduced manuscript prose. Source anchor: {escape(reader["source_anchor"])}.</p>
    <p>Snapshot {escape(commit)}; introduction blob {escape(reader["source_blob_sha"])}; upstream Model blob {escape(reader["upstream_model_blob_sha"])}; Main blob {escape(reader["upstream_main_blob_sha"])}. The displayed Lean excerpts retain upstream Apache-2.0 provenance. No author endorsement is implied.</p>
  </details>
</section>'''
    return _page(item["title"], rel, body)


def _page(title: str, rel: str, body: str) -> str:
    text = astis_site.page(
        title,
        rel,
        body,
        active="Libraries",
        description="Pinned OpenAI Math source routes mapped to Samplinglib textbook and research libraries.",
    )
    prefix = "../" * len(Path(rel).parent.parts)
    return text.replace("</head>", f'  <link rel="stylesheet" href="{prefix}assets/{STYLE_NAME}">\n</head>', 1)


def _central(model: dict) -> str:
    rel = CENTRAL_PATH
    counts = Counter(p["library"] for item in model["items"] for p in item["placements"])
    library_links = "".join(
        f'<a class="oai-library-chip" href="{escape(_href(rel, lib["extension_path"]))}"><strong>{escape(lib["label"])}</strong><span>{counts[lib["id"]]} mapped routes</span></a>'
        for lib in model["libraries"]
    )
    cards = "".join(_card(item, model, rel) for item in model["items"])
    exclusions = "".join(
        f'<li><strong>{entry["catalogue_result"]:03d}. {escape(entry["title"])}</strong> — {escape(entry["reason"])}</li>'
        for entry in model.get("explicit_non_intake_examples", [])
    )
    upstream = model["upstream"]
    body = f'''<section class="page-hero compact" {MARKER}>
  <div class="eyebrow">External proof memory · seven-library coverage</div>
  <h1>OpenAI Math intake map</h1>
  <p class="lede">A pinned, truth-preserving map from relevant OpenAI Math result families into Samplinglib's seven textbook and research libraries. It tells readers where a route belongs without claiming that upstream Lean is ASTIS-owned Lean.</p>
  <div class="oai-summary"><span><strong>{len(model["items"])}</strong> domain routes</span><span><strong>{len(model["libraries"])}</strong> libraries</span><span><strong>{upstream["catalogue_families"]}</strong> upstream families audited</span><span><strong>{upstream["formalization_manifest_main_results"]}</strong> manifest endpoints inspected</span></div>
  <p><a class="button primary" href="https://github.com/openai/math/tree/{escape(upstream["commit"])}">Pinned upstream snapshot</a> <a class="button" href="{escape(_href(rel, "attribution/index.html"))}">Attribution and licenses</a></p>
</section>
<section class="oai-truth"><h2>How to read the status</h2><p>Every card is an <strong>external reference</strong>. Comparator-backed means that a named endpoint is exposed by the audited upstream verification material; it does not create a solid edge in Samplinglib's Lean graph. Only an ASTIS-owned declaration that compiles locally may become blue.</p></section>
<section><div class="section-heading"><span>Place by consumer, not keyword</span><h2>Seven library shelves</h2></div><div class="oai-library-grid">{library_links}</div></section>
<section><div class="section-heading"><span>Audited domain sweep</span><h2>Relevant result and substrate routes</h2></div><div class="oai-route-grid">{cards}</div></section>
<section class="oai-exclusions"><div class="section-heading"><span>Negative classification evidence</span><h2>Similar words do not imply the same mathematics</h2></div><ul>{exclusions}</ul></section>'''
    return _page("OpenAI Math intake map", rel, body)


def _library_page(model: dict, library: dict) -> str:
    rel = library["extension_path"]
    items = [item for item in model["items"] if any(p["library"] == library["id"] for p in item["placements"])]
    extensions = "".join(
        f'<li><strong>{escape(key)}</strong> — {escape(value)} <span class="muted">(Samplinglib extension; not a source-text chapter)</span></li>'
        for key, value in library.get("extended_chapters", {}).items()
    )
    cards = "".join(_card(item, model, rel, library["id"]) for item in items)
    body = f'''<section class="page-hero compact" {MARKER} data-oai-library="{escape(library["id"])}">
  <div class="eyebrow">{escape(library["label"])} · external extension shelf</div>
  <h1>OpenAI Math routes for {escape(library["label"])}</h1>
  <p class="lede">These routes are placed beside the chapters that can explain or consume them. They do not alter the primary source's chapter numbering, and they remain external until a reviewed ASTIS adapter or theorem compiles.</p>
  <p><a class="button primary" href="{escape(_href(rel, library["index_path"]))}">Back to {escape(library["label"])}</a> <a class="button" href="{escape(_href(rel, CENTRAL_PATH))}">All seven libraries</a></p>
</section>
<section class="oai-truth"><h2>Extended chapters</h2><ul>{extensions}</ul></section>
<section><div class="section-heading"><span>{len(items)} mapped routes</span><h2>Chapter and extension placement</h2></div><div class="oai-route-grid">{cards}</div></section>'''
    return _page(f"OpenAI Math · {library['label']}", rel, body)


def _patch_index(output: Path, library: dict, count: int) -> None:
    path = output / library["index_path"]
    _require(path.exists(), f'missing library index: {library["index_path"]}')
    text = path.read_text(encoding="utf-8")
    marker = f'data-oai-index="{library["id"]}"'
    if marker in text:
        return
    href = _href(library["index_path"], library["extension_path"])
    central = _href(library["index_path"], CENTRAL_PATH)
    card = f'''<section class="oai-index-card" {marker}>
  <div><span class="eyebrow">Pinned external proof memory</span><h2>OpenAI Math extension shelf</h2><p>{count} audited upstream routes are placed beside this library's real chapters or named Samplinglib extensions. External verification is shown separately from ASTIS compilation.</p></div>
  <p><a class="button primary" href="{escape(href)}">Open this library's map</a> <a class="button" href="{escape(central)}">See all seven</a></p>
</section>'''
    _require("</main>" in text, f'{library["index_path"]}: main element missing')
    text = text.replace("</main>", card + "\n</main>", 1)
    path.write_text(text, encoding="utf-8", newline="\n")


def _inherit_library_shell(output: Path, rel: str) -> None:
    """Apply the canonical seven-library shell to one newly generated page."""
    import library_shelves

    path = output / rel
    text = path.read_text(encoding="utf-8")
    text = library_shelves.replace_sidebar(text, rel)
    text = library_shelves.inherit_canonical_theme(text, rel, output)
    text = library_shelves.add_style(text, rel)
    path.write_text(text, encoding="utf-8", newline="\n")


def enrich_site(output: Path) -> None:
    model = _load()
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(STYLE, assets / STYLE_NAME)
    astis_site.write_page(output, CENTRAL_PATH, _central(model))
    _inherit_library_shell(output, CENTRAL_PATH)
    for item in model["items"]:
        if item.get("reader"):
            rel = item["reader"]["path"]
            astis_site.write_page(output, rel, _reader_page(item, model))
            _inherit_library_shell(output, rel)
    counts = Counter(p["library"] for item in model["items"] for p in item["placements"])
    for library in model["libraries"]:
        astis_site.write_page(output, library["extension_path"], _library_page(model, library))
        _inherit_library_shell(output, library["extension_path"])
        _patch_index(output, library, counts[library["id"]])


def validate_site(output: Path) -> list[str]:
    errors: list[str] = []
    try:
        model = _load()
    except Exception as exc:
        return [str(exc)]
    expected_pages = ([CENTRAL_PATH] + [entry["extension_path"] for entry in model["libraries"]]
                      + [item["reader"]["path"] for item in model["items"] if item.get("reader")])
    for rel in expected_pages:
        path = output / rel
        if not path.exists():
            errors.append(f"OpenAI Math page missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        if MARKER not in text:
            errors.append(f"OpenAI Math marker missing: {rel}")
        if 'data-status="compiled"' in text or 'data-local-proof-status="compiled"' in text:
            errors.append(f"external OpenAI Math material mislabelled compiled: {rel}")
    central = (output / CENTRAL_PATH).read_text(encoding="utf-8") if (output / CENTRAL_PATH).exists() else ""
    for item in model["items"]:
        if item.get("reader"):
            path = output / item["reader"]["path"]
            if path.exists():
                html = path.read_text(encoding="utf-8")
                for marker in ('id="result"', 'id="contribution"', 'id="proof-route"', 'id="verification"',
                               'data-local-proof-status="external-reference"', 'class="language-lean"'):
                    if marker not in html:
                        errors.append(f"{path.name}: missing source-reader marker {marker}")
        if f'data-oai-route="{item["id"]}"' not in central:
            errors.append(f'OpenAI Math central page lost {item["id"]}')
        for placement in item["placements"]:
            library = next(entry for entry in model["libraries"] if entry["id"] == placement["library"])
            page = output / library["extension_path"]
            if page.exists() and f'data-oai-route="{item["id"]}"' not in page.read_text(encoding="utf-8"):
                errors.append(f'{library["extension_path"]}: missing {item["id"]}')
    for library in model["libraries"]:
        path = output / library["index_path"]
        if not path.exists() or f'data-oai-index="{library["id"]}"' not in path.read_text(encoding="utf-8"):
            errors.append(f'{library["index_path"]}: OpenAI Math shelf link missing')
    return errors
