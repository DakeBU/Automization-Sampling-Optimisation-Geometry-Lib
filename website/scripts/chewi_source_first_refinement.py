#!/usr/bin/env python3
"""Refine the source-first reader before its final rendering pass.

The public textbook should contain a great deal of mathematics without turning
into a formula dump.  This pass therefore enforces two independent contracts:

* source results read in the order Statement -> Proof / derivation -> assumptions
  -> folded strict ASTIS LaTeX -> folded Lean; and
* ordinary reader prose never contains ASCII mathematics that should have been
  rendered by MathJax.

Audit-only metadata is never copied into the textbook merely because it exists
in ``source_correspondence.json``.  Conversely, once a source card is visible,
its mathematical statement is mandatory and formula-first.
"""

from __future__ import annotations

from html.parser import HTMLParser
import re
from pathlib import Path
from typing import Any


INLINE_REPLACEMENTS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\btau_m\s*<=\s*tau_n\b"), r"\(\tau_m\le\tau_n\)"),
    (re.compile(r"\bt\s*->\s*A_t\b"), r"\(t\mapsto A_t\)"),
    (re.compile(r"\bc\s*>=\s*0\b"), r"\(c\ge 0\)"),
    (re.compile(r"\bL2\(Omega\)\b"), r"\(L^2(\Omega)\)"),
    (re.compile(r"\bL2\b"), r"\(L^2\)"),
    (re.compile(r"\[0,T\]"), r"\([0,T]\)"),
)

FORBIDDEN_READER_HEADINGS: tuple[str, ...] = (
    "<h3>Chewi statement</h3>",
    "<h3>Chewi proof / derivation</h3>",
    "<h3>Chewi proof status</h3>",
)

FORBIDDEN_INTERNAL_PROSE: tuple[str, ...] = (
    "Mathlib's predicate derives integrability from the fixed-point conditional-expectation law",
    "For s <= t, E[M_t | F_s] = M_s",
    "f(omega,t)=|eta_t(omega)|^2",
)

SKIP_TAGS = {"pre", "code", "script", "style"}
INLINE_MATH_RE = re.compile(r"\\\(.*?\\\)", re.S)
DISPLAY_MATH_RE = re.compile(r"\\\[.*?\\\]", re.S)
# The shared math-reader.js also configures $...$ and $$...$$. Ignore only
# complete, unescaped pairs; unmatched/escaped delimiters still expose raw prose.
# Escaped characters inside math are one token; even backslash runs before
# an opening dollar leave that delimiter unescaped, as in the reader runtime.
DOLLAR_INLINE_MATH_RE = re.compile(
    r"(?<![\\$])(?:\\\\)*\$(?!\$)(?:\\.|[^\\$])*\$(?!\$)", re.S
)
DOLLAR_DISPLAY_MATH_RE = re.compile(
    r"(?<!\\)(?:\\\\)*\$\$(?:\\.|[^\\$]|\$(?!\$))*\$\$", re.S
)


def mathify(value: object) -> str:
    """Convert the few legacy mixed prose clauses that are intentionally kept.

    This is not a general TeX parser.  Long mathematical claims belong in a
    dedicated displayed formula; this helper is only for short assumptions.
    """

    text = str(value)
    for pattern, replacement in INLINE_REPLACEMENTS:
        text = pattern.sub(lambda _m, replacement=replacement: replacement, text)
    return text


def neutralize_reader_headings(text: str) -> str:
    return (
        text
        .replace("<h3>Chewi statement</h3>", "<h3>Statement</h3>")
        .replace(
            "<h3>Chewi proof / derivation</h3>",
            "<h3>Proof / derivation</h3>",
        )
        .replace(
            "<h3>Chewi proof status</h3>",
            "<h3>Proof / derivation status</h3>",
        )
    )


