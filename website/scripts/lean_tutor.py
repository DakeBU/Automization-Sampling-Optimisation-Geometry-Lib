#!/usr/bin/env python3
"""Inject beginner-facing Lean learning tools into generated declaration pages.

This layer is deliberately pedagogical. It never changes theorem status,
Registry ownership, source correspondence, or Chapter 1 completion evidence.
It makes already-generated Lean declarations easier to read at two levels:

* dedicated theorem/declaration cards receive reading-depth controls, a source-
  derived proof tree/network, line-by-line explanations, and a syntax glossary;
* bottom-level declarations that only live at module anchors receive a compact
  on-demand Lean tutor. If no Registry graph evidence exists, no graph edge is
  invented merely for presentation.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from math_first_reader import CJK_RE


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
START = "<!-- ASTIS_LEAN_TUTOR_START -->"
END = "<!-- ASTIS_LEAN_TUTOR_END -->"


def rel_asset(page: Path, output: Path, filename: str) -> str:
    target = output / "assets" / filename
    return os.path.relpath(target, page.parent).replace(os.sep, "/")


def studio_html() -> str:
    return f"""{START}
<section class="lean-learning-studio" data-lean-studio>
  <header>
    <div>
      <span class="studio-kicker">Lean learning studio · mathematics → formal proof</span>
      <h2>Read the mathematics first, then descend into Lean</h2>
      <p>You do not need to know Lean before opening this panel. The page keeps the paper-level theorem, rigorous proof obligations, exact Lean declaration, and proof dependencies as separate layers so a first-time reader can move down one layer at a time.</p>
    </div>
  </header>

  <div class="reading-mode-strip" role="group" aria-label="Reading depth">
    <button class="mode-button active" type="button" data-reading-mode="beginner" aria-pressed="true">Beginner</button>
    <button class="mode-button" type="button" data-reading-mode="rigorous" aria-pressed="false">Rigorous</button>
    <button class="mode-button" type="button" data-reading-mode="lean" aria-pressed="false">Lean learner</button>
  </div>
  <div class="mode-explanation">
    <div><strong>Beginner</strong><span>Why this theorem exists → intuition → statement → one hand calculation. Hide proof-engineering detail.</span></div>
    <div><strong>Rigorous</strong><span>Expose assumptions, hidden measure/limit/domain issues, proof route, and rigorous references.</span></div>
    <div><strong>Lean learner</strong><span>Open the exact declaration, proof tree/network, syntax glossary, and line-by-line explanation.</span></div>
  </div>

  <div class="lean-studio-workbench">
    <section class="lean-graph-section">
      <h3>Proof architecture</h3>
      <p class="lean-studio-intro">Start with the tree when learning: prerequisites sit below the theorem and downstream results sit above it. Switch to the network when you want to understand where this declaration lives in the local formal library. Every mapped node is clickable.</p>
      <div class="graph-toolbar">
        <div class="graph-mode-strip" role="group" aria-label="Lean graph mode">
          <button class="graph-mode-button active" type="button" data-graph-mode="tree" aria-pressed="true">Proof tree</button>
          <button class="graph-mode-button" type="button" data-graph-mode="network" aria-pressed="false">Dependency network</button>
        </div>
        <div class="lean-graph-stats" data-lean-graph-stats></div>
      </div>
      <div class="lean-graph-frame" data-lean-graph-canvas>
        <div class="note">Loading source-derived dependency evidence…</div>
      </div>
      <p class="lean-graph-stats">Graph rule: only dependencies found by the ASTIS source scan are drawn. Missing tactic indirection is treated as an under-approximation; the site never invents an edge just to make a prettier graph.</p>
    </section>

    <section class="lean-tutor-section">
      <h3>How to read the exact Lean declaration</h3>
      <p class="lean-studio-intro">Read a Lean theorem left-to-right exactly as you would unpack a mathematical sentence: name → ambient types → automatically inferred structures → explicit hypotheses → conclusion → proof. Then read the proof top-to-bottom as transformations of the current goal.</p>
      <ol class="lean-reading-recipe">
        <li><strong>Name</strong><span>What reusable mathematical fact is being created?</span></li>
        <li><strong>Parameters</strong><span>Which symbols are arbitrary, and which structures are inferred by typeclass search?</span></li>
        <li><strong>Proposition</strong><span>After the colon, translate the Lean expression back into a paper statement.</span></li>
        <li><strong>Proof actions</strong><span>After <code>by</code>, ask what each tactic does to the mathematical goal—not only what syntax it uses.</span></li>
      </ol>
      <div class="lean-line-tutor" data-lean-line-tutor></div>
    </section>

    <section class="lean-tutor-section">
      <h3>Syntax used on this page</h3>
      <p class="lean-studio-intro">This glossary is filtered to syntax that actually occurs in the declaration above. Open a symbol only when you meet it, rather than memorizing Lean grammar in advance.</p>
      <div class="lean-syntax-glossary" data-lean-glossary></div>
    </section>

    <section class="note source-voice-policy">
      <h3>Source voice and ASTIS voice stay separate</h3>
      <p>When Samplinglib shows a short quotation from Chewi, it is labeled as a source excerpt and linked to the canonical book page. Intuition, expanded proof steps, hidden regularity assumptions, and Lean explanations are ASTIS-authored commentary. A quotation never substitutes for a formal proof, and an ASTIS explanation is never attributed to the textbook author.</p>
    </section>
  </div>
