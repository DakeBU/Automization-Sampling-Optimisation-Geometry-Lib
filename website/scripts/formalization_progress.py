#!/usr/bin/env python3
"""Unified collaborative Current Progress dashboard for Samplinglib.

The five public formalization and research routes live on one page so collaborators can
track their own theorem-sized Frontier Cells while seeing the other routes and
the shared Lean floor. Historical route URLs remain stable aliases.
"""

from __future__ import annotations

import posixpath
import re
import shutil
import sys
from html import escape
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import astis_frontier_cells  # noqa: E402
import astis_site  # noqa: E402
import library_shelves  # noqa: E402
import cross_domain  # noqa: E402
import discrete_sampling  # noqa: E402
import mcmc_library  # noqa: E402


DEFAULT_OUTPUT = ROOT / "_site"
SOURCE_CSS = ROOT / "website" / "static" / "formalization-progress.css"
STYLE_NAME = "formalization-progress.css"
HARNESS = ROOT / "website" / "static" / "astis-harness-current.svg"
HARNESS_NAME = "astis-harness-current.svg"

OVERVIEW = "progress/index.html"
SAMPLEWIKI_DETAIL = "progress/samplewiki-detail.html"
SAMPLEWIKI_ROUTE = "progress/samplewiki-route.html"
RIEMANNIAN_ROUTE = "progress/riemannian-optimization.html"
OPTIMISATION_ROUTE = "progress/optimisation.html"
OLD_FIRST_ORDER_ROUTE = "progress/first-order-optimization.html"
OLD_SAMPLEWIKI_PROGRESS = "example-cases/samplewiki/progress.html"

ROUTE_ANCHORS = {
    "samplewiki-route": "samplewiki",
    "riemannian-optimization": "riemannian",
    "optimisation": "optimisation",
    "statistical-optimal-transport": "optimal-transport",
    "higher-order-sampling": "higher-order-sampling",
    "discrete-sampling": "discrete-sampling",
    "mcmc": "mcmc",
}

PRIVATE_PUBLIC_MARKERS = (
    "ZDD-style",
    "categorical or functor-like",
    "alternative minimal supports",
    "compression candidates",
)


def prefix(rel: str) -> str:
    return "../" * len(Path(rel).parent.parts)


def href_from(current: str, target: str) -> str:
    start = posixpath.dirname(current) or "."
    return posixpath.relpath(target, start=start)


def dashboard_href(rel: str, anchor: str = "") -> str:
    href = href_from(rel, OVERVIEW)
    return f"{href}#{anchor}" if anchor else href


