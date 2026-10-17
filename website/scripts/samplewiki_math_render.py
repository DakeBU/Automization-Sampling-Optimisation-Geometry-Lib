#!/usr/bin/env python3
"""Finalize the reader-facing SampleWiki presentation.

The pinned case manifest stores browser-visible comparison-row text. KaTeX
extraction leaves a human rendering, the embedded TeX source, then another
human rendering. This pass recovers the TeX for MathJax, preserves mathematical
qualifiers such as ``under LSI`` beside the formula, and inserts a persistent
SampleWiki directory after the global information-architecture pass.
"""

from __future__ import annotations

import html
import json
import posixpath
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
CASES_PATH = ROOT / "research-wiki" / "source-index" / "SampleWiki_cases.json"
OVERVIEW = "example-cases/samplewiki.html"
PROGRESS = "example-cases/samplewiki/progress.html"
FRONTIER = "example-cases/samplewiki/frontier.html"

EXPRESSION_RE = re.compile(
    r'<div class="sw-expression">'
    r'<span>(?P<label>.*?)</span>'
    r'<div>(?P<raw>.*?)</div></div>',
    flags=re.S,
)


def load_cases() -> dict[str, object]:
    raw = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise RuntimeError("SampleWiki_cases.json must contain an object")
    return raw


def href_from(current: str, target: str) -> str:
    start = posixpath.dirname(current) or "."
    return posixpath.relpath(target, start=start)


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower() or "setting"


def setting_path(setting_slug: str) -> str:
    return f"example-cases/samplewiki/settings/{slugify(setting_slug)}.html"


def is_samplewiki_page(rel_path: str) -> bool:
    return rel_path == OVERVIEW or rel_path.startswith("example-cases/samplewiki/")


def math_fragment(value: str) -> str:
    """Extract the first complete TeX fragment from KaTeX-derived row text."""
    first = value.find("\\")
    if first < 0:
        return ""

    start = first
    while start > 0 and not value[start - 1].isspace():
        start -= 1

    braces = parens = brackets = 0
    index = start
    saw_backslash = False
    operator_suffixes = (
        "\\le", "\\ge", "=", "<", ">", "+", "-", "\\sim", "\\to", "\\asymp"
    )
    argument_commands = {
        "\\widetilde",
        "\\mathcal",
        "\\mathrm",
        "\\mathbf",
        "\\sqrt",
    }
    while index < len(value):
        char = value[index]
        if char == "\\":
            saw_backslash = True
        elif char == "{":
            braces += 1
        elif char == "}":
            braces = max(0, braces - 1)
        elif char == "(":
            parens += 1
        elif char == ")":
            parens = max(0, parens - 1)
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets = max(0, brackets - 1)

        if saw_backslash and char.isspace() and braces == parens == brackets == 0:
            cursor = index
            while cursor < len(value) and value[cursor].isspace():
                cursor += 1
            current = value[start:index].strip()
            if current in argument_commands and cursor < len(value):
                index = cursor
                continue
            if current.endswith(operator_suffixes) and cursor < len(value):
                index = cursor
                continue
            return current
        index += 1
    return value[start:].strip()


def qualifier_fragments(raw: str) -> tuple[str, str]:
    """Keep source-row qualifiers that change the mathematical claim visible."""
    prefix = ""
    suffixes: list[str] = []
    lowered = raw.lower()

    if "tv accuracy proportional to" in lowered:
        prefix = "TV accuracy proportional to"
    if "under lsi" in lowered:
        suffixes.append("under LSI")
    if "on average" in lowered:
        suffixes.append("on average")
    if "in the same model" in lowered:
        suffixes.append("in the same model")
    if "\\varepsilon^2=\\beta d" in raw:
        suffixes.append("at ε² = β d")

    return prefix, "; ".join(suffixes)


def render_match(match: re.Match[str]) -> str:
    label = match.group("label")
    raw_html = match.group("raw")
    raw = html.unescape(re.sub(r"<[^>]+>", "", raw_html)).strip()
    latex = math_fragment(raw)
    if not latex:
        return match.group(0)
    if latex in {"\\mathcal", "\\widetilde", "\\mathrm", "\\mathbf", "\\sqrt"}:
        raise RuntimeError(f"incomplete SampleWiki TeX fragment: {latex!r} from {raw!r}")

    prefix, suffix = qualifier_fragments(raw)
    prefix_html = (
        f'<div class="sw-row-context sw-row-prefix">{html.escape(prefix)}</div>'
        if prefix
        else ""
    )
    suffix_html = (
        f'<div class="sw-row-context sw-row-suffix">{html.escape(suffix)}</div>'
        if suffix
        else ""
    )
    return (
        '<div class="sw-expression">'
        f'<span>{label}</span>'
        f'{prefix_html}'
        f'<div class="formula sw-row-formula">\\[{html.escape(latex, quote=True)}\\]</div>'
        f'{suffix_html}'
        '<details class="sw-raw-row"><summary>Raw pinned row text</summary>'
        f'<div>{html.escape(raw, quote=True)}</div></details></div>'
    )


