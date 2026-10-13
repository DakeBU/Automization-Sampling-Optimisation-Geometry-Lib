#!/usr/bin/env python3
"""Final public source-lineage overlay for Samplinglib.

This layer makes mathematical provenance explicit:
- Chewi's book is the primary sampling source;
- supp.pdf is an official Chapter 2 source layer;
- background textbooks justify omitted standard details without replacing Chewi;
- Chewi's arXiv Lectures on Optimization are the public Optimisation target;
- Beck/Bubeck/Nesterov remain attributed background/cross-check sources.
"""

from __future__ import annotations

import json
import shutil
from html import escape
from pathlib import Path
from typing import Any

import astis_site
import formalization_progress
import library_shelves


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
DATA_PATH = ROOT / "website" / "content" / "source_lineage.json"
SOURCE_CSS = ROOT / "website" / "static" / "source-lineage.css"
STYLE_NAME = "source-lineage.css"

TEXTBOOK_INDEX = "textbook/index.html"
CHEWI_CHAPTER_2 = "textbook/chapter-02.html"
ATTRIBUTION = "attribution/index.html"
OPT_PROGRESS = "progress/optimisation.html"
OLD_OPT_PROGRESS = "progress/first-order-optimization.html"


def load_data() -> dict[str, Any]:
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError("source_lineage.json must contain an object")
    return raw


def prefix(rel: str) -> str:
    return "../" * len(Path(rel).parent.parts)