class _VisibleMathScanner(HTMLParser):
    """Lint visible prose while remembering the nearest mathematical card id."""

    def __init__(self, contract: Any) -> None:
        super().__init__(convert_charrefs=True)
        self.contract = contract
        self.frames: list[tuple[str, bool, str]] = []
        self.skip_depth = 0
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: (value or "") for key, value in attrs}
        classes = set(values.get("class", "").split())
        inherited = self.frames[-1][2] if self.frames else "page"
        context = values.get("data-source-id") or values.get("id") or inherited
        skip = tag.lower() in SKIP_TAGS or "formula" in classes
        self.frames.append((tag.lower(), skip, context))
        if skip:
            self.skip_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        target = tag.lower()
        if not self.frames:
            return
        # Generated HTML is well nested, but recover gracefully from a malformed
        # fragment so the linter itself never hides the original site error.
        index = len(self.frames) - 1
        while index >= 0 and self.frames[index][0] != target:
            index -= 1
        if index < 0:
            return
        removed = self.frames[index:]
        del self.frames[index:]
        self.skip_depth -= sum(1 for _tag, skip, _context in removed if skip)
        self.skip_depth = max(self.skip_depth, 0)

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        visible = INLINE_MATH_RE.sub(" ", data)
        visible = DISPLAY_MATH_RE.sub(" ", visible)
        visible = DOLLAR_DISPLAY_MATH_RE.sub(" ", visible)
        visible = DOLLAR_INLINE_MATH_RE.sub(" ", visible)
        if not visible.strip():
            return
        context = self.frames[-1][2] if self.frames else "page"
        tag = self.frames[-1][0] if self.frames else "text"
        for pattern, label in self.contract.RAW_MATH_PATTERNS:
            match = pattern.search(visible)
            if not match:
                continue
            start = max(0, match.start() - 70)
            stop = min(len(visible), match.end() + 90)
            snippet = " ".join(visible[start:stop].split())
            self.errors.append(
                f"[{context}] <{tag}> {label}: {snippet!r}"
            )


def _scan_visible_math(contract: Any, text: str) -> list[str]:
    scanner = _VisibleMathScanner(contract)
    scanner.feed(text)
    scanner.close()
    return scanner.errors


