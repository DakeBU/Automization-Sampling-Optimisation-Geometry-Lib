#!/usr/bin/env python3
"""Enforce the math-first public reading contract for Samplinglib.

Canonical textbook pages should read like mathematics, not like a tutorial
chat transcript.  This final post-build layer therefore:

* removes the long undergraduate story ladder from canonical section pages;
* rewrites completed Chewi lessons as source statement -> displayed equations
  -> source proof status -> ASTIS formal expansion -> Lean correspondence;
* repairs leaked Markdown bold markers and a small set of raw ASCII formulas;
* fails the build on visible CJK text or leaked Markdown in generated HTML.

It is presentation-only and does not alter Lean/source verification status.
"""

from __future__ import annotations

import html
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "website" / "content"
DEFAULT_OUTPUT = ROOT / "_site"
UNDERGRAD_START = "<!-- ASTIS_UNDERGRAD_GUIDE_START -->"
UNDERGRAD_END = "<!-- ASTIS_UNDERGRAD_GUIDE_END -->"
LESSON_START = "<!-- ASTIS_THEOREM_LESSONS_START -->"
LESSON_END = "<!-- ASTIS_THEOREM_LESSONS_END -->"
STYLE_NAME = "math-first-reader.css"
SOURCE_STYLE = ROOT / "website" / "static" / STYLE_NAME
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


STATEMENT_OVERRIDES: dict[str, list[str]] = {
    "chewi-proposition-1-1-13-lesson": [
        r"A_t(\omega):=\int_0^t \eta_s(\omega)^2\,ds,\qquad "
        r"\tau_n:=\inf\{t\in[0,T]:A_t\ge n+1\}\wedge T,",
        r"\tau_n\le \tau_{n+1},\qquad \tau_n\uparrow T\ \text{a.s.},\qquad "
        r"\mathbb E\!\left[\int_0^T \eta_s^2\mathbf 1_{\{s\le\tau_n\}}\,ds\right]\le n+1.",
    ],
    "chewi-proposition-1-1-16-lesson": [
        r"M_t:=\int_0^t \eta_s\,dB_s,\qquad "
        r"M_{t\wedge\tau_n}=\int_0^t \eta_s\mathbf 1_{\{s\le\tau_n\}}\,dB_s,",
        r"0\le s\le t\quad\Longrightarrow\quad "
        r"\mathbb E\!\left[M_{t\wedge\tau_n}\mid\mathcal F_s\right]=M_{s\wedge\tau_n},",
        r"\tau_n\uparrow\infty\ \text{a.s.}\quad\Longrightarrow\quad "
        r"M\in\mathcal M_{\mathrm{loc}}\ \text{and }M\text{ has continuous paths.}",
    ],
}


# Keep the source's level of detail explicit.  These cards have compiled ASTIS
# proofs, but Chewi does not supply those expanded proofs in Section 1.1.
SOURCE_PROOF_STATUS: dict[str, str] = {
    "chewi-proposition-1-1-13-lesson": (
        "Chewi explicitly says that this proposition barely needs a proof and omits it. "
        "The expansion below is the ASTIS formal proof, not a reconstruction attributed to the book."
    ),
    "chewi-proposition-1-1-16-lesson": (
        "Chewi defines the localized Itô integral through the stopped processes in (1.1.14) and says "
        "that the technical details are omitted.  The expansion below records the ASTIS proof obligations."
    ),
}


