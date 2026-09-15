#!/usr/bin/env python3
"""Final reader contract for the SampleWiki casebook.

The crawler-level comparison rows remain provenance only.  Reader pages are
rebuilt as mathematical case studies with a strict truth boundary:

1. audited primary-source theorem/corollary -> exact source statement;
2. literature-open row -> open problem, never a synthetic theorem;
3. cited but unaudited row -> normalized SampleWiki statement, explicitly
   pending primary-theorem audit.

Every case page follows the same pedagogical order:
Statement -> Proof / derivation -> Assumptions and implicit prerequisites ->
folded ASTIS rigorous LaTeX -> folded Lean formalization.
"""

from __future__ import annotations

import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from typing import Any

import samplewiki_math_render


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
CASES_PATH = ROOT / "research-wiki" / "source-index" / "SampleWiki_cases.json"
AUDIT_PATH = ROOT / "website" / "content" / "samplewiki_frontier_audit.json"
READER_PATH = ROOT / "website" / "content" / "samplewiki_reader.json"
STYLE_PATH = ROOT / "website" / "static" / "samplewiki-math-reader.css"
STYLE_NAME = "samplewiki-math-reader.css"

OVERVIEW = "example-cases/samplewiki.html"
PROGRESS = "example-cases/samplewiki/progress.html"
FRONTIER = "example-cases/samplewiki/frontier.html"


class FormulaError(ValueError):
    pass