def add_style(text: str, rel: str) -> str:
    href = f"{prefix(rel)}assets/{STYLE_NAME}"
    if href in text:
        return text
    if "</head>" not in text:
        raise RuntimeError(f"{rel}: missing </head>")
    return text.replace("</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', 1)


def canonical_shell(text: str, rel: str, output: Path) -> str:
    """Apply the same final reader shell used by the established Samplinglib pages."""
    text = library_shelves.replace_sidebar(text, rel)
    text = formalization_progress.insert_progress_sidebar(text, rel)
    text = formalization_progress.patch_site_nav(text, rel)
    # formalization_progress is intentionally backwards-compatible with the old
    # route name, so normalize the public route atomically after reusing it.
    text = text.replace("progress/first-order-optimization.html", "progress/optimisation.html")
    text = text.replace("first-order-optimization.html", "optimisation.html")
    text = text.replace("First-Order Optimization", "Optimisation")
    text = library_shelves.inherit_canonical_theme(text, rel, output)
    text = add_style(text, rel)
    # Late astis_site.page calls still contain an obsolete root anchor that the
    # final information-architecture overlay removes from established pages.
    text = text.replace(f'{prefix(rel)}index.html#samplinglib', f'{prefix(rel)}index.html')
    return text


def append_main(output: Path, rel: str, html: str, marker: str) -> None:
    path = output / rel
    if not path.exists():
        raise RuntimeError(f"missing source-lineage page: {rel}")
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    text = add_style(text, rel)
    end = text.rfind("</main>")
    if end < 0:
        raise RuntimeError(f"{rel}: missing </main>")
    text = text[:end] + html + text[end:]
    path.write_text(text, encoding="utf-8", newline="\n")


def linked_name(ref: dict[str, Any]) -> str:
    name = escape(str(ref.get("name", "")))
    url = str(ref.get("url", "")).strip()
    return f'<a href="{escape(url)}">{name}</a>' if url else name


def source_stack_html(data: dict[str, Any]) -> str:
    chewi = dict(data["chewi_log_concave_sampling"])
    primary = dict(chewi["primary"])
    supplement = dict(chewi["official_supplement"])
    groups = [dict(item) for item in chewi.get("background_reference_groups", []) if isinstance(item, dict)]
    group_cards = []
    for group in groups:
        refs = [dict(item) for item in group.get("references", []) if isinstance(item, dict)]
        group_cards.append(
            f"""
<article class="source-stack-card">
  <span class="source-stack-role">Background / rigorous completion</span>
  <h3>{escape(str(group.get('title', 'Background references')))}</h3>
  <p>{escape(str(group.get('role', '')))}</p>
  <ul>{''.join(f'<li>{linked_name(ref)}</li>' for ref in refs)}</ul>
</article>"""
        )
    return f"""
<section class="source-stack" data-chewi-source-stack="true">
  <div class="section-heading"><span>Mathematical source hierarchy</span><h2>What controls a formalized statement?</h2></div>
  <p class="source-hierarchy-note"><strong>Primary theorem authority stays explicit.</strong> Chewi's book controls the source-facing theorem; Chewi's official supplement is additional source material. Other textbooks are used to recover standard omitted prerequisites or rigorous details and never silently alter the pinned theorem.</p>
  <div class="source-stack-grid">
    <article class="source-stack-card primary"><span class="source-stack-role">Primary source</span><h3>{escape(str(primary['title']))}</h3><p>{escape(str(primary['role']))}</p><a class="lineage-source-link" href="{escape(str(primary['url']))}">Open textbook ↗</a></article>
    <article class="source-stack-card primary"><span class="source-stack-role">Official supplement</span><h3>{escape(str(supplement['title']))}</h3><p>{escape(str(supplement['role']))}</p><a class="lineage-source-link" href="{escape(str(supplement['url']))}">Open supp.pdf ↗</a></article>
    {''.join(group_cards)}
  </div>
</section>
"""


def supplement_html(data: dict[str, Any]) -> str:
    supp = dict(data["chewi_log_concave_sampling"]["official_supplement"])
    cards = []
    for raw in supp.get("sections", []):
        if not isinstance(raw, dict):
            continue
        pages = str(raw.get("pages", ""))
        first_page = pages.split("-", 1)[0]
        url = f"{supp['url']}#page={first_page}" if first_page else str(supp["url"])
        items = [str(item) for item in raw.get("items", [])]
        cards.append(
            f"""
<article class="supplement-card official" data-official-supplement-section="{escape(str(raw.get('id', '')))}">
  <span class="supplement-source-id">{escape(str(raw.get('id', '')))} · supp. §{escape(str(raw.get('source_section', '')))} · pp. {escape(pages)}</span>
  <h3>{escape(str(raw.get('title', '')))}</h3>
  <p>{escape(str(raw.get('summary', '')))}</p>
  <ul>{''.join(f'<li>{escape(item)}</li>' for item in items)}</ul>
  <a class="supplement-page-link" href="{escape(url)}">Open exact source pages ↗</a>
</article>"""
        )
    return f"""
<section class="official-supplement" id="official-supplement" data-chewi-official-supplement="chapter-2">
  <div class="supplement-header"><div class="section-heading"><span>Official source supplement</span><h2>Supplement to Chapter 2</h2></div><a class="button" href="{escape(str(supp['url']))}">Open Chewi's supp.pdf ↗</a></div>
  <p class="source-hierarchy-note">The supplement says that this material was omitted from <em>Log-Concave Sampling</em> for space. Samplinglib therefore maps <strong>all sections of supp.pdf</strong> into the Chapter 2 source trail. The cards below summarize and anchor the source rather than republishing the 20-page document wholesale.</p>
  <div class="supplement-grid">{''.join(cards)}</div>
</section>
"""


def patch_chapter2_sections(output: Path, supp_url: str) -> None:
    chapter_dir = output / "textbook" / "chapter-02"
    if not chapter_dir.exists():
        return
    for path in sorted(chapter_dir.glob("*.html")):
        rel = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        if 'data-chapter-official-supplement="2"' in text:
            continue
        text = add_style(text, rel)
        banner = f"""
<section class="source-hierarchy-note" data-chapter-official-supplement="2">
<strong>Official Chapter 2 supplement.</strong> Chewi's <a href="{escape(supp_url)}">supp.pdf</a> contains the omitted tensorization, concentration, Gozlan, metric-measure-space, synthetic-Ricci-curvature, and exercise material. <a href="../chapter-02.html#official-supplement">See the complete structured supplement map →</a>
</section>
"""
        end = text.rfind("</main>")
        if end < 0:
            raise RuntimeError(f"{rel}: missing main while adding official supplement")
        text = text[:end] + banner + text[end:]
        path.write_text(text, encoding="utf-8", newline="\n")


def attribution_html(data: dict[str, Any]) -> str:
    chewi = dict(data["chewi_log_concave_sampling"])
    optimisation = dict(data["optimisation"])
    background_groups = [dict(item) for item in chewi.get("background_reference_groups", []) if isinstance(item, dict)]
    opt_background = [dict(item) for item in optimisation.get("background_references", []) if isinstance(item, dict)]
    cards = [
        f"""<article class="source-lineage-card"><span class="lineage-role">Sampling · primary source</span><h3>Sinho Chewi · Log-Concave Sampling</h3><p>The source-facing theorem order and statement authority for the sampling textbook route.</p><a class="lineage-source-link" href="{escape(str(chewi['primary']['url']))}">main.pdf ↗</a></article>""",
        f"""<article class="source-lineage-card"><span class="lineage-role">Sampling · official supplement</span><h3>Sinho Chewi · Supplement to Log-Concave Sampling</h3><p>Official Chapter 2 material omitted from the book for space; treated as source, not ASTIS-added mathematics.</p><a class="lineage-source-link" href="{escape(str(chewi['official_supplement']['url']))}">supp.pdf ↗</a></article>""",
        f"""<article class="source-lineage-card"><span class="lineage-role">Optimisation · primary source</span><h3>Sinho Chewi · Lectures on Optimization</h3><p>The public theorem-proof source and chapter spine for the Optimisation Library.</p><a class="lineage-source-link" href="{escape(str(optimisation['primary']['url']))}">arXiv:2605.07006 ↗</a></article>""",
    ]
    for group in background_groups:
        refs = [dict(item) for item in group.get("references", []) if isinstance(item, dict)]
        cards.append(
            f"""<article class="source-lineage-card wide"><span class="lineage-role">Sampling · background / rigor references</span><h3>{escape(str(group.get('title', 'Background references')))}</h3><p>{escape(str(group.get('role', '')))}</p><ul>{''.join(f'<li>{linked_name(ref)}</li>' for ref in refs)}</ul></article>"""
        )
    cards.append(
        f"""<article class="source-lineage-card wide"><span class="lineage-role">Optimisation · background lineage</span><h3>Bubeck · Beck · Nesterov</h3><p>Chewi explicitly states that the 2026 lecture notes are primarily based on these sources. They are attributed background and theorem cross-checks; the public formalization follows Chewi's arXiv notes.</p><ul>{''.join(f'<li>{linked_name(ref)} — {escape(str(ref.get("role", "")))}</li>' for ref in opt_background)}</ul></article>"""
    )
    return f"""
<section class="source-lineage-attribution" data-source-lineage-attribution="true">
  <div class="section-heading"><span>Mathematical source lineage</span><h2>Primary source ≠ supplement ≠ background reference.</h2></div>
  <p class="source-hierarchy-note">A primary source controls source-facing statements. An official same-author supplement is additional source material. Background books are used to fill standard omitted details or cross-check conventions. Formal upstreams are reused only after compatibility is checked.</p>
  <div class="source-lineage-grid">{''.join(cards)}</div>
</section>
"""


def optimisation_progress_body() -> str:
    return """
<section class="page-hero compact progress-hero" data-current-progress="optimisation">
  <div class="eyebrow">Current Progress · Optimisation Route</div><h1>Optimisation</h1>
  <p class="lede">The route formalises Sinho Chewi's public <em>Lectures on Optimization</em> (arXiv:2605.07006) section by section. Mathlib, Optlib and CvxLean are searched first; Bubeck, Beck and Nesterov remain attributed background references.</p>
  <p><a href="index.html">← All routes</a> · <a href="../libraries/optimisation/index.html">Open Optimisation library</a></p>
</section>
<section><div class="section-heading"><span>Route milestones</span><h2>Public source first, shared Lean where mathematics really overlaps.</h2></div>
<div class="progress-milestones">
  <article><div class="progress-milestone-head"><span>scaffold</span><b>01</b></div><h3>13 chapters + Appendix A</h3><p>Stable source-facing pages follow Chewi's arXiv table of contents rather than a proprietary book table of contents.</p></article>
  <article><div class="progress-milestone-head"><span>planned</span><b>02</b></div><h3>Convexity, flow, gradient descent and acceleration</h3><p>Formalise §§1-5 while reusing compatible Mathlib/Optlib convex-analysis interfaces.</p></article>
  <article><div class="progress-milestone-head"><span>planned</span><b>03</b></div><h3>Non-smooth, Frank-Wolfe, proximal and duality</h3><p>Formalise §§6-9 and record exact shared nodes with sampling when the theorem statements genuinely coincide.</p></article>
  <article><div class="progress-milestone-head"><span>planned</span><b>04</b></div><h3>Mirror, alternating, stochastic and interior-point methods</h3><p>Formalise §§10-13 and expose candidate shared-floor checkpoints with structured/log-concave sampling.</p></article>
</div></section>
<section class="progress-shared-policy"><h2>Intersection contract</h2><p>Log-Concave Sampling and Optimisation share one lower-level declaration only when objects, quantifiers, assumptions and conclusions match. Near-equivalent formulations use a canonical core plus a small explicit adapter.</p></section>
<section class="progress-workflow" data-progress-verification-workflow="true"><div class="section-heading"><span>Verification Workflow</span><h2>The same ASTIS gate applies.</h2></div><div class="progress-flow"><span>source audit</span><b>→</b><span>search & reuse</span><b>→</b><span>Frontier Cell if missing</span><b>→</b><span>focused test</span><b>→</b><span>independent review</span><b>→</b><span>stabilize & merge</span></div><p><a class="button" href="../workflow/index.html">Open ASTIS Harness</a></p></section>
"""


def write_optimisation_progress(output: Path) -> None:
    text = astis_site.page(
        "Optimisation · Current Progress",
        OPT_PROGRESS,
        optimisation_progress_body(),
        active="Progress",
        description="Current formalization route for Sinho Chewi's Lectures on Optimization.",
    )
    text = canonical_shell(text, OPT_PROGRESS, output)
    astis_site.write_page(output, OPT_PROGRESS, text)

    old = output / OLD_OPT_PROGRESS
    if old.exists():
        redirect = astis_site.page(
            "Optimisation · Current Progress",
            OLD_OPT_PROGRESS,
            '<section class="page-hero compact"><div class="eyebrow">Samplinglib · moved</div><h1>Optimisation</h1><p>This route now formalises Sinho Chewi\'s public lecture notes.</p><a class="button primary" href="optimisation.html">Open Optimisation</a></section>',
            active="Progress",
        )
        redirect = redirect.replace("</head>", '  <meta http-equiv="refresh" content="0; url=optimisation.html">\n</head>', 1)
        redirect = canonical_shell(redirect, OLD_OPT_PROGRESS, output)
        astis_site.write_page(output, OLD_OPT_PROGRESS, redirect)


def patch_public_names(output: Path) -> None:
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output).as_posix()
        if rel == OLD_OPT_PROGRESS or rel.startswith("libraries/first-order-optimization/"):
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("progress/first-order-optimization.html", "progress/optimisation.html")
        text = text.replace("first-order-optimization.html", "optimisation.html")
        text = text.replace("First-Order Optimization", "Optimisation")
        text = text.replace("Beck/Optlib/CvxLean", "Chewi/Optlib/CvxLean")
        path.write_text(text, encoding="utf-8", newline="\n")