def patch(contract: Any) -> None:
    if getattr(contract, "_neutral_heading_refinement_applied", False):
        return

    original_render_source_card = contract._render_source_card
    original_inject_style = contract._inject_style

    def render_mixed_list(values: list[str], css_class: str = "") -> str:
        cls = f' class="{css_class}"' if css_class else ""
        return (
            "<ul" + cls + ">"
            + "".join(f"<li>{contract.esc(mathify(value))}</li>" for value in values)
            + "</ul>"
        )

    def render_hidden_assumptions(source: dict[str, Any]) -> str:
        source_assumptions = [
            str(x) for x in source.get("source_assumptions", []) if str(x).strip()
        ]
        formal_assumptions = [
            str(x) for x in source.get("formal_assumptions", []) if str(x).strip()
        ]
        parts = [
            '<div class="source-contract-hidden-assumptions">',
            '<h3>Assumptions and implicit prerequisites</h3>',
        ]
        if source_assumptions:
            parts.append(
                '<h4>Source-level assumptions</h4>'
                + render_mixed_list(source_assumptions)
            )
        if formal_assumptions:
            parts.append(
                '<h4>Conditions made explicit by ASTIS</h4>'
                + contract._code_list(formal_assumptions)
            )
        parts.append('</div>')
        return "".join(parts)

    def render_astis_latex(
        source_id: str,
        source: dict[str, Any],
        statement: str,
        proof: dict[str, Any] | None,
    ) -> str:
        equations = contract._render_equations(
            proof, "astis-rigorous-proof-formula"
        )
        source_status = str(proof.get("source_status", "")) if proof else ""
        if source_status == "astis_expansion":
            proof_note = (
                "The equations below are the ASTIS expansion of a proof omitted "
                "or compressed in the source."
            )
        elif equations:
            proof_note = (
                "The source argument is restated here as a strict ASTIS LaTeX "
                "packet before the Lean correspondence."
            )
        else:
            proof_note = (
                "This packet records the strict ASTIS statement. No additional "
                "proof is attributed to the source."
            )
        return (
            '<details class="reader-disclosure source-contract-astis-latex">'
            '<summary>ASTIS rigorous LaTeX formalization</summary>'
            '<div class="disclosure-body">'
            f'<p>{contract.esc(proof_note)}</p>'
            f'{contract._display_math(statement, "astis-rigorous-statement")}'
            + equations
            + '</div></details>'
        )

    def render_implicit_card(item: dict[str, Any], url_map: dict[str, str]) -> str:
        item_id = str(item.get("id", ""))
        proof = contract.IMPLICIT_PROOF_OVERRIDES.get(item_id)
        raw_proof = str(item.get("proof", ""))
        if proof is None:
            if contract._raw_math_errors(raw_proof):
                raise RuntimeError(
                    f"{item_id}: implicit-prerequisite proof contains raw mathematics "
                    "and has no clean proof override"
                )
            proof = raw_proof
        assumptions = [
            str(x) for x in item.get("assumptions", []) if str(x).strip()
        ]
        declarations = [
            str(x) for x in item.get("lean_declarations", []) if str(x).strip()
        ]
        lean_rows: list[str] = []
        for name in declarations:
            url = url_map.get(name)
            if url:
                lean_rows.append(
                    f'<li><a href="../../{contract.esc(url)}">'
                    f'<code>{contract.esc(name)}</code></a></li>'
                )
            else:
                lean_rows.append(f'<li><code>{contract.esc(name)}</code></li>')
        return (
            '<article class="textbook-block implicit-prerequisite-card '
            'source-contract-implicit" '
            f'id="{contract.esc(item_id)}" '
            'data-provenance="astis-implicit-prerequisite">'
            '<div class="passage-label">ASTIS implicit prerequisite · not a '
            'standalone source result</div>'
            f'<h2>{contract.esc(item.get("title", ""))}</h2>'
            '<p><strong>Why it is needed.</strong> '
            f'{contract.esc(mathify(item.get("why_needed", "")))}</p>'
            f'{contract._display_math(str(item.get("latex_statement", "")), "implicit-prerequisite-statement")}'
            '<h3>Assumptions</h3>'
            f'{render_mixed_list(assumptions)}'
            '<details class="reader-disclosure source-contract-implicit-proof">'
            '<summary>Mathematical proof</summary><div class="disclosure-body">'
            f'<p>{contract.esc(mathify(proof))}</p></div></details>'
            '<details class="reader-disclosure source-contract-lean">'
            '<summary>Lean formalization</summary><div class="disclosure-body"><ul>'
            + ''.join(lean_rows)
            + '</ul></div></details>'
            '</article>'
        )

    def render_source_card(
        source_id: str,
        source: dict[str, Any],
        supplements: dict[str, dict[str, Any]],
        proofs: dict[str, dict[str, Any]],
        url_map: dict[str, str],
    ) -> str:
        rendered = original_render_source_card(
            source_id, source, supplements, proofs, url_map
        )
        return neutralize_reader_headings(rendered)

    def replace_source_cards(output: Path) -> None:
        """Rebuild every source card that is actually reader-facing.

        ``source_correspondence.json`` also contains audit/roadmap rows for later
        chapters that are not yet emitted as textbook cards.  Those rows must not
        make a presentation pass fail merely because they are metadata.  The
        instant a card is visible (stable id, or an old exact source anchor), it
        is rebuilt under this contract and becomes subject to all validators.
        """

        sources = contract._by_id(contract.SOURCE_CORRESPONDENCE)
        supplements = contract._by_id(contract.FORMULA_SUPPLEMENTS)
        proofs = contract._by_id(contract.PROOF_SUPPLEMENTS)
        url_map = contract._declaration_url_map(output)
        grouped: dict[str, list[tuple[str, dict[str, Any]]]] = {}
        for source_id, source in sources.items():
            grouped.setdefault(str(source.get("section", "")), []).append(
                (source_id, source)
            )

        rendered_ids: set[str] = set()
        errors: list[str] = []
        for section, entries in grouped.items():
            try:
                path = contract.base.section_path(output, section)
            except Exception:
                continue
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8")
            for source_id, source in entries:
                stable = re.compile(
                    rf'<section class="[^"]*\bsource-passage\b[^"]*"[^>]*'
                    rf'data-source-id="{re.escape(contract.esc(source_id))}"[^>]*>.*?</section>',
                    flags=re.S,
                )
                matches = list(stable.finditer(text))
                if len(matches) > 1:
                    errors.append(
                        f"{path.relative_to(output)}: duplicate source card {source_id}"
                    )
                    continue
                if len(matches) == 1:
                    match = matches[0]
                    try:
                        replacement = render_source_card(
                            source_id, source, supplements, proofs, url_map
                        )
                    except RuntimeError as exc:
                        errors.append(
                            f"{path.relative_to(output)}: visible source card {source_id}: {exc}"
                        )
                        continue
                    text = text[:match.start()] + replacement + text[match.end():]
                    rendered_ids.add(source_id)
                    continue

                # Recover older, untagged source cards when the preceding reader
                # still emits the exact source anchor.  If a metadata row has no
                # reader card at all, leave it audit-only rather than fabricating
                # a new textbook result during a presentation pass.
                anchor = ""
                try:
                    anchor = contract.reader._source_anchor(source)
                except Exception:
                    pass
                start = text.find(anchor) if anchor else -1
                if start < 0:
                    continue
                close = text.find("</section>", start)
                if close < 0:
                    errors.append(
                        f"{path.relative_to(output)}: unterminated legacy source card {source_id}"
                    )
                    continue
                try:
                    replacement = render_source_card(
                        source_id, source, supplements, proofs, url_map
                    )
                except RuntimeError as exc:
                    errors.append(
                        f"{path.relative_to(output)}: visible source card {source_id}: {exc}"
                    )
                    continue
                text = text[:start] + replacement + text[close + len("</section>"):]
                rendered_ids.add(source_id)
            path.write_text(text, encoding="utf-8", newline="\n")

        contract._reader_facing_source_ids = rendered_ids
        if errors:
            raise RuntimeError(
                "reader-facing source-card reconstruction failed:\n- "
                + "\n- ".join(errors)
            )

    def inject_style(text: str, rel: Path) -> str:
        return neutralize_reader_headings(original_inject_style(text, rel))

    def validate(output: Path = contract.DEFAULT_OUTPUT) -> None:
        errors: list[str] = []
        proofs = contract._by_id(contract.PROOF_SUPPLEMENTS)

        for path in sorted(output.rglob("*.html")):
            text = path.read_text(encoding="utf-8")
            rel = path.relative_to(output)

            for heading in FORBIDDEN_READER_HEADINGS:
                if heading in text:
                    errors.append(
                        f"{rel}: author-prefixed reader heading remains: {heading}"
                    )
            for phrase in FORBIDDEN_INTERNAL_PROSE:
                if phrase in text:
                    errors.append(
                        f"{rel}: internal/ASCII exposition leaked into reader: {phrase!r}"
                    )

            # Every reconstructed source result must remain formula-first and
            # retain the exact pedagogical hierarchy requested by the reader.
            cards = re.finditer(
                r'<section class="[^"]*\bsource-contract-card\b[^"]*"[^>]*'
                r'data-source-id="([^"]+)"[^>]*>.*?</section>',
                text,
                flags=re.S,
            )
            for match in cards:
                source_id = match.group(1)
                card = match.group(0)
                statement_at = card.find("source-contract-chewi-statement")
                assumptions_at = card.find("source-contract-hidden-assumptions")
                astis_at = card.find("source-contract-astis-latex")
                lean_at = card.find("source-contract-lean")
                if min(statement_at, assumptions_at, astis_at, lean_at) < 0:
                    errors.append(f"{rel} [{source_id}]: incomplete source-card hierarchy")
                    continue
                if not (statement_at < assumptions_at < astis_at < lean_at):
                    errors.append(f"{rel} [{source_id}]: source-card hierarchy is out of order")
                formula_at = card.find("source-formula")
                summary_at = card.find("source-result-summary")
                if formula_at < 0:
                    errors.append(f"{rel} [{source_id}]: Statement has no displayed formula")
                if summary_at >= 0 and formula_at > summary_at:
                    errors.append(f"{rel} [{source_id}]: prose appears before the Statement formula")
                if '<details class="reader-disclosure source-contract-astis-latex" open' in card:
                    errors.append(f"{rel} [{source_id}]: strict ASTIS LaTeX must be folded")
                if '<details class="reader-disclosure source-contract-lean" open' in card:
                    errors.append(f"{rel} [{source_id}]: Lean formalization must be folded")
                proof = proofs.get(source_id)
                if proof and str(proof.get("source_status", "")) == "source_proof":
                    proof_at = card.find("source-contract-chewi-proof")
                    if proof_at < 0 or not (statement_at < proof_at < assumptions_at):
                        errors.append(
                            f"{rel} [{source_id}]: Proof / derivation is not immediately after Statement"
                        )
                    if "chewi-source-proof-formula" not in card:
                        errors.append(
                            f"{rel} [{source_id}]: audited proof route has no displayed equations"
                        )

            # Lint text node by text node, preserving the nearest card/section id
            # in the error. This avoids both giant page-level false positives and
            # silent mixed prose such as `For s <= t, M_t ...`.
            for issue in _scan_visible_math(contract, text):
                errors.append(f"{rel} {issue}")

        if errors:
            raise RuntimeError(
                "clear mathematical reader contract failed:\n- "
                + "\n- ".join(errors)
            )

    contract._render_hidden_assumptions = render_hidden_assumptions
    contract._render_astis_latex = render_astis_latex
    contract._render_implicit_card = render_implicit_card
    contract._render_source_card = render_source_card
    contract._replace_source_cards = replace_source_cards
    contract._inject_style = inject_style
    contract.validate = validate
    contract._neutral_heading_refinement_applied = True