def add_style(text: str, rel: str, style_name: str) -> str:
    href = f"{prefix(rel)}assets/{style_name}"
    if href in text:
        return text
    if "</head>" not in text:
        raise RuntimeError(f"{rel}: missing </head>")
    return text.replace("</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', 1)


def progress_sidebar(rel: str) -> str:
    return f"""<section class="sidebar-group sidebar-progress" data-formalization-progress="1">
  <h2><a href="{dashboard_href(rel)}">Current Progress</a></h2>
  <nav class="progress-route-nav">
    <a href="{dashboard_href(rel, 'samplewiki')}">SampleWiki Route</a>
    <a href="{dashboard_href(rel, 'riemannian')}">Riemannian Optimization</a>
    <a href="{dashboard_href(rel, 'optimisation')}">Optimisation</a>
    <a href="{dashboard_href(rel, 'optimal-transport')}">Statistical Optimal Transport Route</a>
    <a href="{dashboard_href(rel, 'higher-order-sampling')}">Higher-Order Smoothness × Sampling</a>
    <a href="{dashboard_href(rel, 'discrete-sampling')}">Discrete Sampling Route</a>
    <a href="{dashboard_href(rel, 'mcmc')}">Markov Chain Monte Carlo Route</a>
  </nav>
</section>"""


def insert_progress_sidebar(text: str, rel: str) -> str:
    text = re.sub(
        r'<section class="sidebar-group sidebar-progress".*?</section>',
        progress_sidebar(rel),
        text,
        count=1,
        flags=re.S,
    )
    if 'class="sidebar-group sidebar-progress"' in text:
        return text
    pattern = re.compile(r'(<section class="sidebar-group sidebar-libraries".*?</section>)', re.S)
    if not pattern.search(text):
        raise RuntimeError(f"{rel}: Libraries sidebar missing before Current Progress insertion")
    return pattern.sub(lambda match: match.group(1) + "\n" + progress_sidebar(rel), text, count=1)


def patch_site_nav(text: str, rel: str) -> str:
    href = dashboard_href(rel)
    active = ' aria-current="page"' if rel.startswith("progress/") else ""
    link = f'<a href="{href}"{active}>Current Progress</a>'
    pattern = re.compile(r'(<nav class="site-nav"[^>]*>)(.*?)(</nav>)', re.S)
    match = pattern.search(text)
    if not match:
        return text
    body = match.group(2)
    body, count = re.subn(
        r'<a href="[^"]*progress/index\.html"(?: aria-current="page")?>Current Progress</a>',
        link,
        body,
        count=1,
    )
    if count == 0 and "Current Progress</a>" not in body:
        body += link
    replacement = match.group(1) + body + match.group(3)
    return text[: match.start()] + replacement + text[match.end() :]


def _rewrite_one_url(url: str, old_rel: str, new_rel: str) -> str:
    if not url or url.startswith(("#", "/", "//", "mailto:", "tel:", "data:", "javascript:")):
        return url
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return url
    old_parent = posixpath.dirname(old_rel) or "."
    target = posixpath.normpath(posixpath.join(old_parent, parsed.path))
    new_parent = posixpath.dirname(new_rel) or "."
    rebased = posixpath.relpath(target, start=new_parent)
    suffix = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"{rebased}{suffix}{fragment}"


def rebase_local_urls(text: str, old_rel: str, new_rel: str) -> str:
    pattern = re.compile(r'(?P<attr>href|src)="(?P<url>[^"]+)"')

    def repl(match: re.Match[str]) -> str:
        url = _rewrite_one_url(match.group("url"), old_rel, new_rel)
        return f'{match.group("attr")}="{url}"'

    return pattern.sub(repl, text)


def retarget_progress_links(text: str, rel: str) -> str:
    targets = {
        OLD_SAMPLEWIKI_PROGRESS: "samplewiki",
        SAMPLEWIKI_ROUTE: "samplewiki",
        RIEMANNIAN_ROUTE: "riemannian",
        OPTIMISATION_ROUTE: "optimisation",
        OLD_FIRST_ORDER_ROUTE: "optimisation",
    }
    pattern = re.compile(r'href="(?P<url>[^"]+)"')

    def repl(match: re.Match[str]) -> str:
        url = match.group("url")
        if not url or url.startswith(("#", "/", "//", "mailto:", "tel:", "data:", "javascript:")):
            return match.group(0)
        parsed = urlsplit(url)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(rel) or ".", parsed.path))
        anchor = targets.get(resolved)
        if not anchor:
            return match.group(0)
        return f'href="{dashboard_href(rel, anchor)}"'

    return pattern.sub(repl, text)


def status_label(status: str) -> str:
    return status.replace("_", " ")


def frontier_cells_by_route() -> dict[str, list[dict[str, object]]]:
    cells = astis_frontier_cells.load_cells()
    errors = astis_frontier_cells.validate_cells(cells)
    if errors:
        raise RuntimeError("Frontier Cell protocol invalid before dashboard render:\n- " + "\n- ".join(errors))
    grouped: dict[str, list[dict[str, object]]] = {route: [] for route in (*ROUTE_ANCHORS.keys(), "shared")}
    for cell in cells:
        route = str(cell.get("route", ""))
        if route in grouped:
            grouped[route].append(cell)
    return grouped