</section>
{END}"""


def strip_existing(text: str) -> str:
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    return pattern.sub("", text)


def dedicated_pages(output: Path) -> list[Path]:
    pages = sorted((output / "theorems").glob("*.html"))
    pages.extend(
        path
        for path in sorted((output / "declarations").glob("*.html"))
        if path.name != "index.html"
    )
    return pages


def module_pages(output: Path) -> list[Path]:
    return sorted((output / "modules").glob("*.html"))


def remove_asset(text: str, filename: str, tag: str) -> str:
    if tag == "link":
        pattern = rf'\n?\s*<link rel="stylesheet" href="[^"]*{re.escape(filename)}">'
    else:
        pattern = rf'\n?\s*<script defer src="[^"]*{re.escape(filename)}"></script>'
    return re.sub(pattern, "", text)


def inject_assets(text: str, path: Path, output: Path, *, script: str) -> str:
    css = rel_asset(path, output, "lean-tutor.css")
    js = rel_asset(path, output, script)
    text = remove_asset(text, "lean-tutor.css", "link")
    text = remove_asset(text, script, "script")
    text = text.replace("</head>", f'  <link rel="stylesheet" href="{css}">\n</head>', 1)
    text = text.replace("</body>", f'  <script defer src="{js}"></script>\n</body>', 1)
    return text


def enrich_dedicated_page(path: Path, output: Path) -> bool:
    text = strip_existing(path.read_text(encoding="utf-8"))
    if "<h2>Lean statement</h2>" not in text:
        return False
    text = inject_assets(text, path, output, script="lean-tutor.js")
    text = text.replace(
        "<h2>Lean statement</h2>",
        studio_html() + "\n    <h2>Lean statement</h2>",
        1,
    )
    path.write_text(text, encoding="utf-8")
    return True


def enrich_module_page(path: Path, output: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if 'class="declaration"' not in text:
        return False
    text = inject_assets(text, path, output, script="module-lean-tutor.js")
    path.write_text(text, encoding="utf-8")
    return True


def enrich_site(output: Path = DEFAULT_OUTPUT) -> int:
    required = (
        "lean-tutor.css",
        "lean-tutor.js",
        "module-lean-tutor.js",
        "module-lean-tutor.css",
    )
    for asset in required:
        if not (output / "assets" / asset).exists():
            raise RuntimeError(f"Lean tutor asset must be copied before enrichment: {asset}")
    changed = 0
    for path in dedicated_pages(output):
        changed += int(enrich_dedicated_page(path, output))
    for path in module_pages(output):
        changed += int(enrich_module_page(path, output))
    return changed


def validate_site(output: Path = DEFAULT_OUTPUT) -> list[str]:
    errors: list[str] = []
    for asset in (
        "lean-tutor.css",
        "lean-tutor.js",
        "module-lean-tutor.js",
        "module-lean-tutor.css",
    ):
        path = output / "assets" / asset
        if not path.exists():
            errors.append(f"generated assets/{asset} is missing")
        elif asset.endswith(".js") and CJK_RE.search(path.read_text(encoding="utf-8")):
            errors.append(f"assets/{asset}: Lean tutor explanations must be English")

    eligible = 0
    for path in dedicated_pages(output):
        text = path.read_text(encoding="utf-8")
        if "<h2>Lean statement</h2>" not in text:
            continue
        eligible += 1
        checks = (
            (text.count(START) == 1 and text.count(END) == 1, "Lean learning studio marker"),
            ('data-reading-mode="beginner"' in text, "beginner reading mode"),
            ('data-reading-mode="rigorous"' in text, "rigorous reading mode"),
            ('data-reading-mode="lean"' in text, "Lean learner reading mode"),
            ('data-graph-mode="tree"' in text, "proof-tree control"),
            ('data-graph-mode="network"' in text, "dependency-network control"),
            ('data-lean-line-tutor' in text, "line-by-line Lean tutor"),
            ('data-lean-glossary' in text, "Lean syntax glossary"),
            ("lean-tutor.css" in text, "Lean tutor stylesheet"),
            ("lean-tutor.js" in text, "Lean tutor script"),
        )
        for passed, label in checks:
            if not passed:
                errors.append(f"{path}: missing {label}")
    if not eligible:
        errors.append("no theorem/declaration page with a Lean statement was enriched")

    module_eligible = 0
    for path in module_pages(output):
        text = path.read_text(encoding="utf-8")
        if 'class="declaration"' not in text:
            continue
        module_eligible += 1
        if "lean-tutor.css" not in text:
            errors.append(f"{path}: module declaration page missing Lean tutor stylesheet")
        if "module-lean-tutor.js" not in text:
            errors.append(f"{path}: module declaration page missing compact Lean tutor script")
    if not module_eligible:
        errors.append("no module declaration page was enriched with compact Lean tutoring")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if args.check:
        errors = validate_site(output)
        for error in errors:
            print(f"ERROR: {error}")
        return 1 if errors else 0
    changed = enrich_site(output)
    print(f"Injected Lean learning tools into {changed} declaration/module page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