def current_attr(current: str, target: str) -> str:
    return ' aria-current="page"' if current == target else ""


def sidebar_directory(rel_path: str, pages: list[dict[str, object]]) -> str:
    import samplewiki_navigation
    setting_links = []
    for page in pages:
        setting_slug = str(page.get("setting_slug", ""))
        target = setting_path(setting_slug)
        setting_links.append(
            f'<a href="{html.escape(href_from(rel_path, target), quote=True)}"'
            f'{current_attr(rel_path, target)}>{html.escape(str(page.get("setting_title", setting_slug)))}</a>'
        )
    return samplewiki_navigation.paper_directory(rel_path) + f"""
<section class="sidebar-group sw-sidebar-directory" data-samplewiki-directory="true">
  <nav>
    <a href="{html.escape(href_from(rel_path, PROGRESS), quote=True)}"{current_attr(rel_path, PROGRESS)}>Current progress</a>
  </nav>
  <details class="sw-sidebar-settings">
    <summary>By assumptions and guarantees</summary>
    <nav>{''.join(setting_links)}</nav>
  </details>
</section>
"""


def inject_directory(text: str, rel_path: str, pages: list[dict[str, object]]) -> str:
    if not is_samplewiki_page(rel_path):
        return text
    if 'data-samplewiki-directory="true"' in text:
        return text
    marker = '<details class="book-nav"'
    position = text.find(marker)
    if position < 0:
        raise RuntimeError(f"{rel_path}: global sidebar book marker missing")
    return text[:position] + sidebar_directory(rel_path, pages) + text[position:]


def enrich_site(output: Path = DEFAULT_OUTPUT) -> None:
    cases = load_cases()
    pages = [dict(item) for item in cases.get("pages", []) if isinstance(item, dict)]

    converted = 0
    touched = 0
    for path in sorted((output / "example-cases").rglob("*.html")):
        rel_path = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        text, count = EXPRESSION_RE.subn(render_match, text)
        converted += count
        if is_samplewiki_page(rel_path):
            text = inject_directory(text, rel_path, pages)
            touched += 1
        path.write_text(text, encoding="utf-8", newline="\n")

    if converted == 0:
        raise RuntimeError("SampleWiki math renderer found no row expressions")
    if touched != 3 + len(pages) + int(cases.get("case_count", 0)):
        raise RuntimeError(
            f"SampleWiki directory touched {touched} pages; expected "
            f"{3 + len(pages) + int(cases.get('case_count', 0))}"
        )

    errors: list[str] = []
    rendered_pages: list[str] = []
    for path in sorted((output / "example-cases").rglob("*.html")):
        rel_path = path.relative_to(output).as_posix()
        text = path.read_text(encoding="utf-8")
        if is_samplewiki_page(rel_path):
            rendered_pages.append(text)
        for match in EXPRESSION_RE.finditer(text):
            raw = html.unescape(match.group("raw"))
            if "\\" in raw:
                errors.append(f"{rel_path}: TeX-bearing row expression was not converted")
                break
        if is_samplewiki_page(rel_path) and 'data-samplewiki-directory="true"' not in text:
            errors.append(f"{rel_path}: SampleWiki sidebar directory missing")

    # These qualifiers materially narrow the source claim and therefore must
    # remain in visible context nodes, not merely in the raw audit disclosure.
    corpus = "\n".join(rendered_pages)
    visible_qualifier_markers = (
        '>under LSI</div>',
        '>on average</div>',
        '>in the same model</div>',
        '>TV accuracy proportional to</div>',
        '>at ε² = β d</div>',
    )
    for marker in visible_qualifier_markers:
        if marker not in corpus:
            errors.append(f"SampleWiki visible material qualifier missing: {marker}")

    # Bare font/style commands are never complete row formulas.
    for command in (r"\\mathcal", r"\\widetilde", r"\\mathrm", r"\\mathbf", r"\\sqrt"):
        if f'\\[{command}\\]' in corpus:
            errors.append(f"SampleWiki bare TeX command leaked as formula: {command}")

    if errors:
        raise RuntimeError("SampleWiki presentation finalization failed:\n- " + "\n- ".join(errors))


if __name__ == "__main__":
    enrich_site()
