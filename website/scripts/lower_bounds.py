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
METHOD_CONTEXTS = {
    "textbook/chapter-07/section-7-5.html": ("mala", "Compare MALA upper and lower bounds →"),
    "textbook/chapter-07/section-7-6.html": ("mala", "Compare MALA upper and lower bounds →"),
    "textbook/chapter-05/section-5-2.html": ("hmc", "Compare HMC variants and their lower-bound boundaries →"),
    "libraries/mcmc/index.html": ("algorithm-specific", "Algorithm-specific lower bounds and shared MCMC tools →"),
    "libraries/discrete-sampling/index.html": ("connections", "Shared kernel tools for upper and lower bounds →"),
}
MARKER = 'data-lower-bounds-reader="true"'
GRAPH_PATH = "data/underlying-lean-graph.json"
GAUSSIAN_ITEMS = (
    "huanjian-evaluated-eq24",
    "huanjian-single-block-separation",
    "huanjian-mixture-densities",
    "huanjian-single-block-affinity",  # Optional until admitted on the built checkout.
)
OPTIMISATION_ITEMS = ("chewi-opt-v1-exercise-3-3-convex-gap-sharpness",)
# Fixed primary reading references, not publication bindings or proof credit.
METROPOLIZED_SOURCE = "https://papers.nips.cc/paper/2021/hash/9c4e6233c6d5ff637e7984152a3531d5-Abstract.html"
WARM_MALA_SOURCE = "https://arxiv.org/abs/2109.13055v2"


def link(path: str, label: str, *, page: str = PAGE) -> str:
    href = path if path.startswith("https://") else astis_site.relative_prefix(page) + path
    return f'<a href="{escape(href)}">{escape(label)}</a>'


