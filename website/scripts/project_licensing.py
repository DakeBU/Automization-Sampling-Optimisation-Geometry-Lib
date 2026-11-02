"""Publish the root license/notices without relicensing external source material."""
from __future__ import annotations

from html import escape
from pathlib import Path

import astis_site
import source_lineage

ROOT = Path(__file__).resolve().parents[2]
PAGE = 'licensing/index.html'
LICENSE_FILES = ('LICENSE', 'NOTICE', 'LICENSE_SCOPE.md', 'NOTICE.md')
MARKER = 'data-project-license="true"'


def add_to_archive(archive, root: Path = ROOT) -> None:
    """Every redistributable project-code bundle carries the exact root notices."""
    for name in LICENSE_FILES:
        archive.write(root / name, name)


def footer_link(text: str, rel: str) -> str:
    if MARKER in text or '</footer>' not in text:
        return text
    href = astis_site.relative_prefix(rel) + PAGE
    return text.replace('</footer>',
        f'<p {MARKER}><a href="{href}">Apache-2.0 · license and third-party notices</a></p></footer>')


def enrich_site(output: Path) -> None:
    target = output / 'licensing'
    target.mkdir(parents=True, exist_ok=True)
    for name in LICENSE_FILES:
        (target / name).write_bytes((ROOT / name).read_bytes())
    downloads = ' · '.join(f'<a href="{name}" download>{escape(name)}</a>' for name in LICENSE_FILES)
    license_text = escape((ROOT / 'LICENSE').read_text(encoding='utf-8'))
    body = f'''<section class="page-hero compact"><div class="eyebrow">Reuse and contribution</div>
<h1>License and reuse</h1><p class="lede">Samplinglib's original Lean library, tools, documentation and website exposition are available under Apache-2.0. Reuse, modification, redistribution and contributions are welcome.</p></section>
<section><h2>Apache License, Version 2.0</h2><p>Keep the license and applicable copyright/attribution notices, identify modified files and preserve applicable NOTICE material. The software is provided without warranty. Each contributor retains copyright; no transfer of third-party rights is asserted.</p>
<p>{downloads}</p><p><a href="https://www.apache.org/licenses/LICENSE-2.0">Official Apache-2.0 text</a> · <a href="../attribution/index.html">Mathematical and design attribution</a></p></section>
<section><h2>Existing Lean modules and historical reuse</h2><p>The grant includes project-original Analysis, FunctionalInequalities and Geometry modules, including their versions at revision <code>933dd38de9423d2967bc36b501b3a2006343000d</code>, subject to preserved third-party terms. This is permission granted now, not a claim that that historical tree already had a root license. Include the current license/notices when redistributing those versions.</p></section>
<section><h2>What this license does not cover</h2><p>Source textbooks and papers, quotations, figures, external repositories and dependencies retain their own licenses. The project does not grant permission to republish Chewi's textbook. Apache-licensed adaptations retain their upstream copyright, including Yuanhe Zhang's notices in the ported SLT modules.</p>
<p>The ATLAS-derived reference index and its copies/projections retain the pinned academic/research-only restrictions, including no commercial use or ML-model development. These restrictions do not extend to unrelated original Samplinglib code. Material without established upstream permission is not made reusable by our root license.</p>
<p><a href="LICENSE_SCOPE.md">Read the complete scope and exclusions</a>. Citation is appreciated, not an additional license requirement.</p></section>
<details><summary>Read the full, unmodified Apache-2.0 license</summary><pre><code class="language-text">{license_text}</code></pre></details>'''
    text = astis_site.page('License and reuse', PAGE, body)
    astis_site.write_page(output, PAGE, source_lineage.canonical_shell(text, PAGE, output))
    for rel in ('attribution.html', 'attribution/index.html'):
        path = output / rel
        if path.exists():
            link = astis_site.relative_prefix(rel) + PAGE
            source_lineage.append_main(output, rel,
                f'<section data-project-license-summary="true"><h2>Project license: Apache-2.0</h2><p>Original Samplinglib material is licensed under Apache-2.0; external material retains its own terms. <a href="{link}">License, historical reuse and third-party boundaries</a>.</p></section>',
                'data-project-license-summary="true"')
    for path in output.rglob('*.html'):
        original = path.read_text(encoding='utf-8')
        rendered = footer_link(original, path.relative_to(output).as_posix())
        if rendered != original:
            path.write_text(rendered, encoding='utf-8', newline='\n')


def validate_site(output: Path) -> list[str]:
    errors = []
    for name in LICENSE_FILES:
        exported = output / 'licensing' / name
        if not exported.is_file() or exported.read_bytes() != (ROOT / name).read_bytes():
            errors.append(f'License/notices missing or stale: {name}')
    if not (output / PAGE).is_file():
        errors.append('Missing public license and reuse page')
    for path in output.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if '</footer>' in text and MARKER not in text:
            errors.append(f'Missing license footer: {path.relative_to(output)}')
    return errors