def cells_html(cells: list[dict[str, object]], *, empty_copy: str) -> str:
    if not cells:
        return f'<p class="progress-empty-cells">{escape(empty_copy)}</p>'
    priority = {
        "blocked": 0,
        "quarantined": 1,
        "claimed": 2,
        "proved_locally": 3,
        "independently_verified": 4,
        "stabilized": 5,
        "merged": 6,
    }
    ordered = sorted(cells, key=lambda cell: (priority.get(str(cell.get("status")), 99), str(cell.get("cell_id", ""))))
    rows = []
    for cell in ordered[:10]:
        status = str(cell.get("status", ""))
        rows.append(
            f"""<article class="progress-cell" data-frontier-cell="{escape(str(cell.get('cell_id', '')))}">
  <div class="progress-cell-head"><code>{escape(str(cell.get('cell_id', '')))}</code><span class="cell-status cell-status-{escape(status)}">{escape(status_label(status))}</span></div>
  <h4>{escape(str(cell.get('title', '')))}</h4>
  <p>{escape(str(cell.get('target_statement', '')))}</p>
</article>"""
        )
    if len(cells) > 10:
        rows.append(f'<p class="progress-empty-cells">+ {len(cells) - 10} additional registered cells.</p>')
    return '<div class="progress-cell-list">' + "".join(rows) + '</div>'


def milestones(items: list[tuple[str, str, str]]) -> str:
    return '<div class="progress-milestones">' + ''.join(
        f'<article><div class="progress-milestone-head"><span>{escape(status)}</span><b>{index:02d}</b></div><h3>{escape(title)}</h3><p>{escape(copy)}</p></article>'
        for index, (status, title, copy) in enumerate(items, 1)
    ) + '</div>'


def route_panel(
    *,
    route_id: str,
    anchor: str,
    title: str,
    eyebrow: str,
    status: str,
    source_label: str,
    source_url: str,
    lede: str,
    items: list[tuple[str, str, str]],
    cells: list[dict[str, object]],
    actions: str,
) -> str:
    progress = library_shelves.publication_reader.publication.chapter_progress(route_id)
    if progress['status'] != 'scaffold':
        status = progress['label'] + ' · source fidelity separate'
    return f"""
<section class="progress-route-panel route-{escape(anchor)}" id="{escape(anchor)}" data-progress-route="{escape(route_id)}">
  <header class="progress-route-header">
    <div><span class="route-kicker">{escape(eyebrow)}</span><h2>{escape(title)}</h2><p>{escape(lede)}</p></div>
    <div class="route-meta"><span class="route-status">{escape(status)}</span><a href="{escape(source_url)}">{escape(source_label)} ↗</a></div>
  </header>
  <div class="progress-route-body">
    <div><h3>Route milestones</h3>{milestones(items)}</div>
    <aside class="progress-cells"><h3>Registered Frontier Cells</h3>{cells_html(cells, empty_copy="No active Frontier Cell record is published for this route yet. Create one when a theorem-sized task is claimed.")}{actions}</aside>
  </div>
</section>
"""