PROOF_OVERRIDES: dict[str, list[dict[str, str]]] = {
    "chewi-proposition-1-1-13-lesson": [
        {
            "title": "Accumulated energy",
            "text": "The energy process is adapted, continuous, and nondecreasing.",
            "latex": r"A_t=\int_0^t\eta_s^2\,ds,\qquad 0\le s\le t\le T\Longrightarrow A_s\le A_t.",
        },
        {
            "title": "Stopping-time property",
            "text": "Continuity turns first passage into a fixed-time measurable event.",
            "latex": r"\{\tau_n\le t\}=\{A_t\ge n+1\}\in\mathcal F_t\qquad (t<T).",
        },
        {
            "title": "Stopped energy",
            "text": "Before the first hit, accumulated energy cannot exceed the threshold.",
            "latex": r"\int_0^T\eta_s^2\mathbf 1_{\{s\le\tau_n\}}\,ds=A_{\tau_n}\le n+1.",
        },
        {
            "title": "Global square integrability",
            "text": "Integrating the pathwise bound gives the global L2 estimate required by the Itô integral.",
            "latex": r"\mathbb E\!\left[\int_0^T\eta_s^2\mathbf 1_{\{s\le\tau_n\}}\,ds\right]\le n+1<\infty.",
        },
        {
            "title": "Exhaustion",
            "text": "If the terminal energy is finite, every sufficiently high level is never reached.",
            "latex": r"A_T(\omega)<\infty\quad\Longrightarrow\quad \exists N(\omega)\ \forall n\ge N(\omega),\ \tau_n(\omega)=T.",
        },
    ],
    "chewi-proposition-1-1-16-lesson": [
        {
            "title": "Localize into the L2 theory",
            "text": "For each canonical localizer, the stopped integrand is a legal global-L2 integrand.",
            "latex": r"\eta^{(n)}_s:=\eta_s\mathbf 1_{\{s\le\tau_n\}},\qquad "
                     r"\mathbb E\int_0^T|\eta^{(n)}_s|^2\,ds<\infty.",
        },
        {
            "title": "Apply the global Itô theorem",
            "text": "Theorem 1.1.8 produces a continuous martingale on every localized window.",
            "latex": r"M^{(n)}_t:=\int_0^t\eta^{(n)}_s\,dB_s,\qquad "
                     r"\mathbb E[M^{(n)}_t\mid\mathcal F_s]=M^{(n)}_s\quad(s\le t).",
        },
        {
            "title": "Random stopping commutes with Itô integration",
            "text": "Grid-valued stopping is finite-sum algebra; dyadic approximation and the Itô isometry pass to bounded stopping times.",
            "latex": r"\left(\int_0^{\cdot}\eta_s\,dB_s\right)_{t\wedge\tau}="
                     r"\int_0^t\eta_s\mathbf 1_{\{s\le\tau\}}\,dB_s.",
        },
        {
            "title": "Endpoint convention",
            "text": "Strict and closed stopping differ only on the stopping graph, which is product-measure null.",
            "latex": r"(dt\otimes d\mathbb P)\{(s,\omega):s=\tau(\omega)\}=0.",
        },
        {
            "title": "Coherence",
            "text": "Localized martingales agree on every common stopping window.",
            "latex": r"k\le \ell\quad\Longrightarrow\quad "
                     r"M^{(\ell)}_{t\wedge\tau_k}=M^{(k)}_t\qquad\text{a.s. for all }t.",
        },
        {
            "title": "Glue and localize",
            "text": "Coherence defines one continuous process whose stopped versions are genuine martingales.",
            "latex": r"M^{\tau_k}=M^{(k)}\in\mathcal M_c,\qquad \tau_k\uparrow\infty\ \text{a.s.}",
        },
        {
            "title": "Conclusion",
            "text": "This is exactly the definition of a continuous local martingale.",
            "latex": r"M_t=\int_0^t\eta_s\,dB_s\in\mathcal M_{\mathrm{loc}}\cap C([0,\infty)).",
        },
    ],
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower() or "entry"


def section_path(output: Path, section: str) -> Path:
    chapter = int(section.split(".", 1)[0])
    return output / "textbook" / f"chapter-{chapter:02d}" / f"section-{slugify(section)}.html"


def display_math(latex: str) -> str:
    return f'<div class="formula math-first-display">\\[{esc(latex)}\\]</div>'


def load_lessons() -> list[dict[str, Any]]:
    raw = json.loads((CONTENT / "theorem_lessons.json").read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise RuntimeError("theorem_lessons.json must contain a list")
    return [dict(item) for item in raw if isinstance(item, dict)]


def source_link(item: dict[str, Any]) -> str:
    return (
        f'<a class="source-anchor math-source-link" href="{esc(item["source_url"])}">'
        f'Chewi, {esc(item["source_kind"])} ↗</a>'
    )


def render_assumptions(item: dict[str, Any]) -> str:
    values = [str(x) for x in item.get("source_assumptions", [])]
    if not values:
        return ""
    return '<ul class="math-assumptions">' + "".join(f"<li>{esc(x)}</li>" for x in values) + "</ul>"


def render_proof(item: dict[str, Any]) -> str:
    blocks = PROOF_OVERRIDES.get(str(item.get("id")), [])
    if not blocks:
        blocks = [
            {
                "title": str(step.get("title", "Proof step")),
                "text": str(step.get("text", "")),
                "latex": str(step.get("latex", "")),
            }
            for step in item.get("proof_steps", [])
            if isinstance(step, dict)
        ]
    rendered = []
    for index, block in enumerate(blocks, 1):
        formula = display_math(block["latex"]) if block.get("latex") else ""
        rendered.append(
            '<div class="math-proof-step">'
            f'<div class="math-proof-index">{index}</div>'
            '<div>'
            f'<h4>{esc(block["title"])}</h4>'
            f'{formula}'
            f'<p>{esc(block["text"])}</p>'
            '</div></div>'
        )
    return '<div class="math-proof">' + "".join(rendered) + "</div>"


def render_lean_correspondence(item: dict[str, Any]) -> str:
    rows = []
    for index, raw in enumerate(item.get("lean_layers", []), 1):
        if not isinstance(raw, dict):
            continue
        declarations = [str(x) for x in raw.get("declarations", [])]
        decl_html = "<br>".join(f'<code>{esc(name.rsplit(".", 1)[-1])}</code>' for name in declarations)
        rows.append(
            '<tr>'
            f'<td>{index}</td><td><strong>{esc(raw.get("title", ""))}</strong><br>'
            f'<span>{esc(raw.get("role", ""))}</span></td><td>{decl_html}</td>'
            '</tr>'
        )
    if not rows:
        return ""
    return (
        '<details class="reader-disclosure lean-disclosure math-lean-correspondence">'
        '<summary>Lean correspondence</summary><div class="disclosure-body">'
        '<div class="table-wrap"><table><thead><tr><th>#</th><th>Mathematical step</th><th>Lean lemmas</th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table></div>'
        f'<p class="card-meta">Focused test: <code>{esc(item.get("focused_test", ""))}</code></p>'
        '</div></details>'
    )


def render_lesson(item: dict[str, Any]) -> str:
    item_id = str(item.get("id", ""))
    formulas = STATEMENT_OVERRIDES.get(item_id)
    if not formulas:
        formulas = [str(item.get("formula", ""))]
    statement_math = "".join(display_math(value) for value in formulas if value)
    proof_status = SOURCE_PROOF_STATUS.get(item_id)
    if proof_status:
        proof_section = (
            '<section class="math-theorem-proof math-source-proof-status">'
            '<h3>Chewi proof status</h3>'
            f'<p>{esc(proof_status)}</p>'
            '<details class="reader-disclosure math-astis-proof">'
            '<summary>ASTIS formal expansion</summary><div class="disclosure-body">'
            f'{render_proof(item)}'
            '</div></details>'
            '</section>'
        )
    else:
        proof_section = (
            '<section class="math-theorem-proof">'
            '<h3>Proof</h3>'
            f'{render_proof(item)}'
            '</section>'
        )
    return f"""
<article class="textbook-block theorem-lesson-card math-first-theorem" id="{esc(item_id)}" data-chewi-theorem="{esc(item.get('number', ''))}">
  <header class="math-theorem-header">
    <div class="passage-label">{esc(item.get('source_kind', 'Theorem'))}</div>
    <h2>{esc(item.get('title', ''))}</h2>
  </header>
  <section class="math-theorem-statement">
    <h3>Chewi statement</h3>
    {statement_math}
    <p class="math-source-summary">{esc(item.get('source_statement', ''))}</p>
    <details class="math-assumption-disclosure"><summary>Assumptions</summary>{render_assumptions(item)}</details>
  </section>
  {proof_section}
  {render_lean_correspondence(item)}
  {source_link(item)}
</article>"""


def render_lesson_section(items: list[dict[str, Any]]) -> str:
    return (
        LESSON_START
        + '\n<section class="source-theorem-lessons math-first-lessons" id="source-theorem-lessons">'
        + '<div class="section-heading"><span>Chewi results with compiled ASTIS proofs</span>'
        + '<h2>Source statements and formal expansions</h2></div>'
        + "".join(render_lesson(item) for item in items)
        + '</section>\n'
        + LESSON_END
    )


def strip_between(text: str, start: str, end: str) -> str:
    return re.sub(re.escape(start) + r".*?" + re.escape(end), "", text, flags=re.S)


def replace_lesson_block(text: str, rendered: str) -> str:
    pattern = re.compile(re.escape(LESSON_START) + r".*?" + re.escape(LESSON_END), re.S)
    if pattern.search(text):
        return pattern.sub(rendered, text, count=1)
    marker = '<nav class="reader-pagination"'
    if marker not in text:
        raise RuntimeError("reader pagination marker missing while inserting theorem lessons")
    return text.replace(marker, rendered + "\n" + marker, 1)


def non_code_segments(text: str) -> list[str]:
    return re.split(r"(<(?:pre|code|script|style)\b[^>]*>.*?</(?:pre|code|script|style)>)", text, flags=re.S | re.I)


def repair_visible_markup(text: str) -> str:
    parts = non_code_segments(text)
    for i in range(0, len(parts), 2):
        segment = parts[i]
        segment = re.sub(r"\*\*([^*<>]+?)\*\*", r"<strong>\1</strong>", segment)
        segment = re.sub(r"(<p[^>]*>)\s*-\s*(?=<strong>)", r"\1", segment)
        segment = segment.replace(
            "For s <= t, E[M_t | F_s] = M_s",
            r"For \\(s\le t\\), \\(\mathbb E[M_t\mid\mathcal F_s]=M_s\\)",
        )
        segment = segment.replace(
            "E[M_t | F_s] = M_s",
            r"\\(\mathbb E[M_t\mid\mathcal F_s]=M_s\\)",
        )
        parts[i] = segment
    return "".join(parts)


def inject_style(text: str, rel: Path) -> str:
    prefix = "../" * len(rel.parent.parts)
    href = f"{prefix}assets/{STYLE_NAME}"
    if href in text:
        return text
    return text.replace("</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', 1)


def visible_text(text: str) -> str:
    value = re.sub(r"<(?:pre|code|script|style)\b[^>]*>.*?</(?:pre|code|script|style)>", " ", text, flags=re.S | re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    return html.unescape(value)


def validate_page(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    visible = visible_text(text)
    cjk = CJK_RE.search(visible)
    if cjk:
        start = max(0, cjk.start() - 60)
        errors.append(f"{path}: visible non-English/CJK text: {visible[start:cjk.start()+60]!r}")
    if "**" in visible:
        errors.append(f"{path}: leaked Markdown bold marker '**'")
    if re.search(r"\bE\[\s*M_[^\]]*\|\s*F_", visible):
        errors.append(f"{path}: raw conditional-expectation formula leaked outside MathJax")
    if " <= " in visible and re.search(r"[A-Za-z]_[A-Za-z0-9]", visible):
        errors.append(f"{path}: raw ASCII inequality remains near mathematical notation")
    return errors


def validate(output: Path) -> None:
    errors: list[str] = []
    for path in output.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        errors.extend(validate_page(path.relative_to(output), text))
    for path in (output / "textbook" / "chapter-01").glob("section-*.html"):
        text = path.read_text(encoding="utf-8")
        if UNDERGRAD_START in text or "story-ladder" in text:
            errors.append(f"{path.relative_to(output)}: undergraduate story ladder remains on canonical textbook page")
    section_11 = output / "textbook" / "chapter-01" / "section-1-1.html"
    if section_11.exists():
        text = section_11.read_text(encoding="utf-8")
        for theorem_id in STATEMENT_OVERRIDES:
            anchor = f'id="{theorem_id}"'
            if anchor not in text:
                errors.append(f"section-1-1.html: missing math-first theorem card {theorem_id}")
        for theorem_id, status in SOURCE_PROOF_STATUS.items():
            if f'id="{theorem_id}"' in text and esc(status) not in text:
                errors.append(f"section-1-1.html: missing source proof-status note for {theorem_id}")
        for latex in (
            r"\mathbb E\!\left[M_{t\wedge\tau_n}\mid\mathcal F_s\right]",
            r"\int_0^T\eta_s^2\mathbf 1_{\{s\le\tau_n\}}",
        ):
            if esc(latex) not in text:
                errors.append(f"section-1-1.html: missing displayed proof formula {latex}")
    if errors:
        raise RuntimeError("math-first reader validation failed:\n- " + "\n- ".join(errors))


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    asset_dir = output / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    (asset_dir / STYLE_NAME).write_text(SOURCE_STYLE.read_text(encoding="utf-8"), encoding="utf-8")

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in load_lessons():
        grouped[str(item.get("section", ""))].append(item)

    for section, items in grouped.items():
        path = section_path(output, section)
        if not path.exists():
            raise RuntimeError(f"missing generated textbook section: {path}")
        text = path.read_text(encoding="utf-8")
        text = strip_between(text, UNDERGRAD_START, UNDERGRAD_END)
        text = replace_lesson_block(text, render_lesson_section(items))
        path.write_text(text, encoding="utf-8", newline="\n")

    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output)
        text = path.read_text(encoding="utf-8")
        text = repair_visible_markup(text)
        text = inject_style(text, rel)
        path.write_text(text, encoding="utf-8", newline="\n")

    validate(output)


if __name__ == "__main__":
    enrich_site()
