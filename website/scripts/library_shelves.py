#!/usr/bin/env python3
"""Add peer-level Boumal and Chewi optimisation shelves to Samplinglib.

The generated library pages deliberately inherit the same presentation stack as
Log-Concave Sampling.  They are not a second mini-site with their own theme.
"""

from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path
from urllib.parse import quote

import astis_site
import cross_domain
import discrete_sampling
import mcmc_library
import publication_reader


ROOT = Path(__file__).resolve().parents[2]
SOURCE_CSS = ROOT / "website" / "static" / "library-shelves.css"
STYLE_NAME = "library-shelves.css"

BOUMAL_URL = "https://www.nicolasboumal.net/book/"
CHEWI_OPT_URL = "https://arxiv.org/pdf/2605.07006"
BECK_URL = "https://epubs.siam.org/doi/book/10.1137/1.9781611974997"
OPTLIB_URL = "https://github.com/optsuite/optlib"
CVXLEAN_URL = "https://github.com/verified-optimization/CvxLean"

BOUMAL = (
    "Introduction",
    "Simple examples",
    "Embedded geometry: first order",
    "First-order optimization algorithms",
    "Embedded geometry: second order",
    "Second-order optimization algorithms",
    "Embedded submanifolds: examples",
    "General manifolds",
    "Quotient manifolds",
    "Additional tools",
    "Geodesic convexity",
)

OPTIMISATION = (
    ("01", "Introduction and basics of convex functions", "§1", 3),
    ("02", "Gradient flow", "§2", 12),
    ("03", "Gradient descent: smooth case", "§3", 18),
    ("04", "Lower bounds for smooth optimization", "§4", 24),
    ("05", "Acceleration", "§5", 29),
    ("06", "Non-smooth convex optimization", "§6", 39),
    ("07", "Frank-Wolfe", "§7", 57),
    ("08", "Proximal methods", "§8", 61),
    ("09", "Fenchel duality", "§9", 67),
    ("10", "Mirror methods", "§10", 76),
    ("11", "Alternating minimization", "§11", 90),
    ("12", "Stochastic optimization", "§12", 104),
    ("13", "Interior point methods", "§13", 127),
    ("A", "Background on symmetric matrices", "Appendix A", 140),
)

CANONICAL_THEME_PAGE = "textbook/index.html"


def prefix(rel: str) -> str:
    return "../" * len(Path(rel).parent.parts)


def current(rel: str, stem: str) -> str:
    return ' aria-current="page"' if rel.startswith(stem) else ""


def libraries_sidebar(rel: str) -> str:
    p = prefix(rel)
    return f"""<section class="sidebar-group sidebar-libraries" data-library-shelves="1">
  <h2><a href="{p}libraries/index.html">Libraries</a></h2>
  <nav class="source-hubs library-source-hubs">
    <a class="source-hub" href="{p}textbook/index.html"{current(rel, "textbook/")}><span class="source-hub-title">Log-Concave Sampling</span><small>Chewi · textbook graph</small></a>
    <a class="source-hub" href="{p}example-cases/samplewiki.html"{current(rel, "example-cases/samplewiki")}><span class="source-hub-title">SampleWiki</span><small>sampling frontier cases</small></a>
    <a class="source-hub" href="{p}libraries/riemannian-optimization/index.html"{current(rel, "libraries/riemannian-optimization/")}><span class="source-hub-title">Riemannian Optimization</span><small>Boumal · 11 chapters</small></a>
    <a class="source-hub" href="{p}libraries/optimisation/index.html"{current(rel, "libraries/optimisation/")}><span class="source-hub-title">Optimisation</span><small>Chewi · arXiv:2605.07006</small></a>
    <a class="source-hub" href="{p}libraries/statistical-optimal-transport/index.html"{current(rel, "libraries/statistical-optimal-transport/")}><span class="source-hub-title">Statistical Optimal Transport</span><small>Chewi · Niles-Weed · Rigollet</small></a>
    <a class="source-hub" href="{p}libraries/discrete-sampling/index.html"{current(rel, "libraries/discrete-sampling/")}><span class="source-hub-title">Discrete Sampling</span><small>Chen · Štefankovič · Vigoda</small></a>
    <a class="source-hub" href="{p}libraries/mcmc/index.html"{current(rel, "libraries/mcmc/")}><span class="source-hub-title">Markov Chain Monte Carlo</span><small>Fearnhead · Nemeth · Oates · Sherlock</small></a>
  </nav>
</section>"""


