"""Authored declaration-level mathematics, with an exhaustive coverage ledger.

An exact Lean listing or a tactic glossary is not textbook-level exposition.
The ledger deliberately keeps every not-yet-authored declaration visible.
"""
from __future__ import annotations

import json
import hashlib
import re
from functools import lru_cache
from collections import Counter, defaultdict
from pathlib import Path

import astis_site as base
import inline_lean
import source_lineage

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'website/content/declaration_lessons'


@lru_cache(maxsize=1)
def mathlib_pin() -> str:
    manifest = json.loads((ROOT / 'lake-manifest.json').read_text(encoding='utf-8'))
    return next(p['rev'] for p in manifest['packages'] if p['name'] == 'mathlib')


def source_link(source: dict, page: str) -> str:
    """Resolve reviewed repository anchors without leaking local paths.

    Mathematics lives in metadata; exact Lean is always taken from the checkout.
    Local documents are copied into the same generated site for unpublished work.
    """
    if source.get('url'):
        if not source['url'].startswith('https://'):
            raise ValueError('Exposition sources must use HTTPS or a repository path')
        return source['url']
    raw = source['path']
    path = Path(raw)
    if raw.startswith(('/', '\\')) or '\\' in raw or path.is_absolute() or '..' in path.parts or re.match(r'^[A-Za-z]:', raw):
        raise ValueError(f'Nonportable exposition source: {raw}')
    if raw.startswith('.lake/packages/mathlib/'):
        path = raw.removeprefix('.lake/packages/mathlib/')
        return f'https://github.com/leanprover-community/mathlib4/blob/{mathlib_pin()}/{path}' + (f'#L{source["line"]}' if source.get('line') else '')
    return base.relative_prefix(page) + 'data/lesson-sources/' + path.as_posix() + '.html' + (f'#L{source["line"]}' if source.get('line') else '')


def inline_text(value: str) -> str:
    """Only inline code is interpreted; mathematical TeX remains for MathJax."""
    return ''.join('<code>' + base.esc(part) + '</code>' if i % 2 else base.esc(part)
                   for i, part in enumerate(re.split(r'`([^`]+)`', value)))


def export_sources(output: Path, units: list[dict]) -> None:
    exported = set()
    source_lines = {}
    for unit in units:
        for source in unit.get('sources', []):
            source_link(source, 'lessons/index.html')  # validate even external anchors
            raw = source.get('path', '')
            if not raw:
                continue
            path = ROOT / raw
            # Website-only CI has the repository but need not install Lean's
            # dependencies. External anchors remain pinned to lake-manifest;
            # this does not upgrade an absent Lean build to compiled status.
            if raw.startswith('.lake/packages/mathlib/') and not path.is_file():
                continue
            if not path.is_file():
                raise ValueError(f'Missing exposition source: {raw}')
            if raw not in source_lines:
                source_lines[raw] = path.read_text(encoding='utf-8').splitlines()
            lines = source_lines[raw]
            if source.get('line') and not 1 <= source['line'] <= len(lines):
                raise ValueError(f'Exposition source line out of range: {source}')
            if raw.startswith('.lake/packages/mathlib/') or raw in exported:
                continue
            exported.add(raw)
            # The exact source excerpt remains readable without leaving the site.
            rel = 'data/lesson-sources/' + raw
            numbered = ''.join(f'<span id="L{i}">{base.esc(line)}</span>\n' for i, line in enumerate(lines, 1))
            target = output / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            # Keep .lean/.md anchors as HTML companion documents, not MIME-dependent files.
            text = base.page(raw, rel + '.html', '<h1>Exact source context</h1><pre>' + numbered + '</pre>')
            target.with_suffix(target.suffix + '.html').write_text(source_lineage.canonical_shell(text, rel + '.html', output), encoding='utf-8')


def load_units() -> list[dict]:
    units = []
    for path in sorted(CONTENT.glob('*.json')):
        raw = json.loads(path.read_text(encoding='utf-8'))
        units.extend(raw['units'] if isinstance(raw, dict) else raw)
    names = set()
    for unit in units:
        name = unit['declaration']
        if name in names:
            raise ValueError(f'Duplicate authored lesson: {name}')
        names.add(name)
        for key in ('kind', 'title', 'statement', 'formula', 'assumptions', 'steps',
                    'lean_statement', 'lean_proof', 'boundary'):
            if not unit.get(key):
                raise ValueError(f'{name}: missing authored {key}')
        for step in unit['steps']:
            if not all(step.get(k) for k in ('title', 'text', 'formula', 'lean')):
                raise ValueError(f'{name}: incomplete mathematical proof step')
    return units