def validate(output: Path, data: dict[str, Any]) -> None:
    errors: list[str] = []
    required = {
        TEXTBOOK_INDEX: ('data-chewi-source-stack="true"', "supp.pdf", "Karatzas-Shreve", "Villani"),
        CHEWI_CHAPTER_2: ('data-chewi-official-supplement="chapter-2"', "S2.1", "S2.6", "Metric measure spaces", "Exercises"),
        ATTRIBUTION: ('data-source-lineage-attribution="true"', "Bubeck", "Amir Beck", "Nesterov", "Protter", "Revuz-Yor"),
        "libraries/optimisation/index.html": ("Lectures on Optimization", "arXiv:2605.07006"),
        OPT_PROGRESS: ("Current Progress · Optimisation Route", "arXiv:2605.07006", 'data-ia-version="2"'),
    }
    for rel, markers in required.items():
        path = output / rel
        if not path.exists():
            errors.append(f"missing {rel}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing source-lineage marker {marker!r}")

    supp = dict(data["chewi_log_concave_sampling"]["official_supplement"])
    chapter2 = (output / CHEWI_CHAPTER_2).read_text(encoding="utf-8") if (output / CHEWI_CHAPTER_2).exists() else ""
    for raw in supp.get("sections", []):
        if isinstance(raw, dict) and str(raw.get("id", "")) not in chapter2:
            errors.append(f"Chapter 2 supplement map missing {raw.get('id')}")

    canonical_styles = set(library_shelves.canonical_theme_styles(output))
    for rel in ("libraries/riemannian-optimization/index.html", "libraries/optimisation/index.html", OPT_PROGRESS):
        path = output / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        styles = set(library_shelves.stylesheet_names(text))
        missing = canonical_styles - styles
        if missing:
            errors.append(f"{rel}: theme differs from Log-Concave Sampling; missing {sorted(missing)}")
        if "index.html#samplinglib" in text:
            errors.append(f"{rel}: obsolete pre-IA Samplinglib anchor remains")

    for path in output.rglob("*.html"):
        rel = path.relative_to(output).as_posix()
        if rel == OLD_OPT_PROGRESS or rel.startswith("libraries/first-order-optimization/"):
            continue
        text = path.read_text(encoding="utf-8")
        if "First-Order Optimization" in text:
            errors.append(f"{rel}: obsolete public library name leaked")
            break

    if errors:
        raise RuntimeError("source lineage validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    data = load_data()
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_CSS, assets / STYLE_NAME)

    append_main(output, TEXTBOOK_INDEX, source_stack_html(data), 'data-chewi-source-stack="true"')
    append_main(output, CHEWI_CHAPTER_2, supplement_html(data), 'data-chewi-official-supplement="chapter-2"')
    patch_chapter2_sections(output, str(data["chewi_log_concave_sampling"]["official_supplement"]["url"]))
    append_main(output, ATTRIBUTION, attribution_html(data), 'data-source-lineage-attribution="true"')
    write_optimisation_progress(output)
    patch_public_names(output)

    for rel in ("libraries/riemannian-optimization/index.html", "libraries/optimisation/index.html"):
        path = output / rel
        if path.exists():
            text = canonical_shell(path.read_text(encoding="utf-8"), rel, output)
            path.write_text(text, encoding="utf-8", newline="\n")

    validate(output, data)


if __name__ == "__main__":
    enrich_site()
