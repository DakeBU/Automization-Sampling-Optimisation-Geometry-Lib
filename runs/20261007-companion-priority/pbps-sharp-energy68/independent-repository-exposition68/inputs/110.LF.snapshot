#!/usr/bin/env python3
"""Generate the interactive Overview/Lean/Functor/source-fidelity evidence graph."""

from __future__ import annotations

import json
import re
import shutil
import sys
from html import escape
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))

from underlying_lean_graph_frontier import add_frontier
from underlying_lean_graph_model import (
    AUDITS,
    CASES,
    CSS,
    DATA,
    DEFAULT_OUTPUT,
    JS,
    LABEL,
    PAGE,
    ROOTS,
    SEMANTIC_CSS,
    SEMANTIC_REGISTRY,
    GraphBuilder,
    load,
)
from underlying_lean_graph_semantic import add_semantic
from underlying_lean_graph_textbook import add_textbook
import cross_domain
import sampling_perspectives
import samplewiki_companions
import publication_reader


def build_graph(output: Path) -> dict[str, Any]:
    site = load(output / "data/site-data.json")
    manifest = load(CASES)
    audit_registry = load(AUDITS)
    semantic_registry = load(SEMANTIC_REGISTRY)
    builder = GraphBuilder()
    textbook = add_textbook(builder, site)
    setting_ids = add_frontier(builder, manifest, audit_registry, textbook["chapter_ids"])
    # Publication mappings can introduce reviewed declarations that are not
    # Registry headline nodes.  Add those declaration nodes before semantic
    # audits so every accepted audit can attach to its actual Lean target.
    publication_reader.project_graph(builder)
    semantic = add_semantic(builder, semantic_registry)
    functor = cross_domain.add_to_graph(builder)
    memory = cross_domain.load(cross_domain.GRAPH_MEMORY_PATH)
    companion_counts = samplewiki_companions.add_to_graph(builder)
    scope_metadata = sampling_perspectives.apply_to_graph(builder)
    # Re-project after all chapter/frontier overlays so their final progress
    # badges and source-correspondence edges use the completed graph.
    publication_reader.project_graph(builder)
    graph = builder.export()
    graph["library_scope_metadata"] = scope_metadata
    graph["companion_frontiers"] = companion_counts
    graph["schema_version"] = 3
    graph['reference_contract'] = 'Name-scanned references are incomplete signals, not elaborated proof dependencies.'
    graph['publication_inputs_sha256'] = publication_reader.graph_input_digest()
    graph["hyperedges"] = functor["hyperedges"]
    graph["conceptual_transport_contract"] = functor["certification_policy"]
    graph["graph_memory_index"] = {
        "path": "website/content/graph_memory_index.json",
        "family_ids": [row["id"] for row in memory["families"]],
        "view_contracts": memory["views"],
    }
    graph["counts"] = {
        "conceptual_domains": len(functor["objects"]),
        "conceptual_hyperedges": len(functor["hyperedges"]),
        "conceptual_families": len(memory["families"]),
        "peer_library_chapter_scaffolds": sum(n["kind"] == "library-chapter" for n in builder.nodes.values()),
        "chapters": len(textbook["chapter_ids"]),
        "samplewiki_settings": len(setting_ids),
        "samplewiki_cases": len(manifest.get("cases", [])),
        "source_claims": len(textbook["source_ids"]),
        "lean_modules": len(textbook["module_ids"]),
        "registry_declarations": len(textbook["registry"]),
        "proof_roots": len(ROOTS),
        "semantic_protocol_nodes": semantic["protocol_nodes"],
        "semantic_audits": semantic["audits"],
        "repair_proposals": semantic["repair_proposals"],
        "accepted_repairs": semantic["accepted_repairs"],
        "nodes": len(builder.nodes),
        "edges": len(builder.edges),
    }
    return graph