def lesson_path(name: str) -> str:
    # Lean identifiers are case sensitive; slugify is not. In particular the
    # DV interface type and its constructor have otherwise identical URLs.
    suffix = hashlib.sha256(name.encode('utf-8')).hexdigest()[:12]
    return f'lessons/{base.slugify(name)[:160]}-{suffix}.html'


def validate_projection(projection: dict, known: dict) -> None:
    """A structure accessor is not a separately authored theorem leaf."""
    parent, field = projection['structure'], projection['field']
    if parent not in known or known[parent].kind not in {'structure', 'class'}:
        raise ValueError(f'Unknown projection structure: {parent}')
    source = base.sanitize_lean(known[parent].source_text)
    if not re.search(r'^\s+' + re.escape(field) + r'\s*(?:\([^\n]*\)\s*)?:', source, re.M):
        raise ValueError(f'Unknown structure field: {parent}.{field}')
    if not projection.get('role'):
        raise ValueError(f'Missing projection explanation: {parent}.{field}')


def render_unit(unit: dict, page: str, *, source_comparison: str = '') -> str:
    name = unit['declaration']
    declaration = inline_lean.declarations()[name]
    is_proof = declaration.kind in {'lemma', 'theorem', 'instance'}
    proof_title = 'Mathematical proof' if is_proof else 'Construction and meaning'
    steps = ''.join(
        f'<div class="proof-reader-step"><h4>{i}. {base.esc(s["title"])}</h4>'
        f'<p>{inline_text(s["text"])}</p><div class="proof-reader-equation">\\[{base.esc(s["formula"])}\\]</div>'
        '<details><summary>Corresponding Lean step</summary>'
        + (base.code_html(s['lean']) if '\n' in s['lean'] else f'<p>{inline_text(s["lean"])}</p>')
        + (f'<p>{inline_text(s["detail"])}</p>' if s.get('detail') else '') + '</details></div>'
        for i, s in enumerate(unit['steps'], 1)
    )
    astis = ''.join(
        f'<li><a href="{base.relative_prefix(page)}{base.declaration_path(inline_lean.declarations()[n])}"><code>{base.esc(n)}</code></a></li>'
        for n in unit.get('astis_dependencies', [])
    )
    projections = ''.join(
        f'<li><a href="{base.relative_prefix(page)}{base.declaration_path(inline_lean.declarations()[p["structure"]])}"><code>{base.esc(p["structure"] + "." + p["field"])}</code></a> — {base.esc(p["role"])}</li>'
        for p in unit.get('astis_projection_dependencies', [])
    )
    external = base.list_html(unit.get('mathlib_dependencies', []), empty='No direct Mathlib call recorded; see the ASTIS parents.')
    sources = ''.join(f'<li><a href="{base.esc(source_link(s, page))}">{base.esc(s["label"])}</a> — {base.esc(s["scope"])}</li>' for s in unit.get('sources', []))
    notation = ''.join(f'<dt>{inline_text(n["symbol"])}</dt><dd><p>{inline_text(n["text"])}</p><div class="proof-reader-equation">\\[{base.esc(n["formula"])}\\]</div></dd>' for n in unit.get('notation', []))
    test = unit.get('tests', {})
    examples = ''
    for key, title in [('worked_example', 'Worked example'), ('null_fiber_example', 'Why the positive-fiber hypothesis matters')]:
        example = test.get(key) if isinstance(test, dict) else None
        if example:
            examples += f'<h3>{title}</h3><p>{inline_text(example.get("definition", ""))}</p><div class="proof-reader-equation">\\[{base.esc(example["formula"])}\\]</div><p>{inline_text(example["explanation"])}</p>'
    dep_notes = unit.get('dependency_notes', '')
    if isinstance(dep_notes, list):
        dep_notes = ' '.join(str(n) for n in dep_notes)
    boundary = unit['boundary']
    if isinstance(boundary, str):
        boundary = [boundary]
    return (
        f'<article class="proof-reader" data-authored-declaration="{base.esc(name)}">'
        '<div class="eyebrow">ASTIS mathematical exposition</div>'
        f'<h1>{base.esc(unit["title"])}</h1>'
        f'<p><code>{base.esc(name)}</code> · {base.esc(declaration.kind)} · <a href="index.html">Teaching coverage</a></p>'
        f'<h2>Statement</h2><p>{base.esc(unit["statement"])}</p>'
        f'<div class="proof-reader-equation">\\[{base.esc(unit["formula"])}\\]</div>'
        '<h3>All objects and hypotheses</h3>' + base.list_html(unit['assumptions'])
        + ('<h3>Notation and interpretation</h3><dl>' + notation + '</dl>' if notation else '')
        + base.list_html(unit.get('conventions', []), empty='')
        + f'<h2>{proof_title}</h2>' + steps
        + inline_lean.disclosure(name, role='statement', explanation=unit['lean_statement'], page=page)
        + inline_lean.disclosure(name, role='proof', explanation=unit['lean_proof'], page=page, helpers=tuple(unit.get('helpers', [])))
        + examples
        + source_comparison
        + '<h2>Scope and omitted-condition boundaries</h2>' + base.list_html(boundary)
        + '<section class="proof-reader-provenance"><h2>Source and reuse</h2><h3>ASTIS parents called</h3><ul>' + astis
        + '</ul>'
        + ('<h3>Domain assumptions accessed</h3><p>These are fields of the linked structure, not additional independently authored theorem leaves.</p><ul>' + projections + '</ul>' if projections else '')
        + '<h3>Mathlib API called (external library)</h3>' + external
        + (f'<p>{inline_text(dep_notes)}</p>' if dep_notes else '')
        + ''.join(f'<p><code>{base.esc(n["declaration"])}</code>: {base.esc(n["role"])}</p>' for n in unit.get('mathlib_dependency_notes', []))
        + '<h3>Mathematical sources</h3><ul>' + sources
        + '</ul>'
        + (f'<p>{base.esc(unit["source_history_boundary"])}</p>' if unit.get('source_history_boundary') else '')
        + '<p>ASTIS prose is not a quotation or a source-equivalence certificate. '
        'Definitions and aliases are explained as constructions, not counted as new mathematical proofs.</p></section>'
        + '</article>'
    )


