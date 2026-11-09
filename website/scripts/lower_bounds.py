"""Cross-library lower-bound reader over the existing source and Lean graph."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
from urllib.parse import urlencode

import astis_publication as publication
import astis_site
import declaration_lessons
import samplewiki_companions
import source_lineage
from samplewiki_reader_contract import formula_html

PAGE = "lower-bounds/index.html"
OPTIMISATION = "libraries/optimisation/chapter-04.html"
ENTRY_PAGES = (OPTIMISATION, "example-cases/samplewiki.html", "resources/index.html")
MARKER = 'data-lower-bounds-reader="true"'
GRAPH_PATH = "data/underlying-lean-graph.json"
GAUSSIAN_ITEMS = (
    "huanjian-evaluated-eq24",
    "huanjian-single-block-separation",
    "huanjian-mixture-densities",
    "huanjian-single-block-affinity",  # Optional until admitted on the built checkout.
)
OPTIMISATION_ITEMS = ("chewi-opt-v1-exercise-3-3-convex-gap-sharpness",)


def link(path: str, label: str, *, page: str = PAGE) -> str:
    href = path if path.startswith("https://") else astis_site.relative_prefix(page) + path
    return f'<a href="{escape(href)}">{escape(label)}</a>'


def graph_path(node: str, view: str = "lean") -> str:
    query = {"view": view, "focus": node}
    if view == "lean":
        query["q"] = node.removeprefix("decl:")
    return "lean-foundations.html?" + urlencode(query)


def case_link(model: dict, case_id: str, label: str) -> str:
    case = next(c for c in model["cases"] if c["id"] == case_id)
    return link(samplewiki_companions.BASE + case["slug"] + ".html", label)


def reviewed_readings(ids: tuple[str, ...], items: dict, data: dict, nodes: dict) -> list[dict]:
    """Follow admitted publication bindings; don't discover nodes by 'lower' in a name."""
    rows = []
    seen = set()
    for ident in ids:
        item = items.get(ident)
        if item is None:
            continue
        for binding in item["bindings"]:
            name = binding["declaration"]
            if name in seen or binding["role"] != "proof-edge":
                continue
            audit = data["audits"].get(binding.get("audit_id"), {})
            if not (publication.verified_binding(binding, data)
                    and audit.get("state") in {"source-reviewed", "accepted"}
                    and audit.get("source_review", {}).get("state") == "accepted"
                    and audit.get("lean", {}).get("compiled") is True
                    and audit.get("publication_binding_sha256") == publication.binding_digest(item, binding, data)):
                continue
            node = "decl:" + name
            lesson = declaration_lessons.lesson_path(name)
            if nodes.get(node, {}).get("url") != lesson:
                raise ValueError(f"Lower Bounds: missing canonical graph-to-lesson link for {name}")
            rows.append({"title": item["title"], "node": node, "lesson": lesson,
                         "source": item["source"]["url"]})
            seen.add(name)
    return rows


def components(rows: list[dict], label: str) -> str:
    if not rows:
        return ""
    return (f'<details><summary>{escape(label)}</summary><ul class="resource-list">'
            + ''.join(f'<li data-lower-bound-lean="{escape(r["node"])}">'
                      + link(r["lesson"], r["title"]) + '<small>'
                      + link(graph_path(r["node"]), "Exact Lean graph node") + " · "
                      + link(r["source"], "Pinned source") + "</small></li>" for r in rows)
            + "</ul></details>")