def main_html(counts: dict[str, Any]) -> str:
    return f'''
<section class="ulg-hero" data-underlying-lean-graph data-graph-source="{DATA}">
  <div class="eyebrow">Samplinglib · formal topology · conceptual memory · semantic fidelity</div>
  <div class="ulg-hero-grid">
    <div><h1>{LABEL}</h1><p>Read the same project at three epistemic resolutions: <strong>Overview Graph</strong> for source/routes/shared stages, <strong>Lean Branches Graph</strong> for declarations, module structure and labelled reference signals, and <strong>Functor Hypergraph</strong> for source-backed recurring mathematical mechanisms such as curvature, PL/LSI and Poincaré/χ² mirrors. The views share stable ids but never share truth status automatically.</p></div>
    <dl><div><dt>{counts.get('chapters', 0)}</dt><dd>sampling chapters</dd></div><div><dt>{counts.get('lean_modules', 0)}</dt><dd>Lean modules</dd></div><div><dt>{counts.get('conceptual_families', 0)}</dt><dd>concept families</dd></div><div><dt>{counts.get('conceptual_hyperedges', 0)}</dt><dd>typed bridges</dd></div><div><dt>{counts.get('samplewiki_cases', 0)}</dt><dd>frontier results</dd></div><div><dt>{counts.get('semantic_audits', 0)}</dt><dd>round-trip audits</dd></div></dl>
  </div>
  <p class="ulg-contract"><strong>Edge direction:</strong> prerequisite/reference → consumer in proof views; Methods × targets edges carry taxonomy labels, not proof implications. <strong>Solid edges</strong> record imports and module/declaration ownership, not theorem implication. <strong>dashed edges</strong> include incomplete source-name reference scans, curated proof-leaf links, textbook/source correspondences, SampleWiki routes, semantic reviews and conceptual mirrors. Scanned references are not an exhaustive export of Lean proof dependencies. <strong>Compilation proves the Lean proposition only:</strong> source fidelity additionally requires source review. Visual proximity never certifies a conceptual transport.</p>
</section>
<section class="ulg-shell">
  <div class="ulg-toolbar">
    <div class="ulg-presets" role="group" aria-label="Graph view"><button class="active" data-view="overview">Overview Graph</button><button data-view="textbook">Textbook · 12 chapters</button><button data-view="frontier">SampleWiki frontier</button><button data-view="lean">Lean Branches Graph</button><button data-view="semantic">Semantic fidelity & repair</button><button data-view="functor">Functor Hypergraph</button><button data-view="perspectives">Methods × targets</button></div>
    <label class="ulg-search"><span>Search theorem, family, bridge, paper, module, declaration, semantic delta, or repair</span><input type="search" data-graph-search placeholder="e.g. metric-gradient-flow, PL, LSI, Fisher, Theorem 8.4.1"></label>
    <div class="ulg-scope-controls"><label>Colour by <select data-graph-color aria-label="Graph colouring"><option value="status">Evidence status</option><option value="library">Library scope / shared</option></select></label><p>Scope colours show source affiliation or planned reuse, not verified multi-textbook consumption. Evidence dots and solid/dashed edge semantics are unchanged.</p></div>
    <div class="ulg-scope-legend" data-scope-legend hidden></div>
    <div class="ulg-actions"><button data-graph-fit>Fit</button><button data-graph-reset>Reset</button><span data-graph-count></span></div>
  </div>
  <div class="ulg-stage"><div class="ulg-canvas" data-graph-canvas tabindex="0"><svg data-graph-svg role="img" aria-label="Interactive Lean and conceptual dependency graph"></svg><p data-graph-empty hidden>No matching branch.</p><small>Drag to pan · wheel to zoom · click a node to highlight its immediate prerequisites/consumers while retaining surrounding context · Esc clears focus.</small></div><aside class="ulg-detail" data-graph-detail aria-live="polite"><div class="ulg-placeholder"><span>Branch inspector</span><h2>Select a node.</h2><p>Source statement, conceptual family, semantic deltas, proof equations, exact Lean leaves, prerequisites, consumers, and reader links appear here.</p></div></aside></div>
  <div class="ulg-legend"><span><i data-status="compiled"></i>compiled</span><span><i data-status="partial"></i>partial</span><span><i data-status="audited"></i>source audited</span><span><i data-status="planned"></i>planned / blocked</span><span><i data-status="literature-open"></i>literature-open</span><span><i data-status="shared"></i>shared protocol/root</span><span><i data-status="fidelity-exact"></i>fidelity exact</span><span><i data-status="review-required"></i>semantic review required</span><span><i data-status="fidelity-mismatch"></i>semantic mismatch</span><span><i data-status="fidelity-repaired"></i>reviewed repair</span><span><i data-status="proposal"></i>conceptual / repair proposal</span><span class="edge-semantics"><b class="ulg-line-key formal"></b>Lean structural edge</span><span><b class="ulg-line-key overlay"></b>curated evidence edge</span></div>
</section>
<section class="ulg-semantics"><div class="section-heading"><span>Topology and semantic-contract semantics</span><h2>What a contribution changes—and what it preserves.</h2></div><div><article><b>01</b><h3>Reuse a branch</h3><p>A thin assembly adds a consumer edge, not a duplicate proof.</p></article><article><b>02</b><h3>Close a leaf</h3><p>A new analytic lemma discharges an open interface.</p></article><article><b>03</b><h3>Add topology</h3><p>A proof connects branches that were previously formalized only in isolation.</p></article><article><b>04</b><h3>Expose a gap</h3><p>An unknown matching theorem stays visible; ASTIS never invents a source statement.</p></article><article><b>05</b><h3>Theorem Fidelity Checker</h3><p>Original theorem → Lean → blind reconstructed theorem is compared slot by slot, not by wording.</p></article><article><b>06</b><h3>Lean Theorem Denoiser</h3><p>Source repair proposals stay separate from the pinned theorem until independent review accepts the exact repair.</p></article><article><b>07</b><h3>Conceptual Mirror Audit</h3><p>A recurring mechanism is retained under stable family/bridge ids, with translated hypotheses and a failure boundary, without becoming a Lean theorem edge.</p></article></div></section>
{cross_domain.graph_guide_html()}
<noscript><p>The interactive graph requires JavaScript. Exact declarations remain in the <a href="declarations/index.html">declaration index</a>.</p></noscript>
'''


