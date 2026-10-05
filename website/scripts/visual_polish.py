#!/usr/bin/env python3
"""Apply the final Samplinglib visual system after all content enrichers.

The information architecture remains ASTIS-specific.  This layer only owns
reader-facing typography, visual rhythm, and the canonical Samplinglib home
masthead.  Its design tokens intentionally follow the restrained academic
language used by the QuantumComputinglib public site.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_CSS = ROOT / "website" / "static" / "quantumcomputinglib-polish.css"
DETAIL_CSS = ROOT / "website" / "static" / "quantumcomputinglib-detail-polish.css"
STYLE_NAMES = ("quantumcomputinglib-polish.css", "quantumcomputinglib-detail-polish.css")
HOME = Path("index.html")
LIBRARY_SUBTITLE = "Verified Sampling, Optimisation, Geometry Theory in Lean"
HOME_LEDE = (
    "A readable formal library for sampling, optimisation, and geometry: "
    "Chewi's sampling and optimisation texts, Boumal's Riemannian optimisation route, "
    "statistical optimal transport, a live SampleWiki frontier, and the shared Lean proof graph beneath them."
)
OLD_REPO = "https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep"
NEW_REPO = "https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib"


def prefix_for(path: Path) -> str:
    return "../" * len(path.parent.parts)


def canonical_home_masthead() -> str:
    return (
        f'<div class="eyebrow">{LIBRARY_SUBTITLE}</div>\n'
        '  <h1>Samplinglib</h1>\n'
        f'  <p class="lede">{HOME_LEDE}</p>'
    )


def rewrite_scope(text: str) -> str:
    """Normalize public scope strings that originate in the base site template."""
    text = text.replace("Verified Sampling Theory in Lean", LIBRARY_SUBTITLE)
    text = text.replace("Verified sampling theory in Lean", LIBRARY_SUBTITLE)
    text = text.replace(
        "Samplinglib: verified sampling theory in Lean",
        "Samplinglib: verified sampling, optimisation, and geometry theory in Lean",
    )
    text = text.replace(
        f'<a href="{OLD_REPO}">GitHub',
        f'<a href="{NEW_REPO}">GitHub',
    )
    return text


def rewrite_home(text: str) -> str:
    canonical = canonical_home_masthead()
    if canonical in text:
        return text

    text = re.sub(
        r'<div class="eyebrow">Samplinglib · formal sampling theory</div>\s*'
        r'<h1>Sampling theory, readable and verified\.</h1>\s*'
        r'<p class="lede">.*?</p>',
        canonical,
        text,
        count=1,
        flags=re.S,
    )
    text = re.sub(
        r'<div class="eyebrow">Verified sampling theory in Lean</div>\s*'
        r'<h1>Samplinglib</h1>\s*'
        r'<p class="lede">A readable formal library for sampling theory:.*?</p>',
        canonical,
        text,
        count=1,
        flags=re.S,
    )
    return text


def inject_styles(text: str, rel_path: Path) -> str:
    marker = "</head>"
    if marker not in text:
        raise RuntimeError(f"cannot inject visual stylesheets into {rel_path.as_posix()}")
    links: list[str] = []
    for name in STYLE_NAMES:
        href = f"{prefix_for(rel_path)}assets/{name}"
        if href not in text:
            links.append(f'  <link rel="stylesheet" href="{href}">')
    if not links:
        return text
    return text.replace(marker, "\n".join(links) + "\n" + marker, 1)


def validate(output: Path) -> None:
    home = (output / HOME).read_text(encoding="utf-8")
    errors: list[str] = []
    if "<h1>Samplinglib</h1>" not in home:
        errors.append("home masthead is not Samplinglib")
    for obsolete in (
        "Sampling theory, readable and verified.",
        "Verified sampling theory in Lean",
        "Verified Sampling Theory in Lean",
        "A readable formal library for sampling theory:",
    ):
        if obsolete in home:
            errors.append(f"obsolete sampling-only branding remains: {obsolete}")
    if LIBRARY_SUBTITLE not in home:
        errors.append("widened Samplinglib purpose kicker is missing")
    if HOME_LEDE not in home:
        errors.append("widened Samplinglib home description is missing")

    primary_css = output / "assets" / STYLE_NAMES[0]
    detail_css = output / "assets" / STYLE_NAMES[1]
    if not primary_css.exists():
        errors.append(f"missing generated stylesheet: assets/{STYLE_NAMES[0]}")
    else:
        css = primary_css.read_text(encoding="utf-8")
        for marker in (
            'Charter, "Bitstream Charter"',
            "--academic-page-width: 1260px",
            ".ia-home-hero h1",
            ".source-portal",
            ".site-sidebar",
        ):
            if marker not in css:
                errors.append(f"visual stylesheet missing contract: {marker}")
    if not detail_css.exists():
        errors.append(f"missing generated stylesheet: assets/{STYLE_NAMES[1]}")
    elif ".atlas-layer" not in detail_css.read_text(encoding="utf-8"):
        errors.append("detail polish does not cover Proof Atlas")

    for path in output.rglob("*.html"):
        rel = path.relative_to(output)
        text = path.read_text(encoding="utf-8")
        for name in STYLE_NAMES:
            expected = f"{prefix_for(rel)}assets/{name}"
            if expected not in text:
                errors.append(f"{rel.as_posix()}: final visual stylesheet missing: {name}")

    if errors:
        raise RuntimeError("visual polish validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path) -> None:
    asset_dir = output / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_CSS, asset_dir / STYLE_NAMES[0])
    shutil.copyfile(DETAIL_CSS, asset_dir / STYLE_NAMES[1])

    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output)
        text = path.read_text(encoding="utf-8")
        text = rewrite_scope(text)
        if rel == HOME:
            text = rewrite_home(text)
        text = inject_styles(text, rel)
        path.write_text(text, encoding="utf-8", newline="\n")

    validate(output)
