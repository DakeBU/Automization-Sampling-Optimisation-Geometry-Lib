"""Reader integration for audited data constructions, never theorem coverage."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import astis_site as base
import inline_lean
import metadata_reader
import source_lineage

ROOT = Path(__file__).resolve().parents[2]


def lesson_path(name: str) -> str:
    from declaration_lessons import lesson_path as math_path
    return math_path(name).replace('lessons/', 'data-readers/', 1)


@lru_cache(maxsize=1)
def report() -> dict:
    manifest = json.loads((ROOT / 'website/content/metadata_reader/manifest.json').read_text(encoding='utf-8'))
    reader = metadata_reader.MetadataReader(
        manifest, (ROOT / manifest['audit_path']).read_bytes(),
        {p: (ROOT / p).read_bytes() for p in manifest['source_sha256']},
        list(inline_lean.declarations().values()),
    )
    return reader.explain_all()


def coverage_rows() -> dict:
    return {u['declaration']: {
        'exposition': 'data-explained' if u['resolution'] == 'resolved' else 'data-unresolved',
        'page': lesson_path(u['declaration']),
    } for u in report()['lessons']}


def public_ledger(data: dict) -> dict:
    """The entire exported ledger is deterministic, not only its totals."""
    return {
        'reader_version': data['reader_version'], 'audited': data['audited'],
        'explained': data['explained'], 'unresolved': data['unresolved'],
        'mathematical_proofs_added': 0,
        'declarations': [{'declaration': u['declaration'], 'resolution': u['resolution'], 'reason': u.get('reason'), 'page': lesson_path(u['declaration'])} for u in data['lessons']],
    }


def render_unit(unit: dict, page: str) -> str:
    name = unit['declaration']
    declaration = inline_lean.declarations()[name]
    body = metadata_reader.render_html(unit)
    body = body.replace('<h3>' + base.esc(name) + '</h3>', '<h1>' + base.esc(name) + '</h1>', 1)
    lead = '<h2>Meaning and type</h2><p>The result has data type <code>' + base.esc(unit['result_type']) + '</code>. A value of this type stores descriptions; it is not a proof of the statements in those descriptions.</p>'
    if unit['lean_source'] is not None:
        signature, _ = inline_lean.split_statement(unit['lean_source'])
        lead += '<details class="inline-lean inline-lean-statement"><summary>Lean statement of this data definition</summary><p>The part after the colon is the output data type. This declaration takes no mathematical proof inputs.</p>' + base.code_html(signature) + '</details>'
    else:
        lead += '<p>Exact-source disclosure is withheld because the existing declaration contains a machine-specific absolute path. This is an explicit unresolved documentation boundary; no sanitized excerpt is presented as exact.</p>'
    lead += '<h2>Construction and field-by-field explanation</h2>'
    body = body.replace('<p>' + base.esc(unit['summary']) + '</p>', lead + '<p>' + base.esc(unit['summary']) + '</p>', 1)
    if unit['lean_source'] is not None:
        old = '<pre><code class="language-lean">' + base.esc(unit['lean_source']) + '</code></pre>'
        body = body.replace(old, '<p>Each field assignment stores the corresponding value shown above. Omitted fields use the explicitly identified schema defaults. Strings that name theorems remain strings; they do not call those theorems.</p>' + base.code_html(unit['lean_source']))
    # The stable module anchor is a local declaration identity, not a new leaf.
    body += '<p><a href="../' + base.declaration_path(declaration) + '">Existing module entry</a> · <a href="index.html">Audited data-reader index</a> · <a href="../lessons/index.html">All teaching coverage</a></p>'
    return body


def enrich_site(output: Path) -> None:
    data = report()
    table = []
    module_jumps = {}
    for unit in data['lessons']:
        rel = lesson_path(unit['declaration'])
        text = base.page('Data construction: ' + unit['declaration'].rsplit('.', 1)[-1], rel, render_unit(unit, rel), extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')
        base.write_page(output, rel, source_lineage.canonical_shell(text, rel, output))
        table.append('<tr><td><a href="../' + rel + '"><code>' + base.esc(unit['declaration']) + '</code></a></td><td>' + base.esc(unit['resolution']) + '</td><td>' + base.esc(unit.get('reason') or 'Field values and defaults explained; no mathematical proof claimed.') + '</td></tr>')
        declaration = inline_lean.declarations()[unit['declaration']]
        module_jumps.setdefault(declaration.module, {})[declaration.anchor] = rel
    # One read/write per module, not one rewrite of the large SALD page for
    # each of its thousand data records.
    for module, jumps in module_jumps.items():
        module_path = output / ('modules/' + base.slugify(module) + '.html')
        text = module_path.read_text(encoding='utf-8')
        seen = set()
        def link(match):
            anchor = match[1]
            if anchor not in jumps:
                return match[0]
            seen.add(anchor)
            return match[0] + '<p><a href="../' + jumps[anchor] + '">Read what this data definition stores (not a mathematical proof)</a></p>'
        text = re.sub(r'<details class="declaration" id="([^"]+)">.*?</summary>', link, text, flags=re.S)
        if seen != jumps.keys():
            raise ValueError('Missing metadata declaration anchors in ' + module)
        module_path.write_text(text, encoding='utf-8')
    body = '<h1>Provenance and workflow data: reading the Lean constructions</h1><p>' + str(data['explained']) + ' of ' + str(data['audited']) + ' audited definitions have a syntax-exact field-by-field explanation. ' + str(data['unresolved']) + ' remain explicitly unresolved. These are not new mathematical proofs, and do not increase the Registry.</p><p>Unknown computations are not guessed or evaluated. Data references stay symbolic; stored proof-status labels and dependency names are not compilation or dependency evidence.</p><table><thead><tr><th>Definition</th><th>Reader status</th><th>Boundary</th></tr></thead><tbody>' + ''.join(table) + '</tbody></table>'
    rel = 'data-readers/index.html'
    base.write_page(output, rel, source_lineage.canonical_shell(base.page('Data construction readers', rel, body), rel, output))
    # Do not export source-bearing audit records or machine paths to site JSON.
    (output / 'data/metadata-exposition.json').write_text(json.dumps(public_ledger(data), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def validate_site(output: Path) -> list[str]:
    errors = []
    data = report()
    path = output / 'data/metadata-exposition.json'
    if not path.is_file():
        return ['Missing data-reader exposition ledger']
    actual = json.loads(path.read_text(encoding='utf-8'))
    if actual != public_ledger(data):
        errors.append('Data-reader ledger drift (version, identities, order, resolution, reason or page)')
    for unit in data['lessons']:
        path = output / lesson_path(unit['declaration'])
        if not path.is_file():
            errors.append('Missing data-reader page: ' + unit['declaration'])
            continue
        text = path.read_text(encoding='utf-8')
        if render_unit(unit, lesson_path(unit['declaration'])) not in text:
            errors.append('Data-reader exact construction/source drift: ' + unit['declaration'])
        if metadata_reader.BOUNDARY not in text:
            errors.append('Missing data-not-proof boundary: ' + unit['declaration'])
        if unit['resolution'] == 'resolved' and ('Lean statement of this data definition' not in text or 'Exact Lean data construction' not in text):
            errors.append('Missing adjacent data-source folds: ' + unit['declaration'])
    return errors
