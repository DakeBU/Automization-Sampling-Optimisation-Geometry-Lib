#!/usr/bin/env python3
"""Final source-first presentation contract for the ASTIS textbook reader.

Reader-facing source cards must have one stable order:

1. Chewi statement (displayed mathematics first);
2. Chewi proof / derivation, or an explicit source-proof-status note;
3. assumptions and prerequisites that the source leaves implicit;
4. ASTIS rigorous LaTeX restatement / expansion, collapsed by default;
5. exact Lean formalization, collapsed by default.

Internal audit prose such as ``mathematical_exposition`` and
``astis_exposition`` is metadata, not reader copy.  This layer therefore
rebuilds source cards from audited fields instead of leaking those strings into
the public page.  It also rewrites ASTIS implicit-prerequisite cards so legacy
ASCII mathematics never appears as ordinary prose.

This is presentation-only.  It never changes source correspondence, Registry,
completion status, or Lean evidence.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

import math_first_reader as base
import reader_contract_final as reader


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
SOURCE_CORRESPONDENCE = ROOT / "website" / "content" / "source_correspondence.json"
FORMULA_SUPPLEMENTS = ROOT / "website" / "content" / "chapter1_formula_supplements.json"
PROOF_SUPPLEMENTS = ROOT / "website" / "content" / "chapter1_proof_supplements.json"
IMPLICIT_PREREQUISITES = ROOT / "website" / "content" / "implicit_prerequisites.json"
SOURCE_CSS = ROOT / "website" / "static" / "chewi-source-first-contract.css"
STYLE_NAME = "chewi-source-first-contract.css"


IMPLICIT_PROOF_OVERRIDES: dict[str, str] = {
    "implicit-1-1-tonelli-product-energy": (
        "Apply Tonelli's theorem to the nonnegative measurable integrand. "
        "Nonnegativity removes the need for a prior integrability hypothesis, and the displayed identity is the resulting iterated-integral equality."
    ),
    "implicit-1-1-null-time-endpoints": (
        "Lebesgue measure is atomless, so changing a measurable representative at finitely many time points preserves its almost-everywhere class. "
        "The Lebesgue integral, the relevant Lp class, and the completed Itô integral therefore do not depend on those endpoint choices."
    ),
    "implicit-1-1-stopped-process-measurability": (
        "On every finite horizon, progressiveness makes the threshold event measurable in the corresponding time-filtration product sigma-algebra. "
        "Multiplication by its indicator, equivalently a measurable piecewise definition with zero, preserves progressive measurability."
    ),
    "implicit-1-1-hitting-time-stopping": (
        "Continuity and monotonicity identify the first-passage event by a fixed-time level event. "
        "Adaptedness makes that fixed-time event measurable in the filtration, which is exactly the stopping-time requirement."
    ),
    "implicit-1-1-l2-completion-ito": (
        "The elementary Itô isometry sends every Cauchy approximating sequence to a Cauchy sequence in the terminal L2 space. "
        "Completeness gives a limit, the isometry makes it independent of the approximation, and linearity passes through the limit."
    ),
    "implicit-1-1-doob-l2": (
        "Apply Doob's maximal inequality with exponent two to the absolute value of the martingale. "
        "The standard exponent-two constant is four, giving the displayed bound for the whole path from the terminal second moment."
    ),
    "implicit-1-1-borel-cantelli-continuous-version": (
        "Summability of the maximal-deviation events implies by the first Borel-Cantelli lemma that only finitely many occur almost surely. "
        "The remaining tail is uniformly Cauchy, and the uniform limit of continuous paths is continuous."
    ),
    "implicit-1-1-stopped-energy-bound": (
        "Before the first hit, accumulated energy stays below the threshold; at the hit, continuity prevents overshoot. "
        "The resulting pathwise bound becomes a global L2 bound after integration under the probability measure."
    ),
    "implicit-1-1-stopped-ito-consistency": (
        "Stop the larger localized integrand once more at the smaller localizer. "
        "The two stopped integrands agree in product-space L2, and the Itô isometry transfers that equality to the corresponding stochastic integrals."
    ),
}


RAW_MATH_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\s(?:<=|>=|->)\s"), "ASCII relation/operator"),
    (re.compile(r"\b(?:F|M|A|B|X|I|H|V|eta|tau|sigma|mu|pi)_[A-Za-z0-9]"), "raw subscript notation"),
    (re.compile(r"\bf\s*\(\s*omega\s*,\s*t\s*\)"), "raw function-of-omega notation"),
    (re.compile(r"\|\s*eta_"), "raw absolute-value stochastic notation"),
    # Reject an ASCII infix formula, not the legitimate English noun "tensor".
    (re.compile(r"\b(?:[A-Za-z](?:_[A-Za-z0-9]+)?|gamma|mu|nu|pi)\s+tensor\s+"
                r"(?:[A-Za-z](?:_[A-Za-z0-9]+)?|gamma|mu|nu|pi)\b"),
     "raw tensor-product notation"),
    (re.compile(r"\bE\s*\[.*?\|.*?\]"), "raw conditional expectation"),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _load_list(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise RuntimeError(f"{path.relative_to(ROOT)} must contain a JSON list")
    return [dict(item) for item in raw if isinstance(item, dict)]


def _by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {str(item.get("id", "")): item for item in _load_list(path) if item.get("id")}


def _formula_for(
    source_id: str,
    source: dict[str, Any],
    supplements: dict[str, dict[str, Any]],
) -> str:
    latex = str(source.get("latex_statement", "")).strip()
    if latex:
        return latex
    supplement = supplements.get(source_id, {})
    latex = str(supplement.get("formula", "")).strip()
    if latex:
        return latex
    raise RuntimeError(f"{source_id}: no audited LaTeX statement is available")


def _display_math(latex: str, extra_class: str = "") -> str:
    classes = "formula source-formula source-contract-formula"
    if extra_class:
        classes += " " + extra_class
    return f'<div class="{classes}">\\[{esc(latex)}\\]</div>'


def _plain_list(values: list[str], css_class: str = "") -> str:
    cls = f' class="{css_class}"' if css_class else ""
    return "<ul" + cls + ">" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def _code_list(values: list[str], css_class: str = "") -> str:
    cls = f' class="{css_class}"' if css_class else ""
    return "<ul" + cls + ">" + "".join(f"<li><code>{esc(value)}</code></li>" for value in values) + "</ul>"


def _render_equations(proof: dict[str, Any] | None, css_class: str) -> str:
    if not proof:
        return ""
    rows: list[str] = []
    for index, raw in enumerate(proof.get("steps", []), 1):
        if not isinstance(raw, dict):
            continue
        formula = str(raw.get("formula", "")).strip()
        if not formula:
            continue
        rows.append(
            '<div class="source-contract-proof-step">'
            f'<div class="source-contract-proof-index">{index}</div>'
            f'<div class="formula {css_class}">\\[{esc(formula)}\\]</div>'
            '</div>'
        )
    return "".join(rows)


def _render_chewi_proof(source: dict[str, Any], proof: dict[str, Any] | None) -> str:
    if proof and str(proof.get("source_status", "")) == "source_proof":
        equations = _render_equations(proof, "chewi-source-proof-formula")
        return (
            '<div class="source-contract-chewi-proof">'
            '<h3>Chewi proof / derivation</h3>'
            '<p class="source-contract-provenance">Source-faithful equation route; notation is normalized but the argument is not replaced by an ASTIS proof.</p>'
            f'{equations}</div>'
        )

    kind = str(source.get("source_kind", ""))
    theorem_like = any(
        token in kind
        for token in ("Theorem", "Proposition", "Lemma", "Corollary", "Example")
    )
    if not theorem_like:
        return ""
    if proof and str(proof.get("source_status", "")) == "astis_expansion":
        note = (
            "Chewi does not provide the expanded proof represented by this packet at this point in the source. "
            "The strict expansion is therefore labeled ASTIS and kept in the folded formalization below."
        )
    else:
        note = (
            "No source-proof supplement is currently audited for this result. "
            "ASTIS does not present a reconstructed argument as if it were Chewi's proof."
        )
    return (
        '<div class="source-contract-chewi-proof source-contract-proof-status">'
        '<h3>Chewi proof status</h3>'
        f'<p>{esc(note)}</p></div>'
    )


def _render_hidden_assumptions(source: dict[str, Any]) -> str:
    source_assumptions = [str(x) for x in source.get("source_assumptions", []) if str(x).strip()]
    formal_assumptions = [str(x) for x in source.get("formal_assumptions", []) if str(x).strip()]
    rigorous = str(source.get("rigorous_packet", "")).strip()
    parts = [
        '<div class="source-contract-hidden-assumptions">',
        '<h3>Assumptions and implicit prerequisites</h3>',
    ]
    if source_assumptions:
        parts.append('<h4>Source-level assumptions</h4>' + _plain_list(source_assumptions))
    if rigorous:
        parts.append('<h4>What the surrounding textbook context leaves implicit</h4>' + f'<p>{esc(rigorous)}</p>')
    if formal_assumptions:
        parts.append('<h4>ASTIS-explicit formal conditions</h4>' + _code_list(formal_assumptions))
    parts.append('</div>')
    return "".join(parts)


def _render_astis_latex(
    source_id: str,
    source: dict[str, Any],
    statement: str,
    proof: dict[str, Any] | None,
) -> str:
    equations = _render_equations(proof, "astis-rigorous-proof-formula")
    rigorous = str(source.get("rigorous_packet", "")).strip()
    source_status = str(proof.get("source_status", "")) if proof else ""
    if source_status == "astis_expansion":
        proof_note = "The equations below are the ASTIS expansion of a proof omitted or compressed in the source."
    elif equations:
        proof_note = "The source argument is restated here as a strict ASTIS LaTeX packet before the Lean correspondence."
    else:
        proof_note = "This packet records the strict ASTIS statement and formal side conditions; no extra proof is invented."
    return (
        '<details class="reader-disclosure source-contract-astis-latex">'
        '<summary>ASTIS rigorous LaTeX formalization</summary>'
        '<div class="disclosure-body">'
        f'<p>{esc(proof_note)}</p>'
        f'{_display_math(statement, "astis-rigorous-statement")}'
        + (f'<p>{esc(rigorous)}</p>' if rigorous else "")
        + equations
        + '</div></details>'
    )


def _declaration_url_map(output: Path) -> dict[str, str]:
    path = output / "search-index.json"
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    resolved: dict[str, str] = {}
    if isinstance(raw, list):
        for row in raw:
            if not isinstance(row, dict):
                continue
            name = str(row.get("name", "")).strip()
            url = str(row.get("url", "")).strip()
            if name and url:
                resolved[name] = url
    return resolved


def _render_lean(source: dict[str, Any], url_map: dict[str, str]) -> str:
    declarations = [str(x) for x in source.get("lean_declarations", []) if str(x).strip()]
    leaves: list[str] = []
    for leaf in source.get("proof_leaves", []):
        if not isinstance(leaf, dict):
            continue
        for name in leaf.get("declarations", []):
            value = str(name).strip()
            if value and value not in leaves:
                leaves.append(value)
    links: list[str] = []
    for name in declarations:
        url = url_map.get(name)
        if url:
            links.append(f'<li><a href="../../{esc(url)}"><code>{esc(name)}</code></a></li>')
        else:
            links.append(f'<li><code>{esc(name)}</code></li>')
    leaf_html = _code_list(leaves, "source-contract-lean-leaves") if leaves else ""
    return (
        '<details class="reader-disclosure source-contract-lean">'
        '<summary>Lean formalization</summary>'
        '<div class="disclosure-body">'
        + ('<h4>Final declaration</h4><ul>' + ''.join(links) + '</ul>' if links else '<p>No compiled Lean declaration is claimed on this source card.</p>')
        + ('<h4>Underlying proof leaves</h4>' + leaf_html if leaf_html else '')
        + '</div></details>'
    )


def _render_source_card(
    source_id: str,
    source: dict[str, Any],
    supplements: dict[str, dict[str, Any]],
    proofs: dict[str, dict[str, Any]],
    url_map: dict[str, str],
) -> str:
    statement = _formula_for(source_id, source, supplements)
    proof = proofs.get(source_id)
    kind = str(source.get("source_kind", ""))
    summary = str(source.get("source_summary", ""))
    page = str(source.get("page", "")).strip()
    source_url = str(source.get("source_url", "")).strip()
    wording = str(source.get("wording_status", "")).strip()
    meta = " · ".join(value for value in (page, wording) if value)
    return (
        '<section class="source-passage source-contract-card" '
        f'data-source-id="{esc(source_id)}">'
        '<header class="source-contract-header">'
        f'<div class="source-result-kind">{esc(kind)}</div>'
        + (f'<div class="source-contract-meta">{esc(meta)}</div>' if meta else '')
        + '</header>'
        '<div class="source-contract-chewi-statement">'
        '<h3>Chewi statement</h3>'
        f'{_display_math(statement, "chewi-source-statement")}'
        + (f'<p class="source-result-summary">{esc(summary)}</p>' if summary else '')
        + '</div>'
        + _render_chewi_proof(source, proof)
        + _render_hidden_assumptions(source)
        + _render_astis_latex(source_id, source, statement, proof)
        + _render_lean(source, url_map)
        + (f'<a class="source-anchor source-contract-link" href="{esc(source_url)}">Chewi source ↗</a>' if source_url else '')
        + '</section>'
    )


def _replace_source_cards(output: Path) -> None:
    sources = _by_id(SOURCE_CORRESPONDENCE)
    supplements = _by_id(FORMULA_SUPPLEMENTS)
    proofs = _by_id(PROOF_SUPPLEMENTS)
    url_map = _declaration_url_map(output)
    grouped: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for source_id, source in sources.items():
        section = str(source.get("section", ""))
        grouped.setdefault(section, []).append((source_id, source))

    errors: list[str] = []
    for section, entries in grouped.items():
        try:
            path = base.section_path(output, section)
        except Exception:
            continue
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for source_id, source in entries:
            pattern = re.compile(
                rf'<section class="[^"]*\bsource-passage\b[^"]*"[^>]*data-source-id="{re.escape(esc(source_id))}"[^>]*>.*?</section>',
                flags=re.S,
            )
            matches = list(pattern.finditer(text))
            if len(matches) != 1:
                errors.append(f"{path.relative_to(output)}: expected one source card {source_id}; found {len(matches)}")
                continue
            match = matches[0]
            replacement = _render_source_card(source_id, source, supplements, proofs, url_map)
            text = text[:match.start()] + replacement + text[match.end():]
        path.write_text(text, encoding="utf-8", newline="\n")
    if errors:
        raise RuntimeError("Chewi source-card reconstruction failed:\n- " + "\n- ".join(errors))


def _render_implicit_card(item: dict[str, Any], url_map: dict[str, str]) -> str:
    item_id = str(item.get("id", ""))
    proof = IMPLICIT_PROOF_OVERRIDES.get(item_id)
    raw_proof = str(item.get("proof", ""))
    if proof is None:
        if _raw_math_errors(raw_proof):
            raise RuntimeError(
                f"{item_id}: implicit-prerequisite proof contains raw mathematics and has no clean proof override"
            )
        proof = raw_proof
    assumptions = [str(x) for x in item.get("assumptions", []) if str(x).strip()]
    declarations = [str(x) for x in item.get("lean_declarations", []) if str(x).strip()]
    lean_rows: list[str] = []
    for name in declarations:
        url = url_map.get(name)
        if url:
            lean_rows.append(f'<li><a href="../../{esc(url)}"><code>{esc(name)}</code></a></li>')
        else:
            lean_rows.append(f'<li><code>{esc(name)}</code></li>')
    return (
        '<article class="textbook-block implicit-prerequisite-card source-contract-implicit" '
        f'id="{esc(item_id)}" data-provenance="astis-implicit-prerequisite">'
        '<div class="passage-label">ASTIS implicit prerequisite · not a standalone Chewi result</div>'
        f'<h2>{esc(item.get("title", ""))}</h2>'
        f'<p><strong>Why it is needed.</strong> {esc(item.get("why_needed", ""))}</p>'
        f'{_display_math(str(item.get("latex_statement", "")), "implicit-prerequisite-statement")}'
        '<h3>Assumptions</h3>'
        f'{_plain_list(assumptions)}'
        '<details class="reader-disclosure source-contract-implicit-proof">'
        '<summary>Mathematical proof</summary><div class="disclosure-body">'
        f'<p>{esc(proof)}</p></div></details>'
        '<details class="reader-disclosure source-contract-lean">'
        '<summary>Lean formalization</summary><div class="disclosure-body"><ul>'
        + ''.join(lean_rows)
        + '</ul></div></details>'
        '</article>'
    )


def _replace_implicit_cards(output: Path) -> None:
    items = _load_list(IMPLICIT_PREREQUISITES)
    url_map = _declaration_url_map(output)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(str(item.get("section", "")), []).append(item)
    errors: list[str] = []
    for section, section_items in grouped.items():
        path = base.section_path(output, section)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for item in section_items:
            item_id = str(item.get("id", ""))
            pattern = re.compile(
                rf'<article class="[^"]*\bimplicit-prerequisite-card\b[^"]*"[^>]*id="{re.escape(esc(item_id))}"[^>]*>.*?</article>',
                flags=re.S,
            )
            matches = list(pattern.finditer(text))
            if len(matches) != 1:
                errors.append(f"{path.relative_to(output)}: expected one implicit prerequisite {item_id}; found {len(matches)}")
                continue
            match = matches[0]
            replacement = _render_implicit_card(item, url_map)
            text = text[:match.start()] + replacement + text[match.end():]
        path.write_text(text, encoding="utf-8", newline="\n")
    if errors:
        raise RuntimeError("implicit-prerequisite reconstruction failed:\n- " + "\n- ".join(errors))


def _inject_style(text: str, rel: Path) -> str:
    prefix = "../" * len(rel.parent.parts)
    href = f"{prefix}assets/{STYLE_NAME}"
    if href in text:
        return text
    return text.replace("</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', 1)


def _non_math_visible_text(text: str) -> str:
    value = re.sub(r'<(?:pre|code|script|style)\b[^>]*>.*?</(?:pre|code|script|style)>', ' ', text, flags=re.S | re.I)
    value = re.sub(r'<[^>]*class="[^"]*\bformula\b[^"]*"[^>]*>.*?</[^>]+>', ' ', value, flags=re.S | re.I)
    value = re.sub(r'\\\(.*?\\\)', ' ', value, flags=re.S)
    value = re.sub(r'\\\[.*?\\\]', ' ', value, flags=re.S)
    value = re.sub(r'<[^>]+>', ' ', value)
    return html.unescape(value)


def _raw_math_errors(value: str) -> list[str]:
    errors: list[str] = []
    for pattern, label in RAW_MATH_PATTERNS:
        if pattern.search(value):
            errors.append(label)
    return errors


def validate(output: Path = DEFAULT_OUTPUT) -> None:
    errors: list[str] = []
    sources = _by_id(SOURCE_CORRESPONDENCE)
    proofs = _by_id(PROOF_SUPPLEMENTS)

    for source_id, source in sources.items():
        section = str(source.get("section", ""))
        try:
            path = base.section_path(output, section)
        except Exception:
            continue
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(
            rf'<section class="[^"]*\bsource-contract-card\b[^"]*"[^>]*data-source-id="{re.escape(esc(source_id))}"[^>]*>.*?</section>',
            flags=re.S,
        )
        match = pattern.search(text)
        if not match:
            errors.append(f"{path.relative_to(output)}: {source_id} is not rendered by the source-first contract")
            continue
        card = match.group(0)
        order = [
            card.find("source-contract-chewi-statement"),
            card.find("source-contract-hidden-assumptions"),
            card.find("source-contract-astis-latex"),
            card.find("source-contract-lean"),
        ]
        proof = proofs.get(source_id)
        if proof and str(proof.get("source_status", "")) == "source_proof":
            proof_at = card.find("source-contract-chewi-proof")
            if proof_at < 0 or not (order[0] < proof_at < order[1]):
                errors.append(f"{path.relative_to(output)}: {source_id} does not place Chewi proof immediately after the statement")
        if any(index < 0 for index in order) or order != sorted(order):
            errors.append(f"{path.relative_to(output)}: {source_id} violates statement/assumptions/ASTIS/Lean order")
        if '<details class="reader-disclosure source-contract-astis-latex" open' in card:
            errors.append(f"{path.relative_to(output)}: {source_id} ASTIS LaTeX disclosure must be folded")
        if '<details class="reader-disclosure source-contract-lean" open' in card:
            errors.append(f"{path.relative_to(output)}: {source_id} Lean disclosure must be folded")

    for path in output.rglob("*.html"):
        visible = _non_math_visible_text(path.read_text(encoding="utf-8"))
        for label in _raw_math_errors(visible):
            snippet = visible[:240].replace("\n", " ")
            errors.append(f"{path.relative_to(output)}: {label} leaked outside MathJax/code; page starts {snippet!r}")

    section_11 = output / "textbook" / "chapter-01" / "section-1-1.html"
    if section_11.exists():
        text = section_11.read_text(encoding="utf-8")
        forbidden = (
            "For s <= t, E[M_t | F_s] = M_s",
            "Mathlib's predicate derives integrability from the fixed-point conditional-expectation law",
            "f(omega,t)=|eta_t(omega)|^2",
        )
        for phrase in forbidden:
            if phrase in text:
                errors.append(f"section-1-1.html: forbidden internal/ASCII exposition leaked: {phrase}")

    if errors:
        raise RuntimeError("Chewi source-first contract failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    _replace_source_cards(output)
    _replace_implicit_cards(output)
    asset_dir = output / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / STYLE_NAME).write_text(SOURCE_CSS.read_text(encoding="utf-8"), encoding="utf-8")
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output)
        text = path.read_text(encoding="utf-8")
        text = _inject_style(text, rel)
        path.write_text(text, encoding="utf-8", newline="\n")
    validate(output)


if __name__ == "__main__":
    enrich_site()
