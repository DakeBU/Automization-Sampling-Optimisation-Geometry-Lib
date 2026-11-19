#!/usr/bin/env python3
"""Final public-reader contract for Samplinglib.

This wrapper deliberately separates presentation cleanup from source evidence.
It reuses ``math_first_reader`` for theorem/equation layout, then applies
ASTIS-owned statement/proof equation layers to canonical Chapter 1 source
cards. Audited source metadata is never rewritten: supplements are
presentation restatements keyed by stable source-correspondence ids.
"""

from __future__ import annotations

import json
from html.parser import HTMLParser
import re
import shutil
from pathlib import Path
from typing import Any

import math_first_reader as base


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
SOURCE_CSS = ROOT / "website" / "static" / "reader-contract-final.css"
STYLE_NAME = "reader-contract-final.css"
DIAGNOSTIC = ROOT / ".astis" / "reader-contract-errors.txt"
FORMULA_SUPPLEMENTS = ROOT / "website" / "content" / "chapter1_formula_supplements.json"
PROOF_SUPPLEMENTS = ROOT / "website" / "content" / "chapter1_proof_supplements.json"
SOURCE_CORRESPONDENCE = ROOT / "website" / "content" / "source_correspondence.json"
FORMULA_FIRST_SECTIONS = ("1.1", "1.2", "1.3", "1.4")
READER_TEXT_ATTRIBUTES = {"aria-label", "aria-description", "aria-roledescription",
                          "aria-valuetext", "alt", "title", "placeholder"}


class ReaderLanguageAttributes(HTMLParser):
    """Check language metadata and reader attributes without rewriting source."""

    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in {"lang", "xml:lang"} and not re.fullmatch(
                    r"en(?:-[a-z0-9]+)*", value or "", re.I):
                self.errors.append(f"<{tag}> has non-English {name}={value!r}")
            if name in READER_TEXT_ATTRIBUTES and value and base.CJK_RE.search(value):
                self.errors.append(f"<{tag}> has non-English/CJK {name}={value[:100]!r}")


def public_language_errors(text: str) -> list[str]:
    tags = re.sub(r"<!--.*?-->|<(script|style)\b[^>]*>.*?</\1>", "", text, flags=re.S | re.I)
    root = re.search(r"<html(?=\s|>)[^>]*>", tags, re.I)
    errors: list[str] = []
    if not root or not re.search(r"""\slang\s*=\s*(?:"en(?:-[a-z0-9]+)*"|'en(?:-[a-z0-9]+)*'|en(?:-[a-z0-9]+)*(?=\s|>))""",
                                 root[0], re.I):
        errors.append("public document must declare English with <html lang=\"en\">")
    # Most pages have only the root lang and no CJK/encoded attribute text.
    # Parse only candidates so the whole-site gate stays inexpensive.
    if (re.search(r"<[^>]+\s(?:lang|xml:lang)\s*=", tags[(root.end() if root else 0):], re.I)
            or re.search(r"<[^>]*(?:" + base.CJK_RE.pattern + r"|&#)[^>]*>", tags)):
        parser = ReaderLanguageAttributes()
        parser.feed(tags)
        parser.close()
        errors.extend(parser.errors)
    return errors


def _write_diagnostic(message: str) -> None:
    DIAGNOSTIC.parent.mkdir(parents=True, exist_ok=True)
    DIAGNOSTIC.write_text(message.rstrip() + "\n", encoding="utf-8")