def workflow_block(shared_cells: list[dict[str, object]]) -> str:
    return f"""
<section class="progress-workflow" data-progress-verification-workflow="true" id="protocol">
  <div class="section-heading"><span>ASTIS Harness · collaborative contract</span><h2>One state machine, one shared Lean floor.</h2></div>
  <div class="progress-state-machine" aria-label="ASTIS formalization state machine">
    <div class="state-main"><span>claimed</span><b>→</b><span>proved locally</span><b>→</b><span>independently verified</span><b>→</b><span>stabilized</span><b>→</b><span>merged</span></div>
    <div class="state-blocked"><span>blocked</span><b>→</b><span>smaller child theorem</span><b>→</b><span>verified</span><b>→</b><span>re-entry</span></div>
  </div>
  <div class="progress-protocol-grid">
    <article><span>Before proving</span><h3>Search and classify</h3><p>Search Samplinglib, Mathlib, active shared cells, and relevant formal upstreams. Record <code>reuse</code>, <code>adapt</code>, <code>missing</code>, or <code>out_of_scope</code> before adding a declaration.</p></article>
    <article><span>Shared lemma collision</span><h3>One canonical shared cell</h3><p>If two routes need the same missing lower-level theorem, record <code>decision: new_canonical_shared</code>, keep the route-local cell at <code>claimed</code>, and open/depend on one <code>route: shared</code> Frontier Cell. Parallel duplicate implementations are rejected by the protocol validator.</p></article>
    <article><span>Integration</span><h3>Single stabilization lane</h3><p>Shared aggregators, root registries, duplicate API resolution, graph regeneration, and final root builds are serialized after independent verification.</p></article>
  </div>
  <div class="progress-shared-cells"><h3>Shared-foundation Frontier Cells</h3>{cells_html(shared_cells, empty_copy="No shared Frontier Cell is currently registered. Candidate cross-route checkpoints are tracked in Libraries/shared-foundations.yml.")}</div>
  <p class="progress-protocol-actions"><a class="button primary" href="../workflow/index.html">Open ASTIS Harness</a> <a class="button" href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/docs">Protocol docs ↗</a> <a class="button" href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/issues/new?template=frontier-cell.yml">Claim a Frontier Cell ↗</a></p>
</section>
"""