def coverage(data: dict, units: list[dict], data_lessons: dict | None = None) -> list[dict]:
    from proof_readers import load_items
    authored = {u['declaration']: lesson_path(u['declaration']) for u in units}
    for reader in load_items():
        authored.update({u['declaration']: f'proofs/{reader["id"]}.html' for u in reader['theorems']})
    existing_notes = {d['declaration'] for d in data['teaching_declarations']}
    data_lessons = data_lessons or {}
    rows = []
    for declaration in data['declarations']:
        name = declaration['full_name']
        if declaration['module'] == 'Tests' or declaration['module'].startswith('Tests.'):
            continue
        rows.append({
            'declaration': name, 'kind': declaration['kind'], 'module': declaration['module'],
            'lean_status': declaration['local_status'],
            'exposition': 'authored' if name in authored else data_lessons[name]['exposition'] if name in data_lessons else 'existing-notes' if name in existing_notes else 'needed',
            'page': authored.get(name, data_lessons.get(name, {}).get('page', declaration['page'])),
        })
    return rows


def enrich_site(output: Path) -> None:
    units = load_units()
    export_sources(output, units)
    known = inline_lean.declarations()
    for unit in units:
        for name in [unit['declaration'], *unit.get('astis_dependencies', []), *unit.get('helpers', [])]:
            if name not in known:
                raise ValueError(f'Unknown lesson dependency: {name}')
        if unit['kind'] != known[unit['declaration']].kind:
            raise ValueError(f'{unit["declaration"]}: Lean declaration kind drift')
        for projection in unit.get('astis_projection_dependencies', []):
            validate_projection(projection, known)
        rel = lesson_path(unit['declaration'])
        text = base.page(unit['title'], rel, render_unit(unit, rel), extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">')
        base.write_page(output, rel, source_lineage.canonical_shell(text, rel, output))
        declaration = known[unit['declaration']]
        module_page = output / f'modules/{base.slugify(declaration.module)}.html'
        text = module_page.read_text(encoding='utf-8')
        # The existing stable declaration anchor remains the identity of the node.
        marker = f'<details class="declaration" id="{declaration.anchor}">'
        start = text.index(marker)
        end = text.index('</summary>', start) + len('</summary>')
        jump = f'<p data-lesson-link="{base.esc(unit["declaration"])}"><a href="../{rel}">Read the complete mathematical statement and proof, with Lean below each</a></p>'
        text = text[:end] + jump + text[end:]
        module_page.write_text(text, encoding='utf-8')
    # A module is also a continuous mathematical reading route, not just a
    # collection of code anchors. Shared declarations retain their own identity.
    by_module = defaultdict(list)
    for unit in units:
        by_module[known[unit['declaration']].module].append(unit)
    for module, module_units in by_module.items():
        module_units.sort(key=lambda u: known[u['declaration']].source_line)
        rel = 'lessons/module-' + base.slugify(module) + '.html'
        contents = '<ol>' + ''.join(f'<li><a href="#{known[u["declaration"]].anchor}">{base.esc(u["title"])}</a></li>' for u in module_units) + '</ol>'
        body = f'<h1>{base.esc(module.rsplit(".", 1)[-1])}: mathematical reading route</h1><p>Read the statements and derivations in source order. Every result has its own optional Lean statement and proof. Source assumptions, library reuse and unproved boundaries are kept explicit.</p>' + contents
        for unit in module_units:
            card = render_unit(unit, rel)
            card = re.sub(r'<(/?)h([1-4])>', lambda m: f'<{m[1]}h{int(m[2])+1}>', card)
            body += f'<section id="{known[unit["declaration"]].anchor}">{card}</section>'
        base.write_page(output, rel, source_lineage.canonical_shell(base.page(module, rel, body, extra_head='<link rel="stylesheet" href="../assets/proof-readers.css">'), rel, output))
        module_page = output / f'modules/{base.slugify(module)}.html'
        text = module_page.read_text(encoding='utf-8')
        text = text.replace('</h1>', f'</h1><p><a href="../{rel}">Read the mathematical statements and proofs in order</a></p>', 1)
        module_page.write_text(text, encoding='utf-8')
    data = json.loads((output / 'data/site-data.json').read_text(encoding='utf-8'))
    import metadata_lessons
    rows = coverage(data, units, metadata_lessons.coverage_rows())
    (output / 'data/declaration-exposition.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts = Counter(r['exposition'] for r in rows)
    table = ''.join(f'<tr data-search="{base.esc((r["declaration"] + " " + r["kind"] + " " + r["exposition"]).lower())}"><td><a href="../{base.esc(r["page"])}"><code>{base.esc(r["declaration"])}</code></a></td><td>{base.esc(r["kind"])}</td><td>{base.esc(r["exposition"])}</td></tr>' for r in rows)
    body = f'<h1>Declaration-by-declaration textbook coverage</h1><p>{len(rows)} production declarations: {counts["authored"]} have newly authored complete teaching units; {counts["data-explained"]} are audited data constructions with field-by-field explanations, not mathematical proofs; {counts["data-unresolved"]} are unresolved data constructions; {counts["existing-notes"]} have existing notes not certified as complete textbook proofs; {counts["needed"]} still need a complete exposition. This is documentation coverage, not Lean completion. The requested full-library teaching expansion is unfinished.</p><p>Source records and definitions require explanations of their meaning, not fictitious proofs. A compiled proposition definition is not a proof of that proposition. <a href="../data-readers/index.html">Read the separate data-construction audit.</a></p><label>Find a declaration <input data-table-search="exposition-table" placeholder="Name or module"></label><table id="exposition-table"><thead><tr><th>Declaration</th><th>Kind</th><th>Teaching coverage</th></tr></thead><tbody>{table}</tbody></table>'
    rel = 'lessons/index.html'
    base.write_page(output, rel, source_lineage.canonical_shell(base.page('Textbook exposition coverage', rel, body), rel, output))
    for rel in ('proofs/index.html', 'progress/index.html'):
        path = output / rel
        text = path.read_text(encoding='utf-8')
        path.write_text(text.replace('</main>', '<p><a href="../lessons/index.html">Complete declaration-by-declaration teaching coverage</a></p></main>', 1), encoding='utf-8')


def validate_site(output: Path, *, require_complete: bool = False) -> list[str]:
    errors = []
    units = load_units()
    data = json.loads((output / 'data/site-data.json').read_text(encoding='utf-8'))
    import metadata_lessons
    expected = coverage(data, units, metadata_lessons.coverage_rows())
    actual = json.loads((output / 'data/declaration-exposition.json').read_text(encoding='utf-8'))
    if actual != expected:
        errors.append('Declaration exposition coverage drift')
    if require_complete and any(r['exposition'] not in {'authored', 'data-explained'} for r in expected):
        errors.append('Full-library textbook exposition is not complete')
    for unit in units:
        path = output / lesson_path(unit['declaration'])
        if not path.is_file():
            errors.append(f'{unit["declaration"]}: missing authored page; rebuild the site')
            continue
        text = path.read_text(encoding='utf-8')
        for value in (unit['statement'], unit['formula'], *unit['assumptions'], *[s['formula'] for s in unit['steps']]):
            if base.esc(value) not in text:
                errors.append(f'{unit["declaration"]}: missing authored mathematics')
        order = [text.find('inline-lean-statement'), text.find('inline-lean-proof')]
        if min(order) < 0 or order != sorted(order):
            errors.append(f'{unit["declaration"]}: missing adjacent Lean statement/proof')
        if re.search(r'<details\b[^>]*\bopen(?:\s|>)', text):
            errors.append(f'{unit["declaration"]}: Lean must start folded')
    return errors
