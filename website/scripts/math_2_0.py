"""Publish Samplinglib's Math 2.0 mission without changing mathematical status."""
from __future__ import annotations

import re
import shutil
from html import escape
from pathlib import Path

import astis_site

ROOT = Path(__file__).resolve().parents[2]
STYLE_NAME = "math-2-0.css"
TAO_URL = "https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf"

# These are contribution directions, not theorem-completion records.
DIRECTIONS = (
    (1, "Open exposition problems", "Understanding", "Explain the mechanism behind sampling proofs, not just their endpoints.",
     "Source-aligned readers and the Functor Hypergraph expose assumptions and recurring mechanisms.",
     "Choose an opaque argument; publish a motivated explanation with a checked path to its full proof.", "textbook/chapter-01/section-1-2.html", "Read semigroups and functional inequalities"),
    (2, "A living knowledge network", "Foundation", "Connect scattered books and frontier papers through reusable mathematical structure.",
     "Library shelves, SampleWiki cases, source anchors and the shared graph organize ongoing work.",
     "Insert a new result with exact hypotheses, parents, contribution and remaining boundaries.", "example-cases/samplewiki.html", "Explore SampleWiki"),
    (3, "High-quality formal mathematics", "Foundation", "Build reusable probability, geometry, optimisation and sampling interfaces.",
     "Lean declarations, the Registry and independent source review provide a formal foundation.",
     "Stabilize missing shared lemmas with source fidelity and complete Lean proofs.", "declarations/index.html", "Inspect Lean declarations"),
    (4, "New principles and methods", "Research agenda", "Cross-pollinate proof mechanisms across spaces, energies, divergences and dynamics.",
     "The Functor Hypergraph records candidate mirrors with explicit hypothesis and failure maps.",
     "Turn a candidate shared mechanism into a useful explanation, theorem or compiled transport adapter.", "lean-foundations.html", "Explore the Functor Hypergraph"),
    (5, "Proof ablation", "Research agenda", "Keep the theorem fixed; test whether selected proof tools can be removed.",
     "Statement seals, ingredient audits and encoder–denoiser review separate assumptions from proof machinery.",
     "Declare forbidden inputs, find an alternative proof, and independently verify the same conclusion.", "workflow/index.html", "Inspect the verification workflow"),
    (6, "Theorem neighborhoods", "Research agenda", "Vary a theorem's hypotheses and find what still holds, or exactly where it fails.",
     "Typed theorem contracts, frontier cells and negative memory preserve the boundary of each route.",
     "Test weaker curvature or regularity and approximate oracles with separate proofs or checked counterexamples.", "progress/index.html", "Explore current frontiers"),
    (7, "Interpretable mathematical models", "Research agenda", "Make explanations, formal proofs and dependencies useful for specialized open mathematical tools.",
     "Our aligned exposition, Lean interfaces and typed diagnostics provide inspectable material.",
     "Prepare rights-cleared retrieval or model experiments. External references retain their license restrictions.", "live/index.html", "Open the research workspace"),
    (8, "Interactive mathematical teaching", "Understanding", "Help students follow an idea from intuition through proof structure to Lean.",
     "Textbook readers, learning paths and graph views offer different levels of mathematical detail.",
     "Improve motivation, worked examples and navigation, then validate them with learners.", "learning-path/index.html", "Start a learning path"),
    (9, "Model boundaries and failure modes", "Research agenda", "Make the assumptions behind mathematical guarantees available for application audits.",
     "Explicit domains, regularity, oracle contracts and source audits expose where a guarantee applies.",
     "Study discretization, finite precision, tails and model mismatch using formal counterexamples and application evidence.", "rigorous-details.html", "Inspect analytic assumptions"),
)


def mission_strip() -> str:
    return '''<section class="math2-mission" id="math-2-0" aria-labelledby="math2-home-title">
<div><span class="eyebrow">Our mission in Math 2.0</span><h2 id="math2-home-title">Make verified mathematics easier to understand.</h2>
<p>Build a living knowledge network and reusable Lean library. Use their proof structure to explain difficult ideas, improve learning, and open new research routes.</p></div>
<a class="button" href="math-2-0/index.html">Explore our nine contribution directions →</a></section>'''