def replace_sidebar(text: str, rel: str) -> str:
    pattern = re.compile(r'<section class="sidebar-group sidebar-libraries".*?</section>', re.S)
    changed, count = pattern.subn(libraries_sidebar(rel), text, count=1)
    if count:
        return changed

    start = text.find('<div class="sidebar-contents">')
    end = text.find('<div class="sidebar-utility">', start)
    if start < 0 or end < 0:
        raise RuntimeError(f"{rel}: sidebar not found")
    p = prefix(rel)
    fallback = f"""<div class="sidebar-contents" data-ia-version="2" data-library-shelves="1">
{libraries_sidebar(rel)}
<section class="sidebar-group"><h2>Proof graph</h2><nav>
<a href="{p}lean-foundations.html">Proof Atlas</a>
<a href="{p}underlying-lean-graph/index.html">Underlying Lean Graph</a>
<a href="{p}implementation-map/index.html">Implementation map</a>
</nav></section>
<section class="sidebar-group"><h2>Project</h2><nav>
<a href="{p}workflow/index.html">ASTIS Harness</a>
<a href="{p}contribute/index.html">Contribute</a>
<a href="{p}attribution/index.html">Attribution</a>
</nav></section>
</div>
"""
    return text[:start] + fallback + text[end:]


def stylesheet_names(text: str) -> list[str]:
    return [
        Path(value).name
        for value in re.findall(r'<link\s+rel="stylesheet"\s+href="([^"]+)"', text)
    ]


def canonical_theme_styles(output: Path) -> list[str]:
    canonical = output / CANONICAL_THEME_PAGE
    if not canonical.exists():
        raise RuntimeError(f"canonical Samplinglib theme page missing: {CANONICAL_THEME_PAGE}")
    names = stylesheet_names(canonical.read_text(encoding="utf-8"))
    if "site.css" not in names or "information-architecture.css" not in names:
        raise RuntimeError("canonical Samplinglib theme stack is incomplete")
    return names


def inherit_canonical_theme(text: str, rel: str, output: Path) -> str:
    """Give generated library pages exactly the Chewi reader presentation stack."""
    existing = set(stylesheet_names(text))
    additions = []
    for name in canonical_theme_styles(output):
        if name in existing:
            continue
        additions.append(f'  <link rel="stylesheet" href="{prefix(rel)}assets/{escape(name)}">')
        existing.add(name)
    if additions:
        if "</head>" not in text:
            raise RuntimeError(f"{rel}: missing </head> while inheriting canonical theme")
        text = text.replace("</head>", "\n".join(additions) + "\n</head>", 1)
    return text