def graph_path(node: str, view: str = "lean") -> str:
    query = {"view": view, "focus": node}
    if view == "lean":
        query["q"] = node.removeprefix("decl:")
    elif view == "perspectives":
        # Enter the existing one-hop view, not the whole methods atlas.
        query["q"] = node
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
    nonlinear = case_link(model, "ASTIS-SW-SLC-LSI-COMPLEXITY-2026", "SLC / LSI query-complexity reader")
    return (f'<article class="resource-reader" {MARKER}>'
            '<header><p class="eyebrow">Samplinglib · cross-library research topic</p><h1>Lower Bounds</h1>'
            '<p class="lede">Why is this algorithm slow? Or why must every algorithm in an oracle model be slow? '
            'These are different questions, connected through shared mathematical tools.</p>'
            '<p>' + link(graph_path("concept:lower", "functor"), "Lower Bounds in the Functor Hypergraph")
            + '</p></header>'
            '<section id="routes"><h2>Choose the kind of lower bound</h2><div class="resource-grid">'
            '<article><h3><a href="#algorithm-specific">Algorithm-specific lower bounds</a></h3>'
            '<p>MALA, leapfrog HMC and midpoint methods: limits of a specified transition or update rule.</p></article>'
            '<article><h3><a href="#general">General oracle lower bounds</a></h3>'
            '<p>Optimisation and sampling: limits of every algorithm allowed by an explicit information model.</p></article>'
            '</div><p><a href="#connections">Follow the shared mathematics across subjects</a></p></section>'
            '<section id="algorithm-specific"><h2>1. Algorithm-specific lower bounds</h2>'
            '<p>Fix the method before choosing a hard instance. Keep its step-size policy, initialization, '
            'error criterion and per-step cost visible. Slow mixing of one chain does not rule out another sampler.</p>'
            '<details id="mala"><summary>MALA · rejection and mixing bottlenecks</summary>'
            '<p>Read the upper and lower analyses of the same Metropolis-adjusted Langevin kernel together. '
            'An acceptance estimate, a spectral-gap bound and a mixing-time bound are different statements.</p>'
            '<p>' + link(METROPOLIZED_SOURCE, 'Lee–Shen–Tian, NeurIPS 2021')
            + ' studies exponentially warm starts; '
            + link(WARM_MALA_SOURCE, 'Wu–Schmidler–Chen, v2 / JMLR 2022')
            + ' gives warm-start minimax bounds and a spectral-gap-based mixing lower-bound tool. '
            'Compare the quantitative warmness assumptions before comparing rates.</p>'
            '<p>' + link('textbook/chapter-07/section-7-5.html', 'Chewi §7.5 · cold-start MALA') + ' · '
            + link('textbook/chapter-07/section-7-6.html', '§7.6 · warm-start MALA') + ' · '
            + link(graph_path('method:mala', 'perspectives'), 'MALA in Methods × targets')
            + '</p><p class="resource-boundary">Primary-source reading targets; these references do not certify local Lean lower bounds.</p></details>'
            '<details id="hmc"><summary>HMC · the integrator and trajectory policy matter</summary>'
            '<p>' + link(METROPOLIZED_SOURCE, 'Lee–Shen–Tian, NeurIPS 2021')
            + ' studies relaxation-time limits for Metropolized leapfrog HMC and connects its integration recurrence '
            'to Chebyshev polynomials. Track the number of leapfrog steps and the gradient cost per transition.</p>'
            '<p>This is not automatically a bound for exact-flow HMC, randomized trajectory lengths, '
            'Picard integrators or every algorithm called HMC. Relaxation time is not itself a uniform mixing guarantee.</p>'
            '<p>' + link('textbook/chapter-05/section-5-2.html', 'Chewi §5.2 · Hamiltonian Monte Carlo') + ' · '
            + case_link(model, 'ASTIS-SW-SPHMC-2026', 'Compare the distinct SPHMC algorithm') + ' · '
            + link(graph_path('method:hmc', 'perspectives'), 'HMC in Methods × targets')
            + '</p><p class="resource-boundary">Lower-bound formalization remains a source target; no automatic transfer between HMC variants.</p></details>'
            '<details id="midpoint"><summary>Midpoint Langevin · stationary bias and finite-time error</summary>'
            '<p><strong>Deterministic (§5):</strong> study the bias of Heun and exponential midpoint on their source hard targets. '
            '<strong>Randomized (§6):</strong> track covariance fluctuations induced by the method’s random choices. '
            'The latter is not a lower bound over all randomized oracles.</p>'
            '<p>Stationary bias, finite-time initialization and conversion from iterations to actual queries '
            'are separate steps. Retain the source’s C² Hessian bounds and normalized Wasserstein accuracy; '
            'do not add higher-derivative bounds.</p>'
            '<p>' + midpoint + ' · ' + link("https://arxiv.org/html/2610.06308v1", "Pinned paper §§5–6")
            + '</p></details>'
            '<details id="method-sharpness"><summary>Optimisation · a sharp example for a specified method</summary>'
            '<p>A sharpness witness for a gradient-method estimate belongs here. It need not defeat '
            'all first-order algorithms. Keep the update rule and its parameters fixed in the comparison.</p>'
            + components(opt, 'Related checked sharpness example (Optimisation §3)') + '</details></section>'
            '<section id="general"><h2>2. General oracle lower bounds</h2>'
            '<p>“General” means every algorithm in the stated oracle class, not every possible computational model. '
            'Specify randomization, adaptivity, query replies, initialization and capped versus expected cost.</p>'
            '<details id="optimisation"><summary>Optimisation · first-order information limits</summary>'
            '<p>Identify the permitted queries, the information revealed by each reply and the required objective accuracy. '
            'Borrow the design of hard instances and the transcript argument, not the rate or its constants.</p>'
            '<p>' + link(OPTIMISATION, "Read Optimisation §4 · Lower bounds for smooth optimisation")
            + '</p></details>'
            '<details id="gaussian"><summary>Gaussian sampling · hide information and separate target laws</summary>'
            '<p>The determinant-sign construction (Theorem 3.1) pairs indistinguishable oracle information with '
            'separated averaged target laws. The fixed-spectrum hidden-eigenbasis route (Theorem 4.1) uses a '
            'different information restriction; do not substitute one proof for the other.</p>'
            '<p>' + gaussian_case + ' · ' + link("https://arxiv.org/html/2610.20492v1", "Pinned paper §§2–4")
            + '</p><p>These Lean components do not certify the complete query lower bounds. '
            'Product amplification, transcript restrictions and the exact cost model belong to the paper route.</p>'
            + components(gaussian, "Open independently reviewed Gaussian components") + '</details>'
            '<details id="nonlinear"><summary>Beyond Gaussians · SLC and LSI query lower bounds</summary>'
            '<p>Zhou–Suzuki (arXiv:2611.05813v1) use nonlinear hard instances: '
            'layered Gaussian tensor fields for strongly log-concave targets, and hidden angular caps '
            'for smooth targets satisfying LSI. Cold-start, unknown warm-start and LSI results have separate contracts.</p>'
            '<p>' + nonlinear + '</p><p>All main results are open in Lean. The source outline locates what must be proved; '
            'it does not certify reuse of Gaussian Complexity or optimisation lower bounds.</p></details></section>'
            '<section id="connections"><h2>Shared mathematics, not isolated shelves</h2>'
            '<p>Read an algorithm’s upper and lower bounds beside the same definitions. Then ask which '
            'proof ingredients can be reused in another subject—not merely which papers have similar titles.</p>'
            '<details><summary>Markov kernels, reversibility and spectral tools · MCMC ↔ discrete sampling</summary>'
            '<p>Both convergence upper bounds and mixing lower bounds can use the same kernel, invariant measure '
            'and Dirichlet-form conventions, but need different estimates. Finite-state adapters are not automatic '
            'general-state MALA or HMC theorems.</p><p>'
            + link('libraries/mcmc/index.html', 'MCMC foundations') + ' · '
            + link('libraries/discrete-sampling/index.html', 'Discrete Sampling') + ' · '
            + link('proofs/random-scan-reversibility.html', 'Existing checked random-scan reversibility')
            + '</p><p>That checked kernel result is a foundation, not a spectral-gap or mixing lower bound.</p></details>'
            '<details><summary>Numerical recurrences and polynomial tools · HMC ↔ optimisation ↔ sampling</summary>'
            '<p>HMC’s leapfrog/Chebyshev connection suggests comparing polynomial recurrences with optimisation '
            'methods; midpoint bounds share integrator definitions with their upper analyses. These are reading '
            'and future adapter routes, not certified reductions or new Functor edges.</p><p>'
            + link('libraries/optimisation/index.html', 'Optimisation') + ' · ' + midpoint
            + '</p></details>'
            '<details id="reuse"><summary>Information restriction + separation · general oracle bounds</summary>'
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
            'identities in the same Lean graph; this reader adds no formal proof edges or completion credit.</p></details>'
            '<p class="resource-boundary">Graph key: exact declarations keep one canonical Lean node; '
            'source placements and method links are reading relations; conceptual mirrors need their own reviewed '
            'hypothesis adapters. None of these latter relations is a proved implication.</p></section></article>')


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
    for rel, (anchor, label) in METHOD_CONTEXTS.items():
        path = output / rel
        text = path.read_text(encoding="utf-8")
        if 'data-lower-bounds-method-context' not in text:
            block = ('<aside class="note" data-lower-bounds-method-context><p>'
                     + link(PAGE + '#' + anchor, label, page=rel) + '</p></aside>')
            path.write_text(text.replace("</main>", block + "</main>", 1), encoding="utf-8", newline="\n")


def validate_site(output: Path) -> list[str]:
    path = output / PAGE
    if not path.is_file():
        return ["Missing standalone Lower Bounds reader"]
    text = path.read_text(encoding="utf-8")
    errors = []
    for marker in (MARKER, 'id="algorithm-specific"', 'id="general"', 'id="mala"', 'id="hmc"',
                   'id="optimisation"', 'id="midpoint"', 'id="gaussian"', 'id="connections"', 'id="reuse"'):
        if marker not in text:
            errors.append("Lower Bounds missing " + marker)
    for rel in ENTRY_PAGES:
        if 'data-lower-bounds-context' not in (output / rel).read_text(encoding="utf-8"):
            errors.append("Missing Lower Bounds context link: " + rel)
    for rel, (anchor, _) in METHOD_CONTEXTS.items():
        page = output / rel
        context = page.read_text(encoding="utf-8") if page.is_file() else ""
        if 'data-lower-bounds-method-context' not in context or PAGE + '#' + anchor not in context:
            errors.append("Missing method-specific Lower Bounds return link: " + rel)
    graph = json.loads((output / GRAPH_PATH).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    if nodes.get("concept:lower", {}).get("url") != PAGE:
        errors.append("Existing Lower Bounds concept must point to its independent reader")
    return errors