def replace_main(text: str, body: str) -> str:
    start = text.find('<main id="content">')
    end = text.find("</main>", start)
    if start < 0 or end < 0:
        raise RuntimeError("lean-foundations main element not found")
    marker = '<main id="content">'
    return text[:start] + marker + body + "</main>" + text[end + 7 :]


def graph_href(rel: str, node_id: str) -> str:
    return "../" * len(Path(rel).parent.parts) + PAGE + "?focus=" + node_id


def context_link(text: str, rel: str, node_id: str, label: str) -> str:
    href = graph_href(rel, node_id)
    if href in text:
        return text
    block = f'<a class="ulg-context" href="{escape(href)}"><span>Formal topology</span><strong>{escape(label)}</strong><b>↗</b></a>'
    start = text.find('<main id="content">')
    closing = "</header>"
    end = text.find(closing, start)
    if end < 0:
        closing = "</section>"
        end = text.find(closing, start)
    cut = end + len(closing)
    return text if end < 0 else text[:cut] + block + text[cut:]


def transform_site(output: Path, graph: dict[str, Any]) -> None:
    asset_dir = output / "assets"
    asset_dir.mkdir(exist_ok=True)
    shutil.copyfile(CSS, asset_dir / CSS.name)
    shutil.copyfile(SEMANTIC_CSS, asset_dir / SEMANTIC_CSS.name)
    shutil.copyfile(JS, asset_dir / JS.name)
    page = output / PAGE
    text = replace_main(page.read_text(encoding="utf-8"), main_html(graph["counts"]))
    title = LABEL + " · Samplinglib"
    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
    text = text.replace("</head>", f'<link rel="stylesheet" href="assets/{CSS.name}">\n<link rel="stylesheet" href="assets/{SEMANTIC_CSS.name}">\n</head>', 1)
    text = text.replace("</body>", f'<script defer src="assets/{JS.name}"></script>\n</body>', 1)
    page.write_text(text, encoding="utf-8", newline="\n")

    link_pattern = re.compile(r'(<a\s+href="(?:\.\./)*lean-foundations\.html"(?:\s+aria-current="page")?>)Proof Atlas(</a>)')
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        text = link_pattern.sub(rf"\1{LABEL}\2", text)
        text = re.sub(r'(?<!id="source-)(data-source-id)="([^"]+)"', r'id="source-\2" \1="\2"', text)
        chapter = re.fullmatch(r"textbook/chapter-(\d{2})\.html", rel)
        section = re.fullmatch(r"textbook/chapter-(\d{2})/section-.*\.html", rel)
        if chapter:
            text = context_link(text, rel, f"chapter:{chapter.group(1)}", "Open this chapter's Lean branches")
        elif section:
            text = context_link(text, rel, f"chapter:{section.group(1)}", "Open this section in the underlying Lean graph")
        path.write_text(text, encoding="utf-8", newline="\n")
    for node in graph["nodes"]:
        if node.get("kind") != "frontier-case" or not node.get("url"):
            continue
        path = output / str(node["url"])
        if path.exists():
            rel = path.relative_to(output).as_posix()
            path.write_text(context_link(path.read_text(encoding="utf-8"), rel, str(node["id"]), "Open this result's proof branch"), encoding="utf-8", newline="\n")