def overview_body() -> str:
    grouped = frontier_cells_by_route()
    samplewiki_items = [
        ("active", "Dependency-first Chewi spine", "Continue the shortest prerequisite route through the Chewi textbook graph toward useful SampleWiki results."),
        ("active", "Source fidelity + theorem insertion", "Audit frontier statements against primary papers, then attach verified declarations to the existing theorem graph."),
        ("planned", "Proximal / LMC / ULD / MALA foundations", "Prioritize reusable analytic roots that unlock multiple frontier cases rather than isolated terminal proofs."),
        ("planned", "Frontier result closure", "Advance the highest-value reachable SampleWiki cells once their shared parents are stable."),
    ]
    riemannian_items = [
        ("scaffold", "Boumal source map", "The eleven-chapter public route and source boundaries are established."),
        ("planned", "Shared geometry floor", "Audit Mathlib and Samplinglib first; Chewi sampling §2.5 is the first explicit cross-route checkpoint."),
        ("planned", "Boumal Chapters 1–4", "Definitions, embedded first-order geometry, and first-order Riemannian algorithms."),
        ("planned", "Boumal Chapters 5–11", "Second-order geometry/algorithms, general and quotient manifolds, additional tools, and geodesic convexity."),
    ]
    optimisation_items = [
        ("scaffold", "Chewi Lectures on Optimization source map", "The public formalization spine follows arXiv:2605.07006: §§1–13 plus Appendix A."),
        ("planned", "Convexity, flow, descent, acceleration", "Formalize §§1–5 while reusing compatible Mathlib/Optlib declarations."),
        ("planned", "Non-smooth, Frank-Wolfe, proximal, duality", "Formalize §§6–9 and expose exact shared foundations with sampling when statements coincide."),
        ("planned", "Mirror, alternating, stochastic, interior-point", "Formalize §§10–13 and audit sampling intersections around mirror/proximal/stochastic structure."),
    ]
    samplewiki_actions = '<p><a class="button" href="samplewiki-detail.html">Detailed dependency/audit view</a></p>'
    riemannian_actions = '<p><a class="button" href="../libraries/riemannian-optimization/index.html">Open Boumal source route</a></p>'
    optimisation_actions = '<p><a class="button" href="../libraries/optimisation/index.html">Open Chewi Optimisation route</a></p>'
    return f"""
<section class="page-hero compact progress-hero" data-current-progress="overview">
  <div class="eyebrow">Samplinglib · Current Progress</div>
  <h1>Seven routes, one collaboration board.</h1>
  <p class="lede">SampleWiki, Riemannian Optimization, Optimisation, Statistical Optimal Transport, Discrete Sampling, and higher-order sampling advance in parallel on one page. Each theorem-sized task is a Frontier Cell; lower-level mathematics is shared only after a reuse/compatibility audit, so collaborators can move independently without rebuilding the same Lean foundation.</p>
  <nav class="progress-dashboard-nav" aria-label="Current Progress routes"><a href="#samplewiki">SampleWiki Route</a><a href="#riemannian">Riemannian Optimization</a><a href="#optimisation">Optimisation</a><a href="#optimal-transport">Statistical Optimal Transport Route</a><a href="#higher-order-sampling">Higher-Order Smoothness × Sampling</a><a href="#discrete-sampling">Discrete Sampling Route</a><a href="#mcmc">Markov Chain Monte Carlo Route</a><a href="#shared-order">Shared order</a><a href="#protocol">Harness protocol</a></nav>
</section>
<div class="progress-dashboard" data-unified-progress-dashboard="true">
{route_panel(route_id="samplewiki-route", anchor="samplewiki", title="SampleWiki Route", eyebrow="Dependency-first frontier route", status="active", source_label="Open SampleWiki", source_url="../example-cases/samplewiki.html", lede="Immediate priority: extend the verified Chewi spine until useful frontier sampling results can enter the same theorem graph with exact source fidelity.", items=samplewiki_items, cells=grouped["samplewiki-route"], actions=samplewiki_actions)}
{route_panel(route_id="riemannian-optimization", anchor="riemannian", title="Riemannian Optimization", eyebrow="Boumal route", status="scaffold", source_label="Open library", source_url="../libraries/riemannian-optimization/index.html", lede="Formalize Boumal while sharing only mathematically identical geometry foundations with the sampling route. Convention differences stay explicit in adapters.", items=riemannian_items, cells=grouped["riemannian-optimization"], actions=riemannian_actions)}
{route_panel(route_id="optimisation", anchor="optimisation", title="Optimisation", eyebrow="Sinho Chewi · arXiv:2605.07006", status="scaffold", source_label="Open library", source_url="../libraries/optimisation/index.html", lede="Formalize Chewi's public optimization notes section by section, reusing Mathlib/Optlib/CvxLean and exposing exact shared convex/proximal/mirror foundations with sampling.", items=optimisation_items, cells=grouped["optimisation"], actions=optimisation_actions)}
{cross_domain.extra_route_panels(grouped, route_panel)}
{discrete_sampling.route_panel(grouped, route_panel)}
{mcmc_library.route_panel(grouped, route_panel)}
</div>
{cross_domain.shared_plan_html()}
<section class="progress-intersections">
  <div class="section-heading"><span>Shared Lean floor</span><h2>Parallel above; canonical below.</h2></div>
  <div class="progress-overlap-grid">
    <article><span>Geometry checkpoint</span><h3>Chewi sampling §2.5 ↔ Boumal</h3><p>Riemannian manifolds, tangent-space/differential interfaces, gradients, metrics, and related analysis are candidates for one canonical shared foundation after convention compatibility is proved.</p></article>
    <article><span>Optimisation checkpoints</span><h3>Chewi sampling §4.3 / Ch. 8 / Ch. 10 ↔ Chewi Optimisation</h3><p>Convex analysis, proximal structure, mirror geometry, and stochastic-gradient primitives may be shared. Sampler kernels, invariant-law arguments, and route-specific source theorems remain separate.</p></article>
    <article><span>Collision rule</span><h3>Reuse → adapt → shared cell</h3><p>Exact match → reuse. Near match → canonical core plus explicit adapter. Missing theorem needed by multiple routes → one shared Frontier Cell. Different theorem → keep separate.</p></article>
  </div>
</section>
{workflow_block(grouped["shared"])}
"""


def write_page(output: Path, rel: str, title: str, body: str, description: str) -> None:
    text = astis_site.page(title, rel, body, active="Progress", description=description)
    astis_site.write_page(output, rel, text)