def load_object(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return raw


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower() or "case"


def case_path(case_id: str) -> str:
    return f"example-cases/samplewiki/cases/{slugify(case_id.removeprefix('ASTIS-SW-'))}.html"


def setting_path(setting_slug: str) -> str:
    return f"example-cases/samplewiki/settings/{slugify(setting_slug)}.html"


def href_from(current: str, target: str) -> str:
    start = posixpath.dirname(current) or "."
    return posixpath.relpath(target, start=start)


def source_refs(case: dict[str, Any]) -> list[dict[str, str]]:
    refs: list[dict[str, str]] = []
    for raw in case.get("source_refs", []):
        if isinstance(raw, dict) and str(raw.get("url", "")).strip():
            refs.append(
                {
                    "label": str(raw.get("label") or raw.get("url")),
                    "url": str(raw.get("url")),
                }
            )
    return refs


def literature_open(case: dict[str, Any]) -> bool:
    return str(case.get("result_class", "")).strip().lower() == "lower unknown"


def validate_latex(value: str, *, context: str = "formula") -> str:
    formula = value.strip()
    if not formula:
        raise FormulaError(f"{context}: empty LaTeX")
    bare = {r"\mathcal", r"\widetilde", r"\mathrm", r"\mathbf", r"\sqrt"}
    if formula in bare:
        raise FormulaError(f"{context}: bare TeX command {formula!r}")
    pairs = {"{": "}", "(": ")", "[": "]"}
    closing = {value: key for key, value in pairs.items()}
    stack: list[str] = []
    escaped = False
    for char in formula:
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char in pairs:
            stack.append(char)
        elif char in closing:
            if not stack or stack[-1] != closing[char]:
                raise FormulaError(f"{context}: unbalanced delimiter in {formula!r}")
            stack.pop()
    if stack:
        raise FormulaError(f"{context}: unbalanced delimiter in {formula!r}")
    return formula


def row_formula(case: dict[str, Any], field: str) -> str:
    raw = str(case.get(field, "") or "").strip()
    if not raw or raw.lower() == "unknown":
        return ""
    formula = samplewiki_math_render.math_fragment(raw)
    if not formula:
        return ""
    return validate_latex(formula, context=f"{case.get('id')}:{field}")


def material_qualifiers(case: dict[str, Any]) -> list[str]:
    raw = " ".join(
        str(case.get(field, "") or "") for field in ("guarantee", "complexity")
    )
    prefix, suffix = samplewiki_math_render.qualifier_fragments(raw)
    values: list[str] = []
    if prefix:
        values.append(prefix)
    for item in (part.strip() for part in suffix.split(";") if part.strip()):
        values.append(item)
    return values


def inline_qualifier(value: str) -> str:
    if value == "at ε² = β d":
        return r"at \(\varepsilon^2=\beta d\)"
    if value == "under LSI":
        return "under the source's LSI hypothesis"
    return esc(value)


def formula_html(latex: str, *, css: str = "") -> str:
    if not latex:
        return ""
    checked = validate_latex(latex)
    classes = "formula sw-casebook-formula" + (f" {css}" if css else "")
    return f'<div class="{classes}">\\[{esc(checked)}\\]</div>'


def reference_links(case: dict[str, Any], *, compact: bool = False) -> str:
    refs = source_refs(case)
    if not refs:
        return '<span class="sw-reference-pending">No primary theorem reference is pinned yet.</span>'
    tag = "span" if compact else "li"
    return "".join(
        f'<{tag}><a href="{esc(ref["url"])}">{esc(ref["label"])}</a></{tag}>'
        for ref in refs
    )


def audit_for(case: dict[str, Any], audits: dict[str, Any]) -> dict[str, Any] | None:
    raw = audits.get(str(case.get("id", "")))
    return dict(raw) if isinstance(raw, dict) else None


def statement_status(case: dict[str, Any], audit: dict[str, Any] | None) -> tuple[str, str]:
    if audit is not None:
        return "Exact source theorem", str(audit.get("theorem_label", "Source theorem"))
    if literature_open(case):
        return "Open problem", "Matching lower bound not currently known in the pinned literature trail"
    return (
        "Normalized SampleWiki statement",
        "Primary theorem audit pending — this is not presented as a verbatim paper theorem",
    )


def statement_formulas(case: dict[str, Any], audit: dict[str, Any] | None) -> list[tuple[str, str]]:
    if audit is not None:
        return [("Theorem statement", validate_latex(str(audit.get("statement_latex", "")), context=str(case.get("id"))))]
    values: list[tuple[str, str]] = []
    guarantee = row_formula(case, "guarantee")
    complexity = row_formula(case, "complexity")
    if guarantee:
        values.append(("Guarantee / accuracy", guarantee))
    if complexity and complexity != guarantee:
        values.append(("Complexity / rate", complexity))
    return values


def statement_section(case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    status, label = statement_status(case, audit)
    formulas = statement_formulas(case, audit)
    formula_blocks = "".join(
        f'<div class="sw-statement-line"><span>{esc(kind)}</span>{formula_html(formula, css="sw-main-statement")}</div>'
        for kind, formula in formulas
    )
    if literature_open(case):
        explanation = (
            "SampleWiki records the matching lower-bound question as open. The target regime is shown when the pinned row contains a mathematical target, but ASTIS does not manufacture a theorem or a rate."
        )
    elif audit is not None:
        explanation = (
            "The theorem label and displayed statement below come from the audited primary source. The source link is the controlling reference for all quantifiers and conventions."
        )
    else:
        explanation = (
            "The displayed formulas are a cleaned mathematical normalization of the pinned SampleWiki comparison result. The cited paper is concrete, but the exact theorem/corollary statement has not yet passed ASTIS primary-source audit, so this page does not call the normalization an exact source theorem."
        )
    source_title = str(audit.get("source_title", "")) if audit else ""
    source_version = str(audit.get("source_version", "")) if audit else ""
    source_url = str(audit.get("source_url", "")) if audit else ""
    source_line = ""
    if audit and source_url:
        source_line = (
            '<p class="sw-primary-source">'
            f'<a href="{esc(source_url)}">{esc(source_title or label)}</a>'
            + (f'<span>{esc(source_version)}</span>' if source_version else "")
            + "</p>"
        )
    else:
        source_line = '<div class="sw-inline-references">' + reference_links(case, compact=True) + "</div>"
    return f"""
<section class="sw-casebook-section sw-casebook-statement" data-reader-layer="statement">
  <div class="sw-reader-step">Statement</div>
  <p class="sw-statement-status">{esc(status)}</p>
  <h2>{esc(label)}</h2>
  <p>{esc(explanation)}</p>
  {source_line}
  {formula_blocks or '<p class="sw-open-statement">No finite matching rate is asserted by the pinned source record.</p>'}
</section>
"""


def proof_section(case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    if audit is None:
        if literature_open(case):
            body = (
                "There is no matching source theorem here, so there is no source proof to reproduce. The absence itself is part of the frontier."
            )
            title = "No theorem, hence no synthetic proof"
        else:
            body = (
                "The cited result has not yet passed theorem-level proof audit. ASTIS therefore publishes no reconstructed proof as though it came from the paper. Once audited, this slot is filled with the actual displayed equations and their logical role."
            )
            title = "Primary proof audit pending"
        return f"""
<section class="sw-casebook-section sw-casebook-proof" data-reader-layer="proof">
  <div class="sw-reader-step">Proof / derivation</div><h2>{esc(title)}</h2><p>{esc(body)}</p>
</section>
"""

    status = str(audit.get("source_proof_status", "not audited"))
    equations: list[str] = []
    for index, raw in enumerate(audit.get("proof_equations", []), start=1):
        if not isinstance(raw, dict):
            continue
        latex = validate_latex(str(raw.get("latex", "")), context=f"{case.get('id')}:proof:{index}")
        equations.append(
            '<article class="sw-proof-equation">'
            f'<span class="sw-proof-index">{index:02d}</span>'
            f'<div>{formula_html(latex)}<p>{esc(raw.get("meaning", ""))}</p></div>'
            '</article>'
        )
    if equations:
        body = '<div class="sw-proof-equations">' + "".join(equations) + "</div>"
    elif "omitted" in status.lower():
        body = (
            '<p class="sw-source-omission">The primary source explicitly omits this proof or inherits it from an earlier argument. ASTIS preserves that omission instead of inventing missing source steps.</p>'
        )
    else:
        body = (
            '<p>The source theorem is audited, but no additional equation-level proof transcription is asserted in the current audit packet.</p>'
        )
    return f"""
<section class="sw-casebook-section sw-casebook-proof" data-reader-layer="proof">
  <div class="sw-reader-step">Proof / derivation</div>
  <h2>{esc(status)}</h2>
  {body}
</section>
"""


def assumptions_section(case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    items = [
        f'Sampling setting: <a href="{esc(str(case.get("source_page", "")))}">{esc(case.get("setting_title", ""))}</a>.'
    ]
    for qualifier in material_qualifiers(case):
        items.append(f"Material qualifier preserved from the comparison record: {inline_qualifier(qualifier)}.")
    if audit is not None:
        for prerequisite in audit.get("prerequisites", []):
            items.append(esc(prerequisite))
    elif literature_open(case):
        items.append("The oracle/model class and accuracy notion are inherited from the linked SampleWiki setting; no extra assumptions are added to manufacture a lower bound.")
    else:
        items.append("Exact theorem-level oracle, initialization, regularity, and parameter-range assumptions remain controlled by the linked paper until primary-source theorem audit is complete.")
    return f"""
<section class="sw-casebook-section sw-casebook-assumptions" data-reader-layer="assumptions">
  <div class="sw-reader-step">Assumptions and implicit prerequisites</div>
  <h2>What must be in force</h2>
  <ul>{''.join(f'<li>{item}</li>' for item in items)}</ul>
</section>
"""


def rigorous_details(
    case: dict[str, Any],
    audit: dict[str, Any] | None,
    active_meta: dict[str, Any] | None,
) -> str:
    formulas = statement_formulas(case, audit)
    pieces = [
        f'<div class="sw-rigorous-line"><span>{esc(label)}</span>{formula_html(formula)}</div>'
        for label, formula in formulas
    ]
    if audit is not None:
        for index, raw in enumerate(audit.get("proof_equations", []), start=1):
            if isinstance(raw, dict):
                latex = validate_latex(str(raw.get("latex", "")), context=f"{case.get('id')}:rigorous:{index}")
                pieces.append(
                    f'<div class="sw-rigorous-line"><span>Source proof equation {index}</span>{formula_html(latex)}</div>'
                )
    if active_meta:
        compiled = active_meta.get("compiled_segment", {})
        if isinstance(compiled, dict):
            for label, field in (("Compiled bridge hypothesis", "hypothesis_latex"), ("Compiled bridge conclusion", "conclusion_latex")):
                value = str(compiled.get(field, "")).strip()
                if value:
                    pieces.append(
                        f'<div class="sw-rigorous-line"><span>{esc(label)}</span>{formula_html(validate_latex(value, context=f"active:{field}"))}</div>'
                    )
    if not pieces:
        pieces.append('<p>No audited theorem-level LaTeX is asserted beyond the open-problem description.</p>')
    return f"""
<details class="sw-casebook-disclosure sw-rigorous-latex" data-reader-layer="rigorous-latex">
  <summary>ASTIS rigorous LaTeX</summary>
  <div class="sw-casebook-disclosure-body">{''.join(pieces)}</div>
</details>
"""


def lean_details(
    case: dict[str, Any],
    audit: dict[str, Any] | None,
    active_meta: dict[str, Any] | None,
) -> str:
    declarations = [str(item) for item in case.get("lean_declarations", []) if str(item).strip()]
    rows: list[str] = []
    if active_meta:
        compiled = active_meta.get("compiled_segment", {})
        if isinstance(compiled, dict):
            assembly = str(compiled.get("assembly_lean", "")).strip()
            if assembly:
                rows.append(
                    '<div class="sw-lean-result"><strong>Compiled source-facing segment</strong>'
                    f'<code>{esc(assembly)}</code></div>'
                )
            for raw in compiled.get("proof_steps", []):
                if isinstance(raw, dict) and str(raw.get("lean", "")).strip():
                    rows.append(f'<code>{esc(raw.get("lean"))}</code>')
    for declaration in declarations:
        rows.append(f'<code>{esc(declaration)}</code>')
    target = str(audit.get("lean_target", "")) if audit else ""
    if target:
        rows.append(f'<p><strong>Next exact Lean target.</strong> {esc(target)}</p>')
    if not rows:
        rows.append(
            '<p>No compiled source-facing theorem declaration is claimed for this case yet. This is a formalization status, not evidence against the mathematical source result.</p>'
        )
    return f"""
<details class="sw-casebook-disclosure sw-lean-formalization" data-reader-layer="lean">
  <summary>Lean formalization</summary>
  <div class="sw-casebook-disclosure-body">{''.join(rows)}</div>
</details>
"""


def references_section(case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    refs = source_refs(case)
    if audit is not None:
        audit_url = str(audit.get("source_url", "")).strip()
        audit_label = " — ".join(
            item for item in (str(audit.get("source_title", "")).strip(), str(audit.get("theorem_label", "")).strip()) if item
        )
        if audit_url and all(ref.get("url") != audit_url for ref in refs):
            refs.insert(0, {"label": audit_label or audit_url, "url": audit_url})
    links = "".join(
        f'<li><a href="{esc(ref["url"])}">{esc(ref["label"])}</a></li>' for ref in refs
    ) or '<li>No primary theorem reference pinned.</li>'
    case_id = str(case.get("id", ""))
    snapshot = str(case.get("row_sha256", ""))[:16]
    return f"""
<section class="sw-casebook-references">
  <h2>References and provenance</h2>
  <ul>{links}</ul>
  <p><a href="{esc(str(case.get("source_page", "")))}">SampleWiki setting</a></p>
  <p class="sw-provenance-code"><code>{esc(case_id)}</code>{f' · source snapshot <code>{esc(snapshot)}</code>' if snapshot else ''}</p>
</section>
"""


def case_main(
    rel_path: str,
    case: dict[str, Any],
    audit: dict[str, Any] | None,
    active_meta: dict[str, Any] | None,
) -> str:
    status, _ = statement_status(case, audit)
    return f"""
<article class="sw-casebook-reader" data-samplewiki-case="{esc(case.get('id', ''))}">
  <nav class="reader-breadcrumb" aria-label="Breadcrumb">
    <a href="{esc(href_from(rel_path, OVERVIEW))}">SampleWiki</a><span>/</span>
    <a href="{esc(href_from(rel_path, setting_path(str(case.get('setting_slug', '')))))}">{esc(case.get('setting_title', ''))}</a>
  </nav>
  <header class="sw-casebook-header">
    <div class="sw-casebook-kicker">{esc(case.get('result_class', 'Result'))} · {esc(status)}</div>
    <h1>{esc(case.get('algorithm_or_model', 'SampleWiki result'))}</h1>
    <p class="sw-casebook-lede">A source-linked mathematical case study in the {esc(case.get('setting_title', 'sampling'))} regime.</p>
  </header>
  {statement_section(case, audit)}
  {proof_section(case, audit)}
  {assumptions_section(case, audit)}
  {rigorous_details(case, audit, active_meta)}
  {lean_details(case, audit, active_meta)}
  {references_section(case, audit)}
</article>
"""


def preview_formula(case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    formulas = statement_formulas(case, audit)
    if not formulas:
        return '<p class="sw-preview-open">Matching result remains open.</p>'
    return "".join(
        f'<div class="sw-preview-formula"><span>{esc(label)}</span>{formula_html(formula)}</div>'
        for label, formula in formulas[:2]
    )


def case_preview(rel_path: str, case: dict[str, Any], audit: dict[str, Any] | None) -> str:
    status, label = statement_status(case, audit)
    refs = source_refs(case)
    paper = refs[0] if refs else None
    source_line = (
        f'<a class="sw-preview-source" href="{esc(paper["url"])}">{esc(paper["label"])}</a>'
        if paper
        else '<span class="sw-reference-pending">Primary theorem reference pending</span>'
    )
    return f"""
<article class="sw-theorem-preview">
  <div class="sw-casebook-kicker">{esc(case.get('result_class', 'Result'))} · {esc(status)}</div>
  <h2><a href="{esc(href_from(rel_path, case_path(str(case.get('id', '')))))}">{esc(case.get('algorithm_or_model', ''))}</a></h2>
  <p class="sw-preview-label">{esc(label)}</p>
  {preview_formula(case, audit)}
  <div class="sw-preview-footer">{source_line}<a href="{esc(href_from(rel_path, case_path(str(case.get('id', '')))))}">Read statement and proof route →</a></div>
</article>
"""


def setting_main(
    rel_path: str,
    setting: dict[str, Any],
    cases: list[dict[str, Any]],
    audits: dict[str, Any],
) -> str:
    previews = "".join(case_preview(rel_path, case, audit_for(case, audits)) for case in cases)
    return f"""
<article class="sw-setting-reader">
  <nav class="reader-breadcrumb"><a href="{esc(href_from(rel_path, OVERVIEW))}">SampleWiki</a></nav>
  <header class="sw-casebook-header">
    <div class="sw-casebook-kicker">Sampling regime</div>
    <h1>{esc(setting.get('setting_title', ''))}</h1>
    <p class="sw-casebook-lede">Compare theorems by mathematical guarantee, rate, and source — not by raw crawler rows.</p>
    <p><a href="{esc(setting.get('source_page', ''))}">Open the live SampleWiki setting ↗</a></p>
  </header>
  <section class="sw-setting-theorems">
    <div class="sw-reader-step">Theorem and frontier cases</div>
    <div class="sw-theorem-preview-list">{previews}</div>
  </section>
</article>
"""


def overview_main(
    pages: list[dict[str, Any]],
    cases: list[dict[str, Any]],
    audits: dict[str, Any],
    reader: dict[str, Any],
) -> str:
    by_setting: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        by_setting.setdefault(str(case.get("setting_slug", "")), []).append(case)
    cards = []
    for page in pages:
        slug = str(page.get("setting_slug", ""))
        group = by_setting.get(slug, [])
        exact = sum(audit_for(case, audits) is not None for case in group)
        open_count = sum(literature_open(case) for case in group)
        cards.append(
            '<a class="sw-setting-book-card" href="' + esc(href_from(OVERVIEW, setting_path(slug))) + '">'
            f'<span>{esc(page.get("setting_title", slug))}</span>'
            f'<small>{len(group)} mathematical cases · {exact} primary-source theorem audits'
            + (f' · {open_count} open frontier' if open_count else '')
            + '</small></a>'
        )
    active_id = str(reader.get("active_case_id", ""))
    active_case = next((case for case in cases if str(case.get("id", "")) == active_id), None)
    focus = ""
    if active_case:
        audit = audit_for(active_case, audits)
        focus = (
            '<section class="sw-overview-focus"><div class="sw-reader-step">Current formalization focus</div>'
            f'<h2>{esc(active_case.get("algorithm_or_model", ""))}</h2>'
            + preview_formula(active_case, audit)
            + f'<a href="{esc(href_from(OVERVIEW, case_path(active_id)))}">Open theorem, proof route, and Lean boundary →</a></section>'
        )
    return f"""
<article class="sw-casebook-home">
  <header class="sw-casebook-header sw-casebook-home-header">
    <div class="sw-casebook-kicker">Sampling frontier · source-linked theorem casebook</div>
    <h1>SampleWiki in ASTIS</h1>
    <p class="sw-casebook-lede">A mathematical reading interface for frontier sampling results. Every case separates what the source states, how the proof runs, what assumptions are inherited, and what Lean has actually verified.</p>
    <div class="hero-actions"><a class="button" href="{esc(href_from(OVERVIEW, PROGRESS))}">Formalization progress</a><a class="button" href="{esc(href_from(OVERVIEW, FRONTIER))}">Open frontier</a></div>
  </header>
  <section class="sw-overview-focus" id="cross-library-state-preparation">
    <div class="sw-reader-step">Cross-library worked problem · sampling structure meets quantum state preparation</div>
    <h2>Smooth auxiliary states for Schrödingerisation of PDEs</h2>
    <p>Jin–Liu–Ma’s Schrödingerisation construction for PDEs with physical boundary or interface conditions introduces a smooth auxiliary \(p\)-register initial state. If its \(2^{n_p}\) grid amplitudes are treated as unrelated data, generic loading is exponential in the register width. QuantumComputinglib/ASPBE instead exploits the exact Hermite–Bernstein/tensor-train representation and proves a constructive circuit bound</p>
    <div class="formula sw-casebook-formula">\[G\le 48n_p(2k+6)^3,\qquad q=\lceil\log_2(2k+6)\rceil.\]</div>
    <p>Thus, for fixed smoothness order \(k\), the gate count is <strong>linear in \(n_p\)</strong>, rather than the generic \(\Theta(2^{n_p})\) amplitude-loading dependence. This is a SampleWiki-style lesson beyond sampling itself: the decisive question is often whether analytical structure exposes a bounded-memory representation before one accepts a black-box oracle or dense table.</p>
    <p class="sw-primary-source"><a href="https://arxiv.org/abs/2403.19123v3">Jin–Liu–Ma: source PDE / Schrödingerisation construction</a> · <a href="https://arxiv.org/abs/2005.04351">Holmes–Matsuura: prior smooth-function-to-MPS state-preparation route</a></p>
    <p><a class="button" href="https://dakebu.github.io/Quantum-Computing-Block-Encoding/example-cases/hermite-smooth-state-preparation/index.html">Open the Lean-verified QuantumComputinglib construction and proof →</a></p>
    <p class="sw-provenance-code">Cross-library pointer only: Samplinglib does not claim this quantum theorem as a local Lean result, and the general function-to-MPS idea is prior art.</p>
  </section>
  <section><div class="sw-reader-step">Choose a mathematical regime</div><div class="sw-setting-book-list">{''.join(cards)}</div></section>
  {focus}
</article>
"""


def progress_main(
    pages: list[dict[str, Any]],
    cases: list[dict[str, Any]],
    audits: dict[str, Any],
    registry: dict[str, Any],
) -> str:
    exact = sum(audit_for(case, audits) is not None for case in cases)
    open_count = sum(literature_open(case) for case in cases)
    pending = len(cases) - exact - open_count
    phases = []
    for raw in registry.get("formalization_phases", []):
        if not isinstance(raw, dict):
            continue
        phases.append(
            '<article class="sw-phase-card">'
            f'<span>Phase {esc(raw.get("id", ""))} · {esc(raw.get("status", ""))}</span>'
            f'<h2>{esc(raw.get("title", ""))}</h2>'
            '<ol>' + ''.join(f'<li>{esc(item)}</li>' for item in raw.get("items", [])) + '</ol></article>'
        )
    groups = []
    for page in pages:
        slug = str(page.get("setting_slug", ""))
        group = [case for case in cases if str(case.get("setting_slug", "")) == slug]
        links = []
        for case in group:
            audit = audit_for(case, audits)
            status, _ = statement_status(case, audit)
            links.append(
                f'<li><a href="{esc(href_from(PROGRESS, case_path(str(case.get("id", "")))))}">{esc(case.get("algorithm_or_model", ""))}</a><span>{esc(status)}</span></li>'
            )
        groups.append(
            f'<details class="sw-progress-group"><summary>{esc(page.get("setting_title", slug))}</summary><ul>{"".join(links)}</ul></details>'
        )
    return f"""
<article class="sw-casebook-progress">
  <nav class="reader-breadcrumb"><a href="{esc(href_from(PROGRESS, OVERVIEW))}">SampleWiki</a></nav>
  <header class="sw-casebook-header"><div class="sw-casebook-kicker">Formalization progress</div><h1>Source audit and Lean progress</h1><p class="sw-casebook-lede">Theorem audit, mathematical dependencies, and Lean completion are tracked separately.</p></header>
  <section class="sw-progress-metrics"><div><strong>{exact}</strong><span>exact theorem audits</span></div><div><strong>{pending}</strong><span>primary theorem audits pending</span></div><div><strong>{open_count}</strong><span>literature-open cases</span></div><div><strong>{len(cases)}</strong><span>mathematical cases</span></div></section>
  <section><div class="sw-reader-step">Dependency-first formalization route</div><div class="sw-phase-grid">{''.join(phases)}</div></section>
  <section><div class="sw-reader-step">Case audit index</div><div class="sw-progress-groups">{''.join(groups)}</div></section>
</article>
"""


def frontier_main(cases: list[dict[str, Any]], audits: dict[str, Any], reader: dict[str, Any]) -> str:
    open_cases = [case for case in cases if literature_open(case)]
    cards = "".join(case_preview(FRONTIER, case, audit_for(case, audits)) for case in open_cases)
    active_id = str(reader.get("active_case_id", ""))
    active_case = next((case for case in cases if str(case.get("id", "")) == active_id), None)
    focus = ""
    if active_case:
        focus = (
            '<section><div class="sw-reader-step">Formalization frontier</div>'
            f'<h2>{esc(active_case.get("algorithm_or_model", ""))}</h2>'
            + preview_formula(active_case, audit_for(active_case, audits))
            + f'<a href="{esc(href_from(FRONTIER, case_path(active_id)))}">Inspect exact open Lean interfaces →</a></section>'
        )
    return f"""
<article class="sw-casebook-frontier">
  <nav class="reader-breadcrumb"><a href="{esc(href_from(FRONTIER, OVERVIEW))}">SampleWiki</a></nav>
  <header class="sw-casebook-header"><div class="sw-casebook-kicker">Open problems</div><h1>Sampling frontier</h1><p class="sw-casebook-lede">Literature-open mathematical questions are separated from results whose mathematics is known but whose Lean dependency graph is still incomplete.</p></header>
  <section><div class="sw-reader-step">Literature-open cases</div><div class="sw-theorem-preview-list">{cards}</div></section>
  {focus}
</article>
"""


def replace_main(text: str, body: str, rel_path: str) -> str:
    pattern = re.compile(r'(<main id="content">).*?(</main>)', flags=re.S)
    if not pattern.search(text):
        raise RuntimeError(f"{rel_path}: main content marker missing")
    return pattern.sub(lambda match: match.group(1) + body + match.group(2), text, count=1)


def add_style(text: str, rel_path: str) -> str:
    href = href_from(rel_path, f"assets/{STYLE_NAME}")
    if STYLE_NAME in text:
        return text
    marker = "</head>"
    if marker not in text:
        raise RuntimeError(f"{rel_path}: head marker missing")
    return text.replace(marker, f'  <link rel="stylesheet" href="{esc(href)}">\n</head>', 1)


def write_final(path: Path, rel_path: str, body: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_main(text, body, rel_path)
    text = add_style(text, rel_path)
    # Raw crawler row text remains in source-index JSON only, never in reader HTML.
    text = re.sub(r'<details class="sw-raw-row">.*?</details>', "", text, flags=re.S)
    path.write_text(text, encoding="utf-8", newline="\n")


def validate_site(
    output: Path,
    cases: list[dict[str, Any]],
    pages: list[dict[str, Any]],
    audits: dict[str, Any],
) -> None:
    errors: list[str] = []
    expected_case_paths = [case_path(str(case.get("id", ""))) for case in cases]
    expected_setting_paths = [setting_path(str(page.get("setting_slug", ""))) for page in pages]
    all_paths = [OVERVIEW, PROGRESS, FRONTIER, *expected_setting_paths, *expected_case_paths]

    for rel_path in all_paths:
        path = output / rel_path
        if not path.exists():
            errors.append(f"missing SampleWiki page: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if STYLE_NAME not in text:
            errors.append(f"{rel_path}: final SampleWiki math-reader stylesheet missing")
        if "Raw pinned row text" in text or "sw-raw-row" in text:
            errors.append(f"{rel_path}: raw pinned row UI leaked into reader")
        if "\\mathcal\\]" in text or "\\widetilde\\]" in text or "\\sqrt\\]" in text:
            errors.append(f"{rel_path}: bare TeX command leaked into MathJax")

    for case in cases:
        case_id = str(case.get("id", ""))
        rel_path = case_path(case_id)
        path = output / rel_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        required = [
            'data-reader-layer="statement"',
            'data-reader-layer="proof"',
            'data-reader-layer="assumptions"',
            'data-reader-layer="rigorous-latex"',
            'data-reader-layer="lean"',
        ]
        positions = [text.find(marker) for marker in required]
        if any(position < 0 for position in positions):
            errors.append(f"{case_id}: missing one of the five reader layers")
        elif positions != sorted(positions):
            errors.append(f"{case_id}: reader layers are out of order")

        audit = audit_for(case, audits)
        if audit is not None:
            statement = validate_latex(str(audit.get("statement_latex", "")), context=case_id)
            if esc(statement) not in text:
                errors.append(f"{case_id}: audited source theorem statement missing")
            if str(audit.get("theorem_label", "")) not in text:
                errors.append(f"{case_id}: audited theorem label missing")
            if "omitted" in str(audit.get("source_proof_status", "")).lower() and "omits this proof" not in text and "proof omitted" not in text:
                errors.append(f"{case_id}: explicit source proof omission was lost")
        elif literature_open(case):
            if "Open problem" not in text or "no synthetic proof" not in text:
                errors.append(f"{case_id}: literature-open truth boundary missing")
        else:
            if "Normalized SampleWiki statement" not in text or "Primary theorem audit pending" not in text:
                errors.append(f"{case_id}: pending theorem-audit boundary missing")
            if not source_refs(case):
                errors.append(f"{case_id}: cited known result has no concrete paper reference")
            if not statement_formulas(case, None):
                errors.append(f"{case_id}: known result has no clean mathematical formula")

    if sum(literature_open(case) for case in cases) != 4:
        errors.append("SampleWiki literature-open partition changed from the audited four cases")
    if len(cases) != 34:
        errors.append(f"SampleWiki reader expected 34 cases, found {len(cases)}")
    if len(pages) != 7:
        errors.append(f"SampleWiki reader expected 7 settings, found {len(pages)}")

    if errors:
        raise RuntimeError("SampleWiki final reader contract failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    manifest = load_object(CASES_PATH)
    registry = load_object(AUDIT_PATH)
    reader = load_object(READER_PATH)
    cases = [dict(item) for item in manifest.get("cases", []) if isinstance(item, dict)]
    pages = [dict(item) for item in manifest.get("pages", []) if isinstance(item, dict)]
    audits_raw = registry.get("case_audits", {})
    if not isinstance(audits_raw, dict):
        raise RuntimeError("samplewiki_frontier_audit.case_audits must be an object")
    audits: dict[str, Any] = audits_raw

    asset_dir = output / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(STYLE_PATH, asset_dir / STYLE_NAME)

    by_setting: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        by_setting.setdefault(str(case.get("setting_slug", "")), []).append(case)

    write_final(output / OVERVIEW, OVERVIEW, overview_main(pages, cases, audits, reader))
    write_final(output / PROGRESS, PROGRESS, progress_main(pages, cases, audits, registry))
    write_final(output / FRONTIER, FRONTIER, frontier_main(cases, audits, reader))

    for page in pages:
        slug = str(page.get("setting_slug", ""))
        rel_path = setting_path(slug)
        write_final(
            output / rel_path,
            rel_path,
            setting_main(rel_path, page, by_setting.get(slug, []), audits),
        )

    active_id = str(reader.get("active_case_id", ""))
    active_meta_raw = reader.get("active_case", {})
    active_meta = dict(active_meta_raw) if isinstance(active_meta_raw, dict) else {}
    for case in cases:
        case_id = str(case.get("id", ""))
        rel_path = case_path(case_id)
        write_final(
            output / rel_path,
            rel_path,
            case_main(
                rel_path,
                case,
                audit_for(case, audits),
                active_meta if case_id == active_id else None,
            ),
        )

    validate_site(output, cases, pages, audits)


if __name__ == "__main__":
    enrich_site()