def render(model: dict, items: dict, data: dict, nodes: dict) -> str:
    opt = reviewed_readings(OPTIMISATION_ITEMS, items, data, nodes)
    gaussian = reviewed_readings(GAUSSIAN_ITEMS, items, data, nodes)
    midpoint = case_link(model, "ASTIS-SW-MIDPOINT-2026", "Midpoint Langevin reader")
    gaussian_case = case_link(model, "ASTIS-SW-GAUSSIAN-COMPLEXITY-2026", "Gaussian Complexity reader")
    return (f'<article class="resource-reader" {MARKER}>'
            '<header><p class="eyebrow">Samplinglib · cross-library research topic</p><h1>Lower Bounds</h1>'
            '<p class="lede">What information does an algorithm receive, and what can it guarantee with that information? '
            'Compare hard instances and proof techniques across optimisation and sampling.</p>'
            '<p>' + link(graph_path("concept:lower", "functor"), "Lower Bounds in the Functor Hypergraph")
            + '</p></header>'
            '<section id="routes"><h2>Choose the kind of lower bound</h2><div class="resource-grid">'
            '<article><h3><a href="#optimisation">Optimisation</a></h3>'
            '<p>First-order oracle limits and hard-instance design.</p></article>'
            '<article><h3><a href="#midpoint">Midpoint methods</a></h3>'
            '<p>Bias and iteration limits for specified numerical methods.</p></article>'
            '<article><h3><a href="#gaussian">Gaussian sampling</a></h3>'
            '<p>Query limits for adaptive algorithms with exact oracle access.</p></article></div></section>'
            '<section id="optimisation"><h2>Optimisation: start with the oracle</h2>'
            '<p>Identify the permitted queries, the information revealed by each reply and the required objective accuracy. '
            'Borrow the design of hard instances and the transcript argument, not the rate or its constants.</p>'
            '<p>' + link(OPTIMISATION, "Read Optimisation §4 · Lower bounds for smooth optimisation")
            + '</p><p>A sharpness witness for a specified gradient method is useful practice, '
            'but does not by itself bound all first-order algorithms.</p>'
            + components(opt, "Related checked sharpness example (Optimisation §3)") + '</section>'
            '<section id="midpoint"><h2>Midpoint: keep the method fixed</h2>'
            '<p><strong>Deterministic (§5):</strong> study the bias of Heun and exponential midpoint on their source hard targets. '
            '<strong>Randomized (§6):</strong> track covariance fluctuations induced by the method’s random choices. '
            'The latter is not a lower bound over all randomized oracles.</p>'
            '<p>In both lanes, stationary bias, finite-time initialization and conversion from iterations to actual queries '
            'are separate steps. Retain the source’s C² Hessian bounds and normalized Wasserstein accuracy; '
            'do not add higher-derivative bounds.</p>'
            '<p>' + midpoint + ' · ' + link("https://arxiv.org/html/2610.06308v1", "Pinned paper §§5–6")
            + '</p></section>'
            '<section id="gaussian"><h2>Gaussian sampling: hide information and separate target laws</h2>'
            '<p>The determinant-sign construction (Theorem 3.1) pairs indistinguishable oracle information with '
            'separated averaged target laws. The fixed-spectrum hidden-eigenbasis route (Theorem 4.1) uses a '
            'different information restriction; do not substitute one proof for the other.</p>'
            '<p>' + gaussian_case + ' · ' + link("https://arxiv.org/html/2610.20492v1", "Pinned paper §§2–4")
            + '</p><p>These Lean components do not certify the complete query lower bounds. '
            'Product amplification, transcript restrictions and the exact cost model belong to the paper route.</p>'
            + components(gaussian, "Open independently reviewed Gaussian components") + '</section>'
            '<section id="reuse"><h2>How the techniques connect</h2>'
            '<p>One reusable proof pattern: if two hard priors yield the same joint law of the random seed and visible transcript '
            r'(including stopping), measurable postprocessing gives one averaged output law \(Q\). If the guarantee places '
            r'that law within \(\varepsilon\) in TV of both averaged targets \(P_+\) and \(P_-\), the triangle inequality gives</p>'
            + formula_html(r"\begin{aligned}\mathrm{TV}(P_+,P_-)&\le\mathrm{TV}(P_+,Q)\\"
                           r"&\quad+\mathrm{TV}(Q,P_-)\\&\le2\varepsilon.\end{aligned}")
            + '<p>The reusable step is the information restriction plus a separation witness. Its application still needs '
            'the actual oracle, measurable algorithm, prior averaging, loss and query budget. A fixed query cap does not '
            'automatically give an expected-cost theorem, and TV closeness does not transfer unbounded cost.</p>'
            '<p>' + link(graph_path("transport:oracle-reduction", "functor"), "Inspect the conditional oracle-reduction template")
            + '. This is a conceptual comparison, not a proved reduction. The links above reuse existing declaration '
            'identities in the same Lean graph; this reader adds no formal proof edges or completion credit.</p></section></article>')


def enrich_site(output: Path) -> None:
    graph = json.loads((output / GRAPH_PATH).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    body = render(samplewiki_companions.load(), {i["id"]: i for i in publication.load()},
                  publication.inputs(), nodes)
    page = astis_site.page("Lower Bounds", PAGE, body,
                          extra_head='<link rel="stylesheet" href="../assets/resource-library.css">')
    astis_site.write_page(output, PAGE, source_lineage.canonical_shell(page, PAGE, output))
    for rel in ENTRY_PAGES:
        path = output / rel
        text = path.read_text(encoding="utf-8")
        if 'data-lower-bounds-context' not in text:
            block = ('<aside class="note" data-lower-bounds-context><p>'
                     + link(PAGE, "Compare lower-bound techniques across libraries →", page=rel)
                     + '</p></aside>')
            path.write_text(text.replace("</main>", block + "</main>", 1), encoding="utf-8", newline="\n")


def validate_site(output: Path) -> list[str]:
    path = output / PAGE
    if not path.is_file():
        return ["Missing standalone Lower Bounds reader"]
    text = path.read_text(encoding="utf-8")
    errors = []
    for marker in (MARKER, 'id="optimisation"', 'id="midpoint"', 'id="gaussian"', 'id="reuse"'):
        if marker not in text:
            errors.append("Lower Bounds missing " + marker)
    for rel in ENTRY_PAGES:
        if 'data-lower-bounds-context' not in (output / rel).read_text(encoding="utf-8"):
            errors.append("Missing Lower Bounds context link: " + rel)
    graph = json.loads((output / GRAPH_PATH).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    if nodes.get("concept:lower", {}).get("url") != PAGE:
        errors.append("Existing Lower Bounds concept must point to its independent reader")
    return errors