def add_style(text: str, rel: str) -> str:
    href = f"{prefix(rel)}assets/{STYLE_NAME}"
    if href in text:
        return text
    if "</head>" not in text:
        raise RuntimeError(f"{rel}: missing </head>")
    return text.replace("</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', 1)


def badge(label: str, css: str = "gray") -> str:
    return f'<span class="status status-{css}">{escape(label)}</span>'


def cards(chapters: tuple[str, ...]) -> str:
    return "".join(
        f"""<article class="library-chapter-card">
<div class="library-chapter-number">{i:02d}</div>
<div><div class="card-meta">{publication_reader.status("riemannian-optimization", f"{i:02d}")}</div>
<h2><a href="chapter-{i:02d}.html">{escape(title)}</a></h2>
<p>Source map, theorem nodes, upstream matches, and exact Lean correspondence will be attached here.</p></div>
</article>"""
        for i, title in enumerate(chapters, 1)
    )


def optimisation_cards() -> str:
    rows = []
    for chapter_id, title, source_section, _ in OPTIMISATION:
        href = "appendix-a.html" if chapter_id == "A" else f"chapter-{chapter_id}.html"
        rows.append(
            f"""<article class="library-chapter-card">
<div class="library-chapter-number">{escape(chapter_id)}</div>
<div><div class="card-meta">{publication_reader.status("optimisation", chapter_id)}</div>
<h2><a href="{href}">{escape(title)}</a></h2>
<p>{escape(source_section)} · {len(publication_reader.publication.chapter_progress('optimisation', chapter_id)['proof_declarations'])} mapped, independently verified local proof declarations. Source equivalence and chapter completion are separate.</p></div>
</article>"""
        )
    return "".join(rows)


def index_body(*, eyebrow: str, title: str, lede: str, source: str, chapters: tuple[str, ...], contract: str) -> str:
    return f"""
<section class="page-hero compact library-book-hero">
<div class="eyebrow">{escape(eyebrow)}</div><h1>{escape(title)}</h1>
<p class="lede">{escape(lede)}</p>
<div class="library-meta-row"><span><strong>Status</strong>chapter environment established</span>
<a href="{escape(source)}">Primary source ↗</a></div>
</section>
<section class="library-integration-note">
<div class="section-heading"><span>Formalization contract</span><h2>Map first, reuse first, prove only real gaps.</h2></div>
<p>{escape(contract)}</p>
<div class="library-status-key">{badge("reuse", "blue")}{badge("adapt", "yellow")}{badge("missing", "orange")}{badge("out of scope")}</div>
</section>
<section><div class="section-heading"><span>Book contents</span><h2>Chapter scaffolds</h2></div>
<div class="library-chapter-list">{cards(chapters)}</div></section>
"""


def mathematical_chapter_map(library: str, chapter: str) -> str:
    """Author chapter goals once in source publication metadata; no status inference."""
    maps = [item['chapter_reader'] for item in publication_reader.publication.load()
            if item['library'] == library and item['chapter'] == chapter
            and item.get('chapter_reader')]
    if not maps:
        return ''
    if any(m != maps[0] for m in maps[1:]):
        raise ValueError(f'Conflicting reader maps for {library}/{chapter}')
    reader = maps[0]
    route = ''.join(
        f'<li><h3>{escape(step["title"])}</h3><p>{escape(step["text"])}</p></li>'
        for step in reader['route'])
    roots = ''.join(
        f'<li><a href="../../lean-foundations.html?view=lean&amp;focus={quote("decl:" + name, safe="")}&amp;q={quote(name, safe="")}">'
        f'<code>{escape(name)}</code></a></li>' for name in reader['shared_roots'])
    return ('<section class="library-chapter-contract" data-chapter-knowledge-map="1">'
            f'<div class="section-heading"><span>Chapter goal</span><h2>{escape(reader["title"])}</h2></div>'
            f'<p class="lede">{escape(reader["goal"])}</p>'
            '<h2>Mathematical knowledge map</h2><ol>' + route + '</ol>'
            f'<p><strong>Current boundary.</strong> {escape(reader["boundary"])}</p>'
            '<details><summary>Source anchors and shared formal roots</summary>'
            f'<p>{escape(reader["source_scope"])}</p><ul>{roots}</ul></details></section>')


def chapter_body(library: str, number: str, title: str, source: str, upstream: str, source_label: str = "Primary source", publication_status: str = "") -> str:
    return f"""
<section class="page-hero compact library-chapter-hero">
<div class="eyebrow">{escape(library)} · {escape(number)}</div>
<h1>{escape(title)}</h1>
<p class="lede">Stable source-facing chapter environment inside the shared Samplinglib reader.</p>
<div class="tag-row">{publication_status or badge("scaffold")}<span>source map</span><span>Full source closure not claimed</span></div>
</section>
<section class="library-chapter-contract">
<div class="section-heading"><span>Planned route</span><h2>Source → theorem map → reusable Lean nodes</h2></div>
<div class="library-contract-grid">
<article><span>01</span><h3>Source audit</h3><p>Definitions, theorems, assumptions, proof route, and exact anchors.</p></article>
<article><span>02</span><h3>Upstream alignment</h3><p>{escape(upstream)}</p></article>
<article><span>03</span><h3>Frontier Cells</h3><p>Only genuinely missing mathematical edges become theorem-sized tasks.</p></article>
<article><span>04</span><h3>Graph placement</h3><p>Dependencies, consumers, cross-library bridges, and reusable shared interfaces.</p></article>
</div><p><a href="{escape(source)}">{escape(source_label)} ↗</a></p>
</section>
<section class="ia-project-note">This page establishes a stable source route and truth boundary; it does not claim a completed formalization.</section>
"""


def write_redirect(output: Path, rel: str, target: str, title: str) -> None:
    p = prefix(rel)
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Samplinglib · moved</div>
<h1>{escape(title)}</h1><p class="lede">This historical route now points to the public Optimisation formalization based on Sinho Chewi's lecture notes.</p>
<p><a class="button primary" href="{escape(target)}">Open Optimisation</a></p></section>
"""
    text = astis_site.page(title, rel, body, active="Libraries")
    text = text.replace("</head>", f'  <meta http-equiv="refresh" content="0; url={escape(target)}">\n</head>', 1)
    astis_site.write_page(output, rel, text)


def write_pages(output: Path) -> None:
    home = """
<section class="page-hero compact library-index-hero">
<div class="eyebrow">Samplinglib · seven first-class libraries</div>
<h1>One formal graph across sampling and optimisation.</h1>
<p class="lede">Public mathematical sources provide stable coordinate systems; SampleWiki inserts frontier results into the same reusable theorem graph.</p>
</section>
<section class="library-index-grid">
<article class="library-index-card library-active"><div class="portal-kicker">Textbook</div><h2>Log-Concave Sampling</h2><p>Chewi's source-aligned textbook graph, including the official Chapter 2 supplement.</p><a class="button primary" href="../textbook/index.html">Open textbook</a></article>
<article class="library-index-card library-active"><div class="portal-kicker">Research frontier</div><h2>SampleWiki</h2><p>Source-pinned frontier results inserted into the reusable graph.</p><a class="button primary" href="../example-cases/samplewiki.html">Open SampleWiki</a></article>
<article class="library-index-card"><div class="portal-kicker">Chapter scaffold</div><h2>Riemannian Optimization</h2><p>Boumal's eleven-chapter geometry and optimization route.</p><a class="button" href="riemannian-optimization/index.html">Open library</a></article>
<article class="library-index-card"><div class="portal-kicker">Public arXiv notes + upstream reuse</div><h2>Optimisation</h2><p>Formalising Sinho Chewi's <em>Lectures on Optimization</em>, with Mathlib, Optlib and CvxLean searched before new proofs.</p><a class="button" href="optimisation/index.html">Open library</a></article>
<article class="library-index-card"><div class="portal-kicker">Chapter scaffold</div><h2>Statistical Optimal Transport</h2><p>Chewi, Niles-Weed and Rigollet: eight chapters and two appendices, with shared transport, convexity and probability foundations.</p><a class="button" href="statistical-optimal-transport/index.html">Open library</a></article>
<article class="library-index-card"><div class="portal-kicker">Finite-state source scaffold</div><h2>Discrete Sampling</h2><p>Ising/Glauber, hard-core and matroid sampling. Chen, Štefankovič and Vigoda, with complementary model and mixing-time sources.</p><a class="button" href="discrete-sampling/index.html">Open library</a></article>
<article class="library-index-card"><div class="portal-kicker">Method-family source scaffold</div><h2>Markov Chain Monte Carlo</h2><p>Scalable Monte Carlo for Bayesian Learning: six primary chapters, with source-pinned extended reading paths.</p><a class="button" href="mcmc/index.html">Open library</a></article>
</section>
<section class="ia-project-note"><strong>Truth boundary.</strong> Scaffold means public chapter routes and source boundaries, not completed Lean proofs.</section>
"""
    astis_site.write_page(output, "libraries/index.html", astis_site.page("Libraries", "libraries/index.html", home, active="Libraries"))

    boumal = index_body(
        eyebrow="Riemannian Optimization Library · Boumal",
        title="An Introduction to Optimization on Smooth Manifolds",
        lede="A chapter-by-chapter graph for smooth-manifold geometry, Riemannian algorithms, and Euclidean-to-manifold transfer.",
        source=BOUMAL_URL,
        chapters=BOUMAL,
        contract="Search Mathlib and Samplinglib geometry interfaces before opening new proofs; make every convention bridge explicit.",
    )
    astis_site.write_page(output, "libraries/riemannian-optimization/index.html", astis_site.page("Riemannian Optimization", "libraries/riemannian-optimization/index.html", boumal, active="Libraries"))
    for i, title in enumerate(BOUMAL, 1):
        path = f"libraries/riemannian-optimization/chapter-{i:02d}.html"
        body = chapter_body("Riemannian Optimization", f"Chapter {i:02d}", title, BOUMAL_URL, "Search Mathlib and local geometry interfaces; adapt only real statement or convention differences.")
        reader_map = mathematical_chapter_map('riemannian-optimization', f'{i:02d}')
        if reader_map:
            start = body.index('<section class="library-chapter-contract">')
            end = body.index('</section>', start) + len('</section>')
            body = body[:start] + reader_map + body[end:]
        astis_site.write_page(output, path, astis_site.page(f"Riemannian Optimization {i}: {title}", path, body, active="Libraries"))

    optimisation = f"""
<section class="page-hero compact library-book-hero">
<div class="eyebrow">Optimisation Library · Sinho Chewi</div><h1>Lectures on Optimization</h1>
<p class="lede">A public theorem-proof formalization route following arXiv:2605.07006 section by section.</p>
<div class="library-meta-row"><span><strong>Status</strong>{publication_reader.status('optimisation')}</span><a href="{CHEWI_OPT_URL}">Primary arXiv source ↗</a></div>
</section>
<section class="library-integration-note">
<div class="section-heading"><span>Source hierarchy</span><h2>Chewi is the formalization target; Beck is background.</h2></div>
<p>Chewi's notes are the controlling public source. The notes themselves state that they are primarily based on Bubeck (2015), Beck (2017), and Nesterov (2018). Those works remain attributed background and cross-check references. Mathlib, Optlib, and CvxLean are searched before new Lean declarations are introduced.</p>
<div class="library-status-key">{badge("reuse", "blue")}{badge("adapt", "yellow")}{badge("missing", "orange")}{badge("out of scope")}</div>
</section>
<section><div class="section-heading"><span>Lecture-note contents</span><h2>13 chapters + Appendix A</h2></div><div class="library-chapter-list">{optimisation_cards()}</div></section>
<section><div class="section-heading"><span>Formal upstreams</span><h2>Reuse checked formal mathematics before reproving it.</h2></div>
<div class="upstream-library-grid">
<article><h3>Optlib</h3><p>Convex analysis, proximal maps, first-order algorithms, acceleration, block methods, and ADMM.</p><a href="{OPTLIB_URL}">Open Optlib ↗</a></article>
<article><h3>CvxLean</h3><p>Formal optimization problems, equivalence, reduction, relaxation, and verified transformations.</p><a href="{CVXLEAN_URL}">Open CvxLean ↗</a></article>
</div></section>
"""
    astis_site.write_page(output, "libraries/optimisation/index.html", astis_site.page("Optimisation", "libraries/optimisation/index.html", optimisation, active="Libraries"))
    for chapter_id, title, source_section, page in OPTIMISATION:
        path = "libraries/optimisation/appendix-a.html" if chapter_id == "A" else f"libraries/optimisation/chapter-{chapter_id}.html"
        source = f"{CHEWI_OPT_URL}#page={page}"
        number = f"{source_section} · source p. {page}"
        body = chapter_body("Optimisation", number, title, source, "Search Mathlib, Optlib, CvxLean, and shared Samplinglib interfaces; preserve the exact Chewi statement and use a small adapter when conventions differ.", source_label="Open exact Chewi source", publication_status=publication_reader.status('optimisation', chapter_id))
        astis_site.write_page(output, path, astis_site.page(f"Optimisation {source_section}: {title}", path, body, active="Libraries"))

    cross_domain.write_ot_pages(output, __import__(__name__))
    discrete_sampling.write_pages(output, __import__(__name__))
    mcmc_library.write_pages(output, __import__(__name__))

    write_redirect(output, "libraries/first-order-optimization/index.html", "../optimisation/index.html", "First-Order Optimization moved to Optimisation")
    for i in range(1, 16):
        write_redirect(output, f"libraries/first-order-optimization/chapter-{i:02d}.html", "../optimisation/index.html", "First-Order Optimization moved to Optimisation")


def seven_portals() -> str:
    return """
<section class="source-portal-grid source-portal-grid-seven" aria-label="Primary mathematical libraries">
<article class="source-portal source-portal-book"><div class="portal-kicker">Textbook</div><h2>Log-Concave Sampling</h2><p>Chewi's source-aligned textbook graph plus official supplement.</p><div class="portal-actions"><a class="button primary" href="textbook/index.html">Read the book</a></div></article>
<article class="source-portal source-portal-wiki"><div class="portal-kicker">Research frontier</div><h2>SampleWiki</h2><p>Source-pinned frontier results and theorem-sized graph insertions.</p><div class="portal-actions"><a class="button primary" href="example-cases/samplewiki.html">Explore SampleWiki</a></div></article>
<article class="source-portal source-portal-riemannian"><div class="portal-kicker">Chapter scaffold</div><h2>Riemannian Optimization</h2><p>Boumal's eleven chapters on geometry and manifold algorithms.</p><div class="portal-actions"><a class="button" href="libraries/riemannian-optimization/index.html">Open library</a></div></article>
<article class="source-portal source-portal-optimization"><div class="portal-kicker">Public arXiv formalization</div><h2>Optimisation</h2><p>Sinho Chewi's <em>Lectures on Optimization</em> with formal-upstream reuse.</p><div class="portal-actions"><a class="button" href="libraries/optimisation/index.html">Open library</a></div></article>
<article class="source-portal source-portal-transport"><div class="portal-kicker">Chapter scaffold</div><h2>Statistical Optimal Transport</h2><p>Chewi · Niles-Weed · Rigollet. Eight chapters and two appendices in the shared reader.</p><div class="portal-actions"><a class="button" href="libraries/statistical-optimal-transport/index.html">Open library</a></div></article>
<article class="source-portal source-portal-discrete"><div class="portal-kicker">Finite-state source scaffold</div><h2>Discrete Sampling</h2><p>Ising / Glauber, hard-core and matroid sampling. Not continuous-state time discretization.</p><div class="portal-actions"><a class="button" href="libraries/discrete-sampling/index.html">Open library</a></div></article>
<article class="source-portal source-portal-mcmc"><div class="portal-kicker">Method-family source scaffold</div><h2>Markov Chain Monte Carlo</h2><p>Fearnhead · Nemeth · Oates · Sherlock. Modern MCMC, shared kernels, scalable algorithms and estimation.</p><div class="portal-actions"><a class="button" href="libraries/mcmc/index.html">Open library</a></div></article>
</section>
"""


def patch_public_optimisation_names(text: str) -> str:
    text = text.replace("libraries/first-order-optimization/index.html", "libraries/optimisation/index.html")
    text = text.replace("First-Order Optimization", "Optimisation")
    text = text.replace("Beck · Optlib · CvxLean", "Chewi · Optlib · CvxLean")
    return text


def patch_special(text: str, rel: str) -> str:
    text = patch_public_optimisation_names(text)
    if rel == "index.html":
        text, count = re.subn(r'<section class="source-portal-grid".*?</section>', seven_portals(), text, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("index.html: library portal grid not found")
        text = text.replace("Two mathematical sources feed one reusable Lean proof graph.", "Six mathematical libraries feed one reusable Lean proof graph.")
    elif rel == "lean-foundations.html":
        old = '<div class="atlas-source-grid"><a href="textbook/index.html">Log-Concave Sampling</a><a href="example-cases/samplewiki.html">SampleWiki</a></div>'
        new = '<div class="atlas-source-grid atlas-source-grid-seven"><a href="textbook/index.html">Log-Concave Sampling</a><a href="example-cases/samplewiki.html">SampleWiki</a><a href="libraries/riemannian-optimization/index.html">Riemannian Optimization</a><a href="libraries/optimisation/index.html">Optimisation</a><a href="libraries/statistical-optimal-transport/index.html">Statistical Optimal Transport</a><a href="libraries/discrete-sampling/index.html">Discrete Sampling</a><a href="libraries/mcmc/index.html">Markov Chain Monte Carlo</a></div>'
        text = text.replace(old, new)
    elif rel == "attribution/index.html" and 'data-library-attribution="true"' not in text:
        block = f"""
<section class="library-attribution" data-library-attribution="true">
<div class="section-heading"><span>Textbooks and formal upstreams</span><h2>Additional Samplinglib library sources</h2></div>
<div class="upstream-library-grid">
<article><h3>Nicolas Boumal</h3><p><em>An Introduction to Optimization on Smooth Manifolds</em> supplies the Riemannian route.</p><a href="{BOUMAL_URL}">Book site ↗</a></article>
<article><h3>Sinho Chewi</h3><p><em>Lectures on Optimization</em> (arXiv:2605.07006) supplies the public Optimisation formalization route.</p><a href="{CHEWI_OPT_URL}">arXiv PDF ↗</a></article>
<article><h3>Chewi · Niles-Weed · Rigollet</h3><p><em>Statistical Optimal Transport</em> supplies the OT source route. Villani, Santambrogio and Ambrosio–Gigli–Savaré provide targeted background for omitted details, not replacement source theorems.</p><a href="https://chewisinho.github.io/st_flour.pdf">Public textbook ↗</a></article>
<article><h3>Chen · Štefankovič · Vigoda</h3><p><em>Spectral Independence and Local-to-Global Techniques for Optimal Mixing of Markov Chains</em>, arXiv:2307.13826v4, supplies the Discrete Sampling spine. Levin–Peres (with Wilmer) and Duminil-Copin supply targeted mixing/model background; §12 proofs are recovered from cited originals, not silently assumed.</p><a href="https://arxiv.org/abs/2307.13826v4">Pinned monograph ↗</a></article>
<article><h3>Optlib</h3><p>Audited convex-analysis and algorithm theorem source.</p><a href="{OPTLIB_URL}">Repository ↗</a></article>
<article><h3>CvxLean</h3><p>Audited optimization-problem and transformation source.</p><a href="{CVXLEAN_URL}">Repository ↗</a></article>
</div></section>
"""
        end = text.rfind("</main>")
        if end < 0:
            raise RuntimeError("attribution/index.html: missing main")
        text = text[:end] + block + text[end:]
    return text


def is_new_library_page(rel: str) -> bool:
    return rel == "libraries/index.html" or rel.startswith("libraries/riemannian-optimization/") or rel.startswith("libraries/optimisation/") or rel.startswith("libraries/statistical-optimal-transport/") or rel.startswith("libraries/discrete-sampling/") or rel.startswith("libraries/mcmc/")


def transform(output: Path) -> None:
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output).as_posix()
        text = patch_special(path.read_text(encoding="utf-8"), rel)
        text = replace_sidebar(text, rel)
        if is_new_library_page(rel):
            text = inherit_canonical_theme(text, rel, output)
        text = add_style(text, rel)
        path.write_text(text, encoding="utf-8", newline="\n")


def validate(output: Path) -> None:
    errors: list[str] = []
    required = {
        "index.html": ("source-portal-grid-seven", "Riemannian Optimization", "Optimisation"),
        "libraries/index.html": ("seven first-class libraries", "Optimisation"),
        "libraries/riemannian-optimization/index.html": ("An Introduction to Optimization on Smooth Manifolds", "chapter environment established"),
        "libraries/optimisation/index.html": ("Lectures on Optimization", "arXiv:2605.07006", "Optlib", "CvxLean"),
        "libraries/statistical-optimal-transport/index.html": ("Statistical Optimal Transport", "Jonathan Niles-Weed", "Philippe Rigollet", "chapter environment established"),
        "libraries/discrete-sampling/index.html": ("arXiv:2307.13826v4", "Ising", "source-boundaries"),
        "attribution/index.html": ('data-library-attribution="true"', "Sinho Chewi", "Nicolas Boumal"),
    }
    forbidden = ("<strong>Owners</strong>", "Andi · Dake", "Dake · Huanjian · Andi")
    canonical_styles = set(canonical_theme_styles(output))
    canonical_html = re.search(r"<html[^>]*>", (output / CANONICAL_THEME_PAGE).read_text(encoding="utf-8"))
    canonical_tag = canonical_html.group(0) if canonical_html else ""
    for rel, markers in required.items():
        path = output / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing {marker}")
        for marker in forbidden:
            if marker in text:
                errors.append(f"{rel}: leaked internal assignment marker {marker!r}")
        if is_new_library_page(rel):
            styles = set(stylesheet_names(text))
            missing = canonical_styles - styles
            if missing:
                errors.append(f"{rel}: does not inherit canonical Samplinglib theme styles: {sorted(missing)}")
            tag = re.search(r"<html[^>]*>", text)
            if canonical_tag and (not tag or tag.group(0) != canonical_tag):
                errors.append(f"{rel}: html theme attributes differ from Log-Concave Sampling")
            if '<span class="brand-mark">S</span>' not in text or '<strong>Samplinglib</strong>' not in text:
                errors.append(f"{rel}: Samplinglib brand shell differs from canonical reader")
    for i in range(1, len(BOUMAL) + 1):
        if not (output / f"libraries/riemannian-optimization/chapter-{i:02d}.html").exists():
            errors.append(f"missing Boumal chapter {i}")
    for chapter_id, _, _, _ in OPTIMISATION:
        rel = "libraries/optimisation/appendix-a.html" if chapter_id == "A" else f"libraries/optimisation/chapter-{chapter_id}.html"
        if not (output / rel).exists():
            errors.append(f"missing Optimisation source chapter {chapter_id}")
    old = output / "libraries/first-order-optimization/index.html"
    if not old.exists() or "../optimisation/index.html" not in old.read_text(encoding="utf-8"):
        errors.append("historical First-Order Optimization route does not redirect to Optimisation")
    for path in output.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        start = text.find('<section class="sidebar-group sidebar-libraries"')
        stop = text.find("</section>", start)
        side = text[start:stop] if start >= 0 and stop >= 0 else ""
        if not all(name in side for name in ("Log-Concave Sampling", "SampleWiki", "Riemannian Optimization", "Optimisation", "Statistical Optimal Transport", "Discrete Sampling")):
            errors.append(f"{path.relative_to(output)}: incomplete Libraries sidebar")
            break
    if not (output / "assets" / STYLE_NAME).exists():
        errors.append("missing library-shelves.css")
    if errors:
        raise RuntimeError("library shelves validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path) -> None:
    write_pages(output)
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_CSS, assets / STYLE_NAME)
    transform(output)
    validate(output)