def render_body() -> str:
    cards = []
    for number, title, group, role, now, next_step, href, label in DIRECTIONS:
        cards.append(f'''<details class="math2-direction" id="direction-{number}"{' open' if number in (2, 3) else ''}>
<summary><span class="math2-number">{number:02}</span><span><strong>{escape(title)}</strong><small>{escape(group)}</small></span></summary>
<div class="math2-direction-body"><p class="math2-role">{escape(role)}</p><p><strong>Current foundation.</strong> {escape(now)}</p>
<p><strong>Next contribution.</strong> {escape(next_step)}</p><a href="../{href}">{escape(label)} →</a></div></details>''')
    return f'''<section class="page-hero compact math2-hero"><div class="eyebrow">Samplinglib · Math 2.0</div>
<h1>Proofs that grow human understanding.</h1><p class="lede">A living network and a reusable Lean library for sampling, optimisation, and geometry. Read the mathematics, explore its mechanisms, and check its assumptions.</p>
<p>Inspired by <a href="{TAO_URL}">Terence Tao's October 2026 lecture</a>, slides 22 and 25–26. These nine directions organize his examples into our contribution agenda.</p>
<div class="hero-actions"><a class="button primary" href="../learning-path/index.html">Learn the mathematics</a><a class="button" href="../lean-foundations.html">Explore proof structure</a><a class="button" href="../declarations/index.html">Inspect Lean</a></div></section>
<section class="math2-layers" aria-label="Mission structure"><article><span>Foundations · 2, 3</span><h2>Connect and verify</h2><p>Living mathematical knowledge and reusable formal libraries.</p></article><article><span>Understanding · 1, 8</span><h2>Explain and teach</h2><p>Motivated exposition and interactive learning built on proof structure.</p></article><article><span>Research · 4, 5, 6, 7, 9</span><h2>Explore and test</h2><p>Cross-pollination, proof ablation, theorem neighborhoods and model boundaries.</p></article></section>
<section><div class="section-heading"><span>Concrete contributions</span><h2>Nine directions, one connected foundation</h2></div><p>Current foundations are linked below. Next contributions are research work to undertake; their own evidence is required before claiming completion.</p><div class="math2-directions">{''.join(cards)}</div></section>
<section class="math2-boundaries"><h2>From proof structure to reliable insight</h2><p>A compressed graph keeps a path to the full proof. A conceptual mirror needs a proved adapter to become a formal edge. Encoder–denoiser review checks meaning; proof ablation additionally removes declared tools while preserving the theorem. Lean checks the stated model; applying it to reality also needs domain evidence.</p></section>
<section><div class="section-heading"><span>A shared mission</span><h2>Three complementary libraries</h2></div><div class="math2-layers"><article><h3>Samplinglib</h3><p>Probability, geometry, optimisation and sampling mechanisms.</p><a href="../libraries/index.html">Explore the libraries →</a></article><article><h3>BanditRLlib</h3><p>Sequential feedback, information, regret and decision theory.</p><a href="https://dakebu.github.io/Auto-Bandit-RL-Proof-In-Sleep/math-2-0/">Explore BanditRLlib →</a></article><article><h3>QuantumComputinglib / ASPBE</h3><p>State and operator contracts, constructive circuits and resource analysis.</p><a href="https://dakebu.github.io/Quantum-Computing-Block-Encoding/math-2-0/">Explore QuantumComputinglib →</a></article></div><p>Shared goals guide collaboration; formal reuse still requires compatible imports or checked adapters.</p></section>'''


def enrich_site(output: Path) -> None:
    assets = output / "assets"
    shutil.copyfile(ROOT / "website" / "static" / STYLE_NAME, assets / STYLE_NAME)
    home = output / "index.html"
    text = home.read_text(encoding="utf-8")
    marker = re.search(r'<section class="ia-home-hero">.*?</section>', text, re.S)
    if marker is None:
        raise RuntimeError("Math 2.0: canonical home hero missing")
    hero = marker.group(0)
    # Keep the canonical masthead and source shelves; add immediate reading routes.
    actions = '<div class="hero-actions math2-reader-actions"><a class="button primary" href="learning-path/index.html">Start learning</a><a class="button" href="lean-foundations.html">Explore proof structure</a><a class="button" href="declarations/index.html">Inspect Lean</a></div>'
    hero = hero.replace("</section>", actions + "</section>")
    text = text[:marker.start()] + hero + mission_strip() + text[marker.end():]
    text = text.replace('<a href="workflow/index.html">ASTIS Harness</a>', '<a href="math-2-0/index.html">Math 2.0 mission</a><a href="workflow/index.html">ASTIS Harness</a>', 1)
    text = text.replace("</head>", f'<link rel="stylesheet" href="assets/{STYLE_NAME}">\n</head>', 1)
    home.write_text(text, encoding="utf-8", newline="\n")

    rel = "math-2-0/index.html"
    page = astis_site.page("Math 2.0", rel, render_body(), active="Home", description="Samplinglib contributions to Math 2.0: living knowledge, Lean proofs, exposition and research.")
    # New pages inherit the existing navigation and visual system.
    import information_architecture
    import visual_polish
    edition = information_architecture.load_json(information_architecture.SOURCE_EDITION)
    page = information_architecture.replace_sidebar(page, edition, rel)
    page = information_architecture.add_style(page, rel)
    page = visual_polish.inject_styles(page, Path(rel))
    import source_lineage
    page = source_lineage.canonical_shell(page, rel, output)
    page = page.replace('<a href="../workflow/index.html">ASTIS Harness</a>', '<a href="../math-2-0/index.html" aria-current="page">Math 2.0 mission</a><a href="../workflow/index.html">ASTIS Harness</a>', 1)
    page = page.replace("</head>", f'<link rel="stylesheet" href="../assets/{STYLE_NAME}">\n</head>', 1)
    astis_site.write_page(output, rel, page)