def write_alias(output: Path, rel: str, title: str, anchor: str) -> None:
    target = f"index.html#{anchor}"
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Samplinglib · Current Progress</div><h1>{escape(title)}</h1><p class="lede">Current Progress is now one collaboration dashboard so all seven formalization and research routes and their shared lower-level foundations stay visible together.</p><p><a class="button primary" href="{target}">Open {escape(title)} on the dashboard</a></p></section>
"""
    text = astis_site.page(f"{title} — Current Progress", rel, body, active="Progress")
    text = text.replace(
        "</head>",
        f'  <link rel="canonical" href="{target}">\n  <meta http-equiv="refresh" content="0; url={target}">\n</head>',
        1,
    )
    astis_site.write_page(output, rel, text)


def lift_samplewiki_detail(output: Path) -> None:
    old_path = output / OLD_SAMPLEWIKI_PROGRESS
    if not old_path.exists():
        raise RuntimeError("final SampleWiki progress page is missing before detail lift")
    text = old_path.read_text(encoding="utf-8")
    text = rebase_local_urls(text, OLD_SAMPLEWIKI_PROGRESS, SAMPLEWIKI_DETAIL)
    text = re.sub(r"<title>.*?</title>", "<title>SampleWiki Detailed Progress · Samplinglib</title>", text, count=1, flags=re.S)
    text = text.replace("<h1>Source audit and Lean progress</h1>", "<h2>Source audit and Lean progress</h2>", 1)
    banner = """
<section class="page-hero compact progress-hero progress-samplewiki-banner" data-current-progress="samplewiki-detail">
  <div class="eyebrow">Current Progress · SampleWiki detailed view</div>
  <h1>SampleWiki dependency and audit detail</h1>
  <p class="lede">This preserves the detailed dependency-first preparation path. The unified dashboard remains the coordination surface for all collaborators.</p>
  <p><a href="index.html#samplewiki">← Unified Current Progress</a> · <a href="../example-cases/samplewiki.html">Open SampleWiki</a></p>
</section>
"""
    marker = '<main id="content">'
    if marker not in text:
        raise RuntimeError("lifted SampleWiki detail is missing main content")
    text = text.replace(marker, marker + banner, 1)
    new_path = output / SAMPLEWIKI_DETAIL
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path.write_text(text, encoding="utf-8", newline="\n")

    alias_body = """
<section class="page-hero compact"><div class="eyebrow">Current Progress</div><h1>SampleWiki Route</h1><p class="lede">This route now lives on the unified collaboration dashboard.</p><p><a class="button primary" href="../../progress/index.html#samplewiki">Open SampleWiki Route</a></p></section>
"""
    alias = astis_site.page("SampleWiki Route — moved", OLD_SAMPLEWIKI_PROGRESS, alias_body, active="Progress")
    alias = alias.replace(
        "</head>",
        '  <link rel="canonical" href="../../progress/index.html#samplewiki">\n  <meta http-equiv="refresh" content="0; url=../../progress/index.html#samplewiki">\n</head>',
        1,
    )
    old_path.write_text(alias, encoding="utf-8", newline="\n")


def home_blocks() -> str:
    return """
<section class="home-progress" data-formalization-progress-home="true">
  <div class="section-heading"><span>Current Progress</span><h2>One collaboration dashboard for all seven routes.</h2></div>
  <div class="home-progress-grid">
    <a class="home-route-samplewiki" href="progress/index.html#samplewiki"><strong>SampleWiki Route</strong><span>dependency-first path to frontier results</span></a>
    <a class="home-route-riemannian" href="progress/index.html#riemannian"><strong>Riemannian Optimization</strong><span>Boumal source route</span></a>
    <a class="home-route-optimisation" href="progress/index.html#optimisation"><strong>Optimisation</strong><span>Sinho Chewi · arXiv:2605.07006</span></a>
    <a href="progress/index.html#optimal-transport"><strong>Statistical Optimal Transport Route</strong><span>transport, geometry and statistics</span></a>
    <a href="progress/index.html#higher-order-sampling"><strong>Higher-Order Smoothness × Sampling</strong><span>fixed-oracle, cost-aware research</span></a>
    <a href="progress/index.html#discrete-sampling"><strong>Discrete Sampling Route</strong><span>Ising / Glauber and finite-state mixing</span></a>
    <a href="progress/index.html#mcmc"><strong>Markov Chain Monte Carlo Route</strong><span>Kernel design, scaling, general-state convergence and estimation</span></a>
  </div>
  <p><a class="button" href="progress/index.html">Open unified Current Progress</a></p>