def _load_list(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise RuntimeError(f"{path.relative_to(ROOT)} must contain a JSON list")
    return [dict(item) for item in raw if isinstance(item, dict)]


def _source_entries() -> dict[str, dict[str, Any]]:
    entries = _load_list(SOURCE_CORRESPONDENCE)
    return {str(item.get("id", "")): item for item in entries if item.get("id")}


def _formula_supplements() -> dict[str, dict[str, Any]]:
    entries = _load_list(FORMULA_SUPPLEMENTS)
    return {str(item.get("id", "")): item for item in entries if item.get("id")}


def _proof_supplements() -> dict[str, dict[str, Any]]:
    entries = _load_list(PROOF_SUPPLEMENTS)
    return {str(item.get("id", "")): item for item in entries if item.get("id")}


def validate_page(path: Path, text: str) -> list[str]:
    errors = [f"{path}: {error}" for error in public_language_errors(text)]
    visible = base.visible_text(text)
    cjk = base.CJK_RE.search(visible)
    if cjk:
        start = max(0, cjk.start() - 60)
        errors.append(
            f"{path}: visible non-English/CJK text: "
            f"{visible[start:cjk.start() + 60]!r}"
        )
    if "**" in visible:
        errors.append(f"{path}: leaked Markdown bold marker '**'")
    if re.search(r"\bE\[\s*M_[^\]]*\|\s*F_", visible):
        errors.append(f"{path}: raw conditional-expectation formula leaked outside MathJax")
    return errors


def _safe_replace_lesson_block(text: str, rendered: str) -> str:
    """Replace generated lesson HTML without interpreting LaTeX backslashes."""
    pattern = re.compile(
        re.escape(base.LESSON_START) + r".*?" + re.escape(base.LESSON_END),
        re.S,
    )
    if pattern.search(text):
        return pattern.sub(lambda _match: rendered, text, count=1)
    marker = '<nav class="reader-pagination"'
    if marker not in text:
        raise RuntimeError("reader pagination marker missing while inserting theorem lessons")
    return text.replace(marker, rendered + "\n" + marker, 1)


def _patch_base_gate() -> None:
    base.validate_page = validate_page
    base.replace_lesson_block = _safe_replace_lesson_block


def _remove_undergrad_ladders(output: Path) -> None:
    chapter = output / "textbook" / "chapter-01"
    for path in chapter.glob("section-*.html"):
        text = path.read_text(encoding="utf-8")
        text = base.strip_between(text, base.UNDERGRAD_START, base.UNDERGRAD_END)
        path.write_text(text, encoding="utf-8", newline="\n")


def _source_anchor(source: dict[str, Any]) -> str:
    return (
        '<section class="source-passage">'
        f'<div class="passage-label">{base.esc(source.get("source_kind", ""))}</div>'
        f'<h2>{base.esc(source.get("source_summary", ""))}</h2>'
    )


def _render_proof_supplement(source_id: str, proof: dict[str, Any] | None) -> str:
    if not proof:
        return ""
    steps = proof.get("steps", [])
    if not isinstance(steps, list) or not steps:
        return ""
    rendered: list[str] = []
    for index, raw in enumerate(steps, 1):
        if not isinstance(raw, dict):
            continue
        latex = str(raw.get("formula", "")).strip()
        if not latex:
            continue
        lean_names = [str(name) for name in raw.get("lean", []) if str(name).strip()]
        lean_html = ""
        if lean_names:
            lean_html = (
                '<div class="source-proof-lean"><span>Lean</span> '
                + " · ".join(f'<code>{base.esc(name)}</code>' for name in lean_names)
                + "</div>"
            )
        rendered.append(
            '<div class="source-proof-step">'
            f'<div class="source-proof-index">{index}</div>'
            '<div class="source-proof-equation">'
            f'<div class="formula source-proof-formula">\\[{base.esc(latex)}\\]</div>'
            f'{lean_html}</div></div>'
        )
    if not rendered:
        return ""
    return (
        f'<div class="source-equation-proof" data-source-proof="{base.esc(source_id)}">'
        '<div class="source-proof-label">Proof</div>'
        + "".join(rendered)
        + "</div>"
    )


def _render_formula_supplement(
    source_id: str,
    supplement: dict[str, Any],
    proof: dict[str, Any] | None,
) -> str:
    latex = str(supplement.get("formula", "")).strip()
    if not latex:
        raise RuntimeError(f"formula supplement {source_id} has an empty formula")
    return (
        f'<div class="formula source-formula formula-supplement" '
        f'data-source-formula="{base.esc(source_id)}">'
        f'\\[{base.esc(latex)}\\]</div>'
        + _render_proof_supplement(source_id, proof)
    )


def _inject_formula_supplements(output: Path) -> None:
    sources = _source_entries()
    supplements = _formula_supplements()
    proofs = _proof_supplements()
    errors: list[str] = []

    unknown_proofs = sorted(set(proofs) - set(sources))
    if unknown_proofs:
        errors.extend(f"proof supplement has no source-correspondence item: {item}" for item in unknown_proofs)

    for source_id, supplement in supplements.items():
        source = sources.get(source_id)
        if source is None:
            errors.append(f"formula supplement has no source-correspondence item: {source_id}")
            continue
        section = str(source.get("section", ""))
        if section not in FORMULA_FIRST_SECTIONS:
            continue
        # An already audited latex_statement wins. Supplements only fill a
        # missing public display and never overwrite source evidence.
        if str(source.get("latex_statement", "")).strip():
            continue

        path = base.section_path(output, section)
        if not path.exists():
            errors.append(f"missing generated section for formula supplement {source_id}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        marker = f'data-source-formula="{base.esc(source_id)}"'
        if marker in text:
            continue
        anchor = _source_anchor(source)
        if anchor not in text:
            errors.append(
                f"{path.relative_to(output)}: cannot locate source card for formula supplement {source_id}"
            )
            continue
        replacement = (
            '<section class="source-passage formula-first-source" '
            f'data-source-id="{base.esc(source_id)}">'
            f'<div class="passage-label">{base.esc(source.get("source_kind", ""))}</div>'
            f'<h2>{base.esc(source.get("source_summary", ""))}</h2>'
            + _render_formula_supplement(source_id, supplement, proofs.get(source_id))
        )
        text = text.replace(anchor, replacement, 1)
        path.write_text(text, encoding="utf-8", newline="\n")

    unattached_proofs = sorted(
        source_id
        for source_id in proofs
        if source_id in sources
        and not str(sources[source_id].get("latex_statement", "")).strip()
        and source_id not in supplements
    )
    errors.extend(f"proof supplement has no formula supplement: {item}" for item in unattached_proofs)

    if errors:
        raise RuntimeError("formula/proof supplement injection failed:\n- " + "\n- ".join(errors))


def _tag_all_source_cards(output: Path) -> None:
    """Attach the stable source-correspondence id to every canonical source card.

    Formula-supplement cards are already tagged during insertion. Cards whose
    formula came from audited ``latex_statement`` fields are tagged here. This
    makes coverage validation source-id based instead of relying on CSS-class
    counts, which can be confused by presentation wrappers.
    """
    errors: list[str] = []
    for source_id, source in _source_entries().items():
        section = str(source.get("section", ""))
        if section not in FORMULA_FIRST_SECTIONS:
            continue
        path = base.section_path(output, section)
        if not path.exists():
            errors.append(f"missing generated section while tagging {source_id}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        marker = f'data-source-id="{base.esc(source_id)}"'
        if marker in text:
            continue
        anchor = _source_anchor(source)
        if anchor not in text:
            errors.append(
                f"{path.relative_to(output)}: cannot locate source card while tagging {source_id}"
            )
            continue
        replacement = (
            f'<section class="source-passage" data-source-id="{base.esc(source_id)}">'
            f'<div class="passage-label">{base.esc(source.get("source_kind", ""))}</div>'
            f'<h2>{base.esc(source.get("source_summary", ""))}</h2>'
        )
        text = text.replace(anchor, replacement, 1)
        path.write_text(text, encoding="utf-8", newline="\n")
    if errors:
        raise RuntimeError("source-card tagging failed:\n- " + "\n- ".join(errors))


def _move_existing_source_formulas_before_prose(output: Path) -> None:
    pattern = re.compile(
        r'(<section class="source-passage(?: [^"]*)?"[^>]*>'
        r'.*?<div class="passage-label">.*?</div><h2>.*?</h2>)'
        r'(<p>.*?</p>)'
        r'(<div class="formula source-formula(?: [^"]*)?"[^>]*>.*?</div>)'
        r'(</section>)',
        flags=re.S,
    )
    for section in FORMULA_FIRST_SECTIONS:
        path = base.section_path(output, section)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        text = pattern.sub(
            lambda match: match.group(1) + match.group(3) + match.group(2) + match.group(4),
            text,
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def _collapse_supplemental_details(text: str) -> str:
    return text.replace(
        '<details class="reader-disclosure rigor-disclosure" open>',
        '<details class="reader-disclosure rigor-disclosure">',
    )


def _repair_exact_public_leaks(text: str) -> str:
    parts = re.split(
        r"(<(?:pre|code|script|style)\b[^>]*>.*?</(?:pre|code|script|style)>)",
        text,
        flags=re.S | re.I,
    )
    for index in range(0, len(parts), 2):
        segment = parts[index]
        segment = segment.replace(
            "For s <= t, E[M_t | F_s] = M_s",
            r"For \\(s\le t\\), \\(\mathbb E[M_t\mid\mathcal F_s]=M_s\\)",
        )
        segment = segment.replace(
            "E[M_t | F_s] = M_s",
            r"\\(\mathbb E[M_t\mid\mathcal F_s]=M_s\\)",
        )
        parts[index] = segment
    return "".join(parts)


def _inject_style(text: str, rel: Path) -> str:
    prefix = "../" * len(rel.parent.parts)
    href = f"{prefix}assets/{STYLE_NAME}"
    if href in text:
        return text
    return text.replace(
        "</head>",
        f'  <link rel="stylesheet" href="{href}">\n</head>',
        1,
    )


def _source_card_for_id(text: str, source_id: str) -> str | None:
    escaped_id = re.escape(base.esc(source_id))
    pattern = re.compile(
        rf'<section class="[^"]*\bsource-passage\b[^"]*"[^>]*'
        rf'data-source-id="{escaped_id}"[^>]*>.*?</section>',
        flags=re.S,
    )
    match = pattern.search(text)
    return match.group(0) if match else None


def _formula_coverage_errors(output: Path) -> list[str]:
    """Require one displayed mathematical statement for every stable source id."""
    errors: list[str] = []
    sources = _source_entries()
    page_cache: dict[str, tuple[Path, str]] = {}

    for source_id, source in sources.items():
        section = str(source.get("section", ""))
        if section not in FORMULA_FIRST_SECTIONS:
            continue
        if section not in page_cache:
            path = base.section_path(output, section)
            if not path.exists():
                errors.append(f"missing canonical formula-first section {section}")
                continue
            page_cache[section] = (path, path.read_text(encoding="utf-8"))
        path, text = page_cache[section]
        card = _source_card_for_id(text, source_id)
        if card is None:
            errors.append(
                f"{path.relative_to(output)}: missing stable source card {source_id}"
            )
            continue
        if "source-formula" not in card:
            errors.append(
                f"{path.relative_to(output)}: source card {source_id} has no displayed formula"
            )

    return errors


def _proof_coverage_errors(output: Path) -> list[str]:
    errors: list[str] = []
    sources = _source_entries()
    proofs = _proof_supplements()
    for source_id, proof in proofs.items():
        source = sources.get(source_id)
        if source is None:
            continue
        section = str(source.get("section", ""))
        path = base.section_path(output, section)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        marker = f'data-source-proof="{base.esc(source_id)}"'
        if marker not in text:
            errors.append(f"{path.relative_to(output)}: missing equation proof {source_id}")
        expected_steps = len(
            [
                step
                for step in proof.get("steps", [])
                if isinstance(step, dict) and step.get("formula")
            ]
        )
        if expected_steps and text.count(marker) != 1:
            errors.append(f"{path.relative_to(output)}: duplicate or missing proof marker {source_id}")
    return errors


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    if DIAGNOSTIC.exists():
        DIAGNOSTIC.unlink()
    try:
        _patch_base_gate()
        _remove_undergrad_ladders(output)
        base.enrich_site(output)

        _inject_formula_supplements(output)
        _tag_all_source_cards(output)
        _move_existing_source_formulas_before_prose(output)

        asset_dir = output / "assets"
        asset_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE_CSS, asset_dir / STYLE_NAME)

        for path in sorted(output.rglob("*.html")):
            rel = path.relative_to(output)
            text = path.read_text(encoding="utf-8")
            text = _collapse_supplemental_details(text)
            text = _repair_exact_public_leaks(text)
            text = _inject_style(text, rel)
            path.write_text(text, encoding="utf-8", newline="\n")

        validate(output)
    except Exception as exc:
        _write_diagnostic(f"{type(exc).__name__}: {exc}")
        raise


def validate(output: Path = DEFAULT_OUTPUT) -> None:
    _patch_base_gate()
    try:
        base.validate(output)

        errors: list[str] = []
        css = output / "assets" / STYLE_NAME
        if not css.exists():
            errors.append(f"missing assets/{STYLE_NAME}")

        errors.extend(_formula_coverage_errors(output))
        errors.extend(_proof_coverage_errors(output))

        for path in output.rglob("*.html"):
            rel = path.relative_to(output)
            text = path.read_text(encoding="utf-8")
            errors.extend(validate_page(rel, text))
            prefix = "../" * len(rel.parent.parts)
            if f"{prefix}assets/{STYLE_NAME}" not in text:
                errors.append(f"{rel}: final reader stylesheet missing")

        if errors:
            raise RuntimeError("final reader contract failed:\n- " + "\n- ".join(errors))
    except Exception as exc:
        _write_diagnostic(f"{type(exc).__name__}: {exc}")
        raise


if __name__ == "__main__":
    enrich_site()