def validate(output: Path, graph: dict[str, Any]) -> None:
    counts = graph["counts"]
    expected = {
        "chapters": 12,
        "samplewiki_settings": 7,
        "samplewiki_cases": 34,
        "semantic_protocol_nodes": 7,
    }
    errors = [f"{key}: expected {value}, found {counts.get(key)}" for key, value in expected.items() if counts.get(key) != value]
    errors.extend(publication_reader.validate_graph(graph, load(output / 'data/site-data.json')))
    for key in ("source_claims", "lean_modules", "registry_declarations", "conceptual_families", "conceptual_hyperedges", "nodes", "edges"):
        if not counts.get(key):
            errors.append(f"{key} is empty")
    page = (output / PAGE).read_text(encoding="utf-8")
    for marker in (
        LABEL,
        "data-underlying-lean-graph",
        DATA,
        CSS.name,
        SEMANTIC_CSS.name,
        JS.name,
        "data-graph-detail",
        "ulg-line-key formal",
        "ulg-line-key overlay",
        'data-view="semantic"',
        "Overview Graph",
        "Lean Branches Graph",
        "Functor Hypergraph",
        "Conceptual Mirror Audit",
        "Theorem Fidelity Checker",
        "Lean Theorem Denoiser",
    ):
        if marker not in page:
            errors.append(f"graph page missing {marker}")
    semantic_ids = {node.get("id") for node in graph.get("nodes", []) if node.get("kind") == "semantic-stage"}
    for node_id in ("semantic:fidelity-checker", "semantic:theorem-denoiser", "semantic:source-review"):
        if node_id not in semantic_ids:
            errors.append(f"semantic graph stage missing {node_id}")
    failures = 0
    for path in output.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        start = text.find('<div class="sidebar-contents"')
        end = text.find('<div class="sidebar-utility">', start)
        if start >= 0 and end >= 0 and LABEL not in text[start:end]:
            failures += 1
    if failures:
        errors.append(f"sidebar label missing on {failures} pages")
    if errors:
        raise RuntimeError("underlying Lean graph validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    graph = build_graph(output)
    data = output / DATA
    data.parent.mkdir(exist_ok=True)
    data.write_text(json.dumps(graph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    transform_site(output, graph)
    validate(output, graph)


if __name__ == "__main__":
    enrich_site()