</section>
<section class="home-harness" data-harness-home="true">
  <div class="section-heading"><span>ASTIS Harness</span><h2>One verification and reuse protocol for every route.</h2></div>
  <p>Each theorem-sized task is a Frontier Cell. Parallel workers may explore independently, but shared lower-level lemmas are searched/reused first, new shared foundations get one canonical shared cell, and only independently verified work enters the single stabilization lane.</p>
  <figure><img src="assets/astis-harness-current.svg" alt="ASTIS Harness theorem-driven verification workflow"></figure>
  <p><a class="button" href="workflow/index.html">Open Harness</a></p>
</section>
"""


def patch_home(text: str) -> str:
    if 'data-formalization-progress-home="true"' in text:
        return text
    pattern = re.compile(r'(<section class="source-portal-grid source-portal-grid-seven".*?</section>)', re.S)
    if not pattern.search(text):
        raise RuntimeError("homepage seven-library portal section missing")
    return pattern.sub(lambda match: match.group(1) + home_blocks(), text, count=1)


def transform_site(output: Path) -> None:
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        text = library_shelves.replace_sidebar(text, rel)
        text = library_shelves.add_style(text, rel)
        text = insert_progress_sidebar(text, rel)
        text = patch_site_nav(text, rel)
        text = retarget_progress_links(text, rel)
        text = text.replace("First-Order Optimization", "Optimisation")
        text = text.replace("cross-library bridges, and compression candidates.", "cross-library bridges, and shared-interface candidates.")
        text = add_style(text, rel, STYLE_NAME)
        if rel.startswith("progress/") or rel == OLD_SAMPLEWIKI_PROGRESS or library_shelves.is_new_library_page(rel):
            text = library_shelves.inherit_canonical_theme(text, rel, output)
            text = text.replace(f'{prefix(rel)}index.html#samplinglib', f'{prefix(rel)}index.html')
        if rel == "index.html":
            text = patch_home(text)
        path.write_text(text, encoding="utf-8", newline="\n")


def validate(output: Path) -> None:
    errors: list[str] = []
    required = {
        OVERVIEW: (
            'data-unified-progress-dashboard="true"',
            'id="samplewiki"',
            'id="riemannian"',
            'id="optimisation"',
            "SampleWiki Route",
            "Riemannian Optimization",
            "Optimisation",
            "claimed",
            "independently verified",
            "new_canonical_shared",
        ),
        SAMPLEWIKI_DETAIL: ("SampleWiki dependency and audit detail", "Source audit and Lean progress"),
        RIEMANNIAN_ROUTE: ("Current Progress is now one collaboration dashboard", "index.html#riemannian"),
        OPTIMISATION_ROUTE: ("Current Progress is now one collaboration dashboard", "index.html#optimisation"),
        "index.html": ('data-formalization-progress-home="true"', 'data-harness-home="true"', HARNESS_NAME),
    }
    for rel, markers in required.items():
        path = output / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing {marker}")

    for rel, anchor in (
        (SAMPLEWIKI_ROUTE, "samplewiki"),
        (RIEMANNIAN_ROUTE, "riemannian"),
        (OPTIMISATION_ROUTE, "optimisation"),
        (OLD_FIRST_ORDER_ROUTE, "optimisation"),
    ):
        path = output / rel
        if not path.exists() or f"index.html#{anchor}" not in path.read_text(encoding="utf-8"):
            errors.append(f"{rel}: route alias does not target unified dashboard #{anchor}")

    alias = output / OLD_SAMPLEWIKI_PROGRESS
    if not alias.exists() or "progress/index.html#samplewiki" not in alias.read_text(encoding="utf-8"):
        errors.append("legacy SampleWiki progress route is not a dashboard alias")

    cells = astis_frontier_cells.load_cells()
    errors.extend(f"Frontier Cell protocol: {error}" for error in astis_frontier_cells.validate_cells(cells))

    canonical = output / library_shelves.CANONICAL_THEME_PAGE
    canonical_text = canonical.read_text(encoding="utf-8") if canonical.exists() else ""
    canonical_styles = set(library_shelves.stylesheet_names(canonical_text))
    canonical_tag_match = re.search(r"<html[^>]*>", canonical_text)
    canonical_tag = canonical_tag_match.group(0) if canonical_tag_match else ""
    for rel in (OVERVIEW, SAMPLEWIKI_DETAIL, RIEMANNIAN_ROUTE, OPTIMISATION_ROUTE):
        path = output / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        styles = set(library_shelves.stylesheet_names(text))
        missing = canonical_styles - styles
        if missing:
            errors.append(f"{rel}: Current Progress theme differs from Log-Concave Sampling; missing {sorted(missing)}")
        tag_match = re.search(r"<html[^>]*>", text)
        if canonical_tag and (not tag_match or tag_match.group(0) != canonical_tag):
            errors.append(f"{rel}: html theme attributes differ from Log-Concave Sampling")
        if '<span class="brand-mark">S</span>' not in text or '<strong>Samplinglib</strong>' not in text:
            errors.append(f"{rel}: Samplinglib brand shell differs from canonical reader")

    for path in output.rglob("*.html"):
        rel = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        if 'class="sidebar-group sidebar-progress"' not in text:
            errors.append(f"{rel}: Current Progress sidebar missing")
            break
        for marker in PRIVATE_PUBLIC_MARKERS:
            if marker in text:
                errors.append(f"{rel}: private research marker leaked: {marker}")

    if not (output / "assets" / STYLE_NAME).exists():
        errors.append(f"missing assets/{STYLE_NAME}")
    if not (output / "assets" / HARNESS_NAME).exists():
        errors.append(f"missing assets/{HARNESS_NAME}")
    if errors:
        raise RuntimeError("formalization progress validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_CSS, assets / STYLE_NAME)
    shutil.copyfile(HARNESS, assets / HARNESS_NAME)

    lift_samplewiki_detail(output)
    write_page(
        output,
        OVERVIEW,
        "Current Progress",
        overview_body(),
        "Unified Samplinglib collaboration dashboard for SampleWiki, Riemannian Optimization, Optimisation, shared Frontier Cells, and the ASTIS Harness state machine.",
    )
    write_alias(output, SAMPLEWIKI_ROUTE, "SampleWiki Route", "samplewiki")
    write_alias(output, RIEMANNIAN_ROUTE, "Riemannian Optimization", "riemannian")
    write_alias(output, OPTIMISATION_ROUTE, "Optimisation", "optimisation")
    write_alias(output, OLD_FIRST_ORDER_ROUTE, "Optimisation", "optimisation")
    write_alias(output, "progress/statistical-optimal-transport.html", "Statistical Optimal Transport Route", "optimal-transport")
    write_alias(output, "progress/higher-order-sampling.html", "Higher-Order Smoothness × Sampling", "higher-order-sampling")
    write_alias(output, "progress/discrete-sampling.html", "Discrete Sampling Route", "discrete-sampling")
    write_alias(output, "progress/mcmc.html", "Markov Chain Monte Carlo Route", "mcmc")
    cross_domain.write_research_page(output)
    transform_site(output)
    validate(output)
    cross_domain.validate_site(output)


if __name__ == "__main__":
    enrich_site()
