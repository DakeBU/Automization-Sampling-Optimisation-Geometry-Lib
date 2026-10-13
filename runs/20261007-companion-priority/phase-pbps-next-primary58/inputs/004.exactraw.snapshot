#!/usr/bin/env python3
"""Incremental theorem → reader → semantic-audit publication contract.

This is an index of correspondence edges, never a second proof-status registry.
Compilation remains the Lean gate's job; semantic equivalence remains an
independent reviewer's job. No model calls or background sessions are started.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'website/scripts'))
import astis_site
import astis_frontier_cells
import astis_semantic_roundtrip as roundtrip

CONTENT = ROOT / 'website/content/publications'
MIGRATION_BASE = '5c6adf3b812f3ba9315c92ba78a4ff59ccc2a53e'
LEGACY_FILE_SHA = '6efa3254bc53f8bd93423d56c79f38b90af35f0097e1223940c328861b336c17'
REGISTRY_DATA_NAMES = frozenset(('sltSourceAnchor analysisMemory gaussianMemory taylorMemory '
    'calculusMemory measureMemory probabilityMemory functionalInequalityMemory stochasticProcessMemory '
    'klDensityMemory renyiDensityMemory variationalMemory geometryMemory saldExtractedMemory '
    'portQueueMemory technicalLemmaMemory formalizedTechnicalLemmaCount').split())
REGISTRY_METADATA_TYPES = frozenset({
    ('inductive', 'AutoSamplingTheory.TechnicalLemmas.LemmaMemoryStatus'),
    ('structure', 'AutoSamplingTheory.TechnicalLemmas.LemmaMemoryEntry'),
})
LEGACY_NAMES = frozenset(
    'AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.' + name
    for name in ('firstOrder_lower_bound_of_strongConvexOn',
                 'gradient_inner_lower_bound_of_strongConvexOn')
)
PRIVATE_IMPLEMENTATION_COVERAGE: list[dict] = []


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def file_digest(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_text(encoding='utf-8').encode()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, encoding='utf-8')


@lru_cache(maxsize=1)
def inputs() -> dict:
    import declaration_lessons
    return {
        'declarations': {d.full_name: d for d in astis_site.scan_project_sources()[1]},
        'lessons': {u['declaration']: u for u in declaration_lessons.load_units()},
        'cells': {c['cell_id']: c for c in astis_frontier_cells.load_cells()},
        'audits': {a['id']: a for a in roundtrip.load_registry()['audits']},
    }


@lru_cache(maxsize=1)
def load() -> list[dict]:
    records = []
    for path in sorted(CONTENT.glob('*.json')):
        raw = json.loads(path.read_text(encoding='utf-8'))
        if raw.get('schema_version') != 1:
            raise ValueError(f'{path.name}: publication schema must be 1')
        records.extend(raw['items'])
    return records


def binding_payload(item: dict, binding: dict, data: dict | None = None) -> dict:
    """Bind code (including imports/scoped variables), source, prose and reuse.

Conservative file-level invalidation is intentional: a changed section variable
can change an elaborated theorem without changing its declaration text.
"""
    data = data or inputs()
    name = binding['declaration']
    decl = data['declarations'][name]
    return {
        'file': file_digest(decl.source_file),
        'current_lean_module': (ROOT / decl.source_file).read_text(encoding='utf-8'),
        'toolchain': file_digest('lean-toolchain'),
        'dependencies': file_digest('lake-manifest.json'),
        'source': item['source'], 'statement': item['statement'],
        'formulae': item['formulae'], 'assumptions': item['assumptions'],
        'obligations': item['obligations'], 'lesson': data['lessons'].get(name),
        'binding': {k: v for k, v in binding.items()
                    if k not in {'audit_id', 'legacy_audit_debt'}},
    }


def binding_digest(item: dict, binding: dict, data: dict | None = None) -> str:
    return digest(binding_payload(item, binding, data))


def review_context(item: dict, binding: dict, data: dict | None = None) -> dict:
    """Candidate mathematics to review, not earlier verdicts/delta classifications."""
    payload = binding_payload(item, binding, data)
    payload['binding'] = {k: payload['binding'][k] for k in ('declaration', 'role', 'supports')}
    payload['lesson'] = {k: v for k, v in payload['lesson'].items()
                         if k not in {'boundary', 'source_history_boundary'}}
    # Assumption comparison is a formalizer claim, not a prior review verdict.
    payload['candidate_assumptions'] = [{k: row[k] for k in ('source', 'lean')}
                                        for row in binding['assumption_deltas']]
    return payload


def legacy_debt_valid(binding: dict, data: dict) -> bool:
    """Two explicitly grandfathered proofs, not an opt-out for new work."""
    name = binding.get('declaration')
    if name not in LEGACY_NAMES or name not in data['declarations']:
        return False
    debt = binding.get('legacy_audit_debt', {})
    return (debt.get('base_commit') == MIGRATION_BASE
            and debt.get('file_sha256') == LEGACY_FILE_SHA == file_digest(data['declarations'][name].source_file)
            and bool(debt.get('reason')))


def validate(items: list[dict] | None = None, data: dict | None = None,
             *, strict_names: set[str] | None = None) -> list[str]:
    items, data = (load() if items is None else items), (inputs() if data is None else data)
    errors, seen, mapped = [], set(), set()
    for item in items:
        ident = item.get('id', '<missing id>')
        if ident in seen:
            errors.append(f'{ident}: duplicate source item')
        seen.add(ident)
        for key in ('id', 'library', 'chapter', 'chapter_path', 'title', 'source',
                    'statement', 'formulae', 'assumptions', 'obligations', 'bindings'):
            if not item.get(key):
                errors.append(f'{ident}: missing {key}')
        source = item.get('source', {})
        for key in ('url', 'edition', 'anchor', 'wording_status'):
            if not source.get(key):
                errors.append(f'{ident}: source.{key} missing')
        if source.get('wording_status') not in {'faithful paraphrase', 'licensed original', 'short quotation'}:
            errors.append(f'{ident}: invalid wording status')
        if not str(source.get('url', '')).startswith('https://'):
            errors.append(f'{ident}: source must be HTTPS')
        for key in ('chapter_path',):
            path = str(item.get(key, ''))
            if not path.endswith('.html') or path.startswith('/') or '..' in Path(path).parts or ':' in path or '\\' in path:
                errors.append(f'{ident}: nonportable {key}')
        obligations = {o.get('id') for o in item.get('obligations', [])}
        if len(obligations) != len(item.get('obligations', [])):
            errors.append(f'{ident}: duplicate obligation')
        for binding in item.get('bindings', []):
            name = binding.get('declaration', '<missing declaration>')
            mapped.add(name)
            decl = data['declarations'].get(name)
            if not decl or decl.has_placeholder:
                errors.append(f'{ident}: missing/placeholder declaration {name}')
                continue
            lesson = data['lessons'].get(name)
            if not lesson:
                errors.append(f'{name}: authored statement/formula/proof/adjacent Lean lesson required')
            else:
                for dependency in lesson.get('astis_dependencies', []) + lesson.get('helpers', []):
                    if dependency not in data['declarations']:
                        errors.append(f'{name}: unknown lesson dependency {dependency}; use an exact declaration id, not explanatory prose')
            if binding.get('cell') not in data['cells']:
                errors.append(f'{name}: missing Frontier Cell')
            elif data['cells'][binding['cell']].get('shared_floor_audit', {}).get('canonical_declaration') != name:
                errors.append(f'{name}: Frontier Cell canonical declaration does not match')
            if binding.get('role') not in {'proof-edge', 'prerequisite'}:
                errors.append(f'{name}: role must distinguish proof-edge from prerequisite')
            if not binding.get('boundary') or not binding.get('assumption_deltas'):
                errors.append(f'{name}: explicit boundary and assumption ledger required')
            for row in binding.get('assumption_deltas', []):
                if not all(row.get(k) for k in ('source', 'lean', 'classification', 'reason')):
                    errors.append(f'{name}: incomplete source/Lean assumption comparison')
                if row.get('classification') not in {'same', 'source-implicit', 'mathematically-necessary', 'API-limitation', 'generalization', 'unresolved'}:
                    errors.append(f'{name}: invalid assumption classification')
            if not set(binding.get('supports', [])) <= obligations:
                errors.append(f'{name}: unknown source obligation')
            if binding.get('role') == 'proof-edge' and not binding.get('supports'):
                errors.append(f'{name}: proof-edge needs an actual source proof obligation')
            if binding.get('role') == 'proof-edge' and decl.kind not in {'theorem', 'lemma'}:
                errors.append(f'{name}: a definition/construction is not a proof-edge')
            audit = data['audits'].get(binding.get('audit_id'))
            if audit:
                if audit['lean']['declaration'] != name:
                    errors.append(f'{name}: audit belongs to another declaration')
                if audit.get('publication_binding_sha256') != binding_digest(item, binding, data):
                    errors.append(f'{name}: stale code/source/exposition round-trip binding; regenerate the bounded audit packet')
                if lesson and audit.get('publication_context') != review_context(item, binding, data):
                    errors.append(f'{name}: source reviewer must receive current code and candidate exposition, not only a hash')
                if strict_names and name in strict_names and audit.get('state') not in {'source-reviewed', 'accepted', 'rejected'}:
                    errors.append(f'{name}: independent source review must finish before publication (draft is not a verdict)')
            elif not legacy_debt_valid(binding, data):
                errors.append(f'{name}: canonical encoder–denoiser audit required')
            elif strict_names and name in strict_names:
                errors.append(f'{name}: changed Lean cannot reuse historical audit debt')
    for name in sorted((strict_names or set()) - mapped):
        errors.append(f'{name}: changed Lean declaration has no publication edge/lesson/audit')
    return errors


def verified_binding(binding: dict, data: dict | None = None) -> bool:
    data = data or inputs()
    cell = data['cells'].get(binding.get('cell'), {})
    d = data['declarations'].get(binding.get('declaration'))
    return bool(d and not d.has_placeholder
                and (binding.get('role') != 'proof-edge' or d.kind in {'theorem', 'lemma'})
                and cell.get('shared_floor_audit', {}).get('canonical_declaration') == d.full_name
                and cell.get('status') in {'independently_verified', 'stabilized', 'merged'})


def chapter_progress(library: str, chapter: str | None = None) -> dict:
    data = inputs()
    bindings = [b for i in load() if i['library'] == library
                and (chapter is None or i['chapter'] == chapter) for b in i['bindings']]
    proved, prerequisites = set(), set()
    for b in bindings:
        if verified_binding(b, data):
            (proved if b['role'] == 'proof-edge' else prerequisites).add(b['declaration'])
    # No chapter-complete inference: the source inventory is not exhaustive.
    return {'status': 'partial' if proved else 'prerequisite-ready' if prerequisites else 'scaffold',
            'label': 'Partially formalized' if proved else 'Prerequisites available' if prerequisites else 'scaffold',
            'proof_declarations': sorted(proved), 'prerequisites': sorted(prerequisites),
            'source_complete': False}


def private_implementation_owner(path: str, text: str, public_names: set[str], data: dict) -> str:
    """A private implementation is covered only by a fresh whole-module review.

    This creates no publication edge or mathematical credit for the helper.
    The covering public theorem remains a strict release target.
    """
    for item in load():
        for binding in item['bindings']:
            name = binding['declaration']
            decl = data['declarations'].get(name)
            if (name not in public_names or not decl or decl.source_file != path
                    or decl.kind not in {'theorem', 'lemma'}):
                continue
            audit = data['audits'].get(binding.get('audit_id'), {})
            if (audit.get('state') not in {'accepted', 'source-reviewed'}
                    or audit.get('source_review', {}).get('state') != 'accepted'
                    or audit.get('publication_context', {}).get('current_lean_module') != text
                    or audit.get('publication_binding_sha256') != binding_digest(item, binding, data)):
                continue
            if not validate([item], data, strict_names={name}):
                return name
    raise ValueError(f'{path}: private implementation has no fresh, accepted whole-module public theorem review')


def changed_declarations(base: str) -> set[str]:
    """Conservative changed-module gate; catches scoped assumptions and imports.

All declarations in a changed production file must be accounted for. Root
aggregators and test examples do not count as new mathematical declarations.
"""
    git('rev-parse', '--verify', base + '^{commit}')
    paths = set(git('diff', '--name-only', '-z', base, '--', 'AutoSamplingTheory', 'AutoSamplingTheory.lean').split('\0'))
    # Untracked candidate files matter locally too; CI sees them after commit.
    paths.update(git('ls-files', '--others', '--exclude-standard', '-z', 'AutoSamplingTheory', 'AutoSamplingTheory.lean').split('\0'))
    paths.discard('')
    PRIVATE_IMPLEMENTATION_COVERAGE.clear()
    data = inputs()
    known = {(d.source_file, d.source_line, d.kind, d.short_name): d for d in data['declarations'].values()}
    private_names, owners = set(), set()
    for path in paths:
        if not path.endswith('.lean') or not (ROOT / path).is_file():
            continue
        text = (ROOT / path).read_text(encoding='utf-8')
        clean = astis_site.sanitize_lean(text)
        implementations = []
        # Inspect complete tokens anywhere, not only at the beginning of a line:
        # multiline attributes and Unicode suffixes must not hide declarations.
        for match in re.finditer(r'\b(theorem|lemma|def|abbrev|structure|class|inductive|opaque|axiom|instance)\b\s*([^\s(\[{:=]*)', clean):
            line = clean.count('\n', 0, match.start()) + 1
            kind, name = match.groups()
            prefix = clean[clean.rfind('\n', 0, match.start()) + 1:match.start()]
            # Only an explicit command modifier counts. Unsupported multiline
            # syntax fails closed, as do private tokens in earlier commands.
            modifiers = re.fullmatch(r'\s*(?:@\[[^\]]*\]\s*)*((?:(?:noncomputable|private|protected|local|unsafe)\s+)*)', prefix)
            private = bool(modifiers and 'private' in modifiers.group(1).split())
            decl = known.get((path, line, kind, name.rsplit('.', 1)[-1]))
            anonymous_private_instance = private and kind == 'instance' and not name
            if not decl and not anonymous_private_instance:
                raise ValueError(f'{path}:{line}: unindexed declaration syntax/name; extend the inventory before publishing (no silent Unicode/anonymous-instance bypass)')
            if private:
                if kind == 'axiom':
                    raise ValueError(f'{path}:{line}: private axiom cannot be implementation coverage')
                if decl:
                    private_names.add(decl.full_name)
                implementations.append({'file': path, 'line': line,
                    'column': match.start() - clean.rfind('\n', 0, match.start()),
                    'kind': kind, 'visibility': 'private', 'name': decl.full_name if decl else None,
                    'anonymous': anonymous_private_instance})
        if implementations:
            public_names = {d.full_name for d in data['declarations'].values()
                            if d.source_file == path and d.full_name not in private_names}
            owner = private_implementation_owner(path, text, public_names, data)
            owners.add(owner)
            PRIVATE_IMPLEMENTATION_COVERAGE.extend(dict(row, owner=owner) for row in implementations)
    return owners | {d.full_name for d in data['declarations'].values() if d.source_file in paths
            and d.full_name not in private_names
            and not (d.source_file == 'AutoSamplingTheory/TechnicalLemmas/Registry.lean'
                     and ((d.kind == 'def' and d.short_name in REGISTRY_DATA_NAMES)
                          or (d.kind, d.full_name) in REGISTRY_METADATA_TYPES))}


def packet(cell_id: str) -> dict:
    data = inputs()
    cell = data['cells'].get(cell_id)
    if cell is None:
        raise ValueError(f'Unknown Frontier Cell {cell_id}')
    targets = []
    for item in load():
        for b in item['bindings']:
            if b['cell'] != cell_id:
                continue
            audit = data['audits'].get(b.get('audit_id'), {})
            targets.append({'declaration': b['declaration'], 'source_item': item['id'],
                            'lesson': 'authored' if b['declaration'] in data['lessons'] else 'needed',
                            'audit_id': b.get('audit_id'), 'audit_state': audit.get('state', 'legacy-debt'),
                            'publication_binding_sha256': binding_digest(item, b, data),
                            'remaining_boundary': b['boundary']})
    return {'cell': cell_id, 'targets': targets,
            'graph_check': f'python3 tools/astis_publication.py graph-check --cell {cell_id}',
            'missing': [] if targets else ['Add one source item/binding and an authored declaration lesson.'],
            'next': ['Run the smallest focused Lean test.',
                     'Reuse unchanged source/lesson/audit records; never reuse a stale binding.',
                     'For a new/changed theorem, use astis-semantic-roundtrip: anonymous decoder → independent anti-anchored source review → separate repair review if needed.',
                     'Run tools/astis_publication.py check --base <base commit> before stabilization.'],
            'boundary': 'This coordinator packet is NOT decoder input. It deliberately contains source identity.'}


def graph_report(cell_id: str, output: Path) -> dict:
    """Bounded generated one-hop context; no model call, build, or new ledger."""
    import publication_reader
    cell = inputs()['cells'].get(cell_id)
    if not cell:
        raise ValueError(f'Unknown Frontier Cell {cell_id}')
    items = [i for i in load() if any(b['cell'] == cell_id for b in i['bindings'])]
    if not items:
        raise ValueError(f'{cell_id}: no publication binding; add the source mapping first')
    try:
        graph = json.loads((output / 'data/underlying-lean-graph.json').read_text(encoding='utf-8'))
        site = json.loads((output / 'data/site-data.json').read_text(encoding='utf-8'))
    except FileNotFoundError as exc:
        raise ValueError('Build the site once before graph-check; no graph is generated by this command') from exc
    errors = publication_reader.validate_graph(graph, site, items)
    # Do not let a stale generated inventory hide a moved/renamed contribution.
    inventory = {d['full_name']: d for d in site['declarations']}
    names = sorted({b['declaration'] for i in items for b in i['bindings'] if b['cell'] == cell_id})
    for name in names:
        current, generated = inputs()['declarations'].get(name), inventory.get(name, {})
        if not current or any(generated.get(k) != getattr(current, k) for k in ('module', 'source_file', 'source_line')):
            errors.append(f'{name}: generated inventory is stale; rebuild the site')
    if errors:
        raise ValueError('\n'.join(errors))
    slices = []
    for name in names:
        ident = 'decl:' + name
        incident = sorted((e for e in graph['edges'] if ident in (e['source'], e['target'])),
                          key=lambda e: (e['relation'], e['source'], e['target']))
        slices.append({'node': ident,
            'focus': 'lean-foundations.html?view=lean&focus=' + quote(ident, safe='') + '&q=' + quote(name, safe=''),
            'connections': incident[:12], 'omitted_connections': max(0, len(incident) - 12)})
    return {'cell': cell_id, 'status': 'graph coverage checked', 'contributions': slices,
            'boundary': 'Reference scans are incomplete. Inspect the affected view; this report is not visual QA or a proof certificate.'}


def release_targets(base: str | None) -> set[str]:
    # All non-grandfathered public mappings need completed review, even if only
    # source/prose/audit metadata changed. The changed Lean gate additionally
    # catches omissions and invalidates the two historical debt exceptions.
    return (changed_declarations(base) if base else set()) | {
        b['declaration'] for i in load() for b in i['bindings'] if not legacy_debt_valid(b, inputs())}


def check_advance(declarations: list[str], *, reviewed: bool) -> None:
    inputs.cache_clear()
    load.cache_clear()
    errors = roundtrip.validate_registry(roundtrip.load_registry())
    errors += validate(strict_names=set(declarations) if reviewed else None)
    known = {b['declaration'] for i in load() for b in i['bindings']}
    errors += [f'{n}: publication record missing' for n in declarations if n not in known]
    if errors:
        raise ValueError('Reader/round-trip publication gate:\n' + '\n'.join(errors))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    check = sub.add_parser('check')
    check.add_argument('--base')
    check.add_argument('--ci', action='store_true')
    sub.add_parser('summary')
    p = sub.add_parser('packet')
    p.add_argument('--cell', required=True)
    graph = sub.add_parser('graph-check')
    graph.add_argument('--cell', required=True)
    graph.add_argument('--output', type=Path, default=ROOT / '_site')
    context = sub.add_parser('review-context')
    context.add_argument('--declaration', required=True)
    context.add_argument('--item', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'graph-check':
            print(json.dumps(graph_report(args.cell, args.output), ensure_ascii=False, indent=2))
        elif args.command == 'review-context':
            item = next(i for i in load() if i['id'] == args.item)
            b = next(b for b in item['bindings'] if b['declaration'] == args.declaration)
            print(json.dumps({'publication_binding_sha256': binding_digest(item, b),
                              'publication_context': review_context(item, b)}, ensure_ascii=False, indent=2))
        elif args.command == 'packet':
            print(json.dumps(packet(args.cell), ensure_ascii=False, indent=2))
        elif args.command == 'summary':
            print(json.dumps({l: chapter_progress(l) for l in sorted({i['library'] for i in load()})}, indent=2))
        else:
            base = args.base
            if args.ci:
                base = os.environ.get('PUBLICATION_BASE') or None
                if not base or set(base) == {'0'}:
                    base = 'HEAD^'
            errors = roundtrip.validate_registry(roundtrip.load_registry())
            errors += validate(strict_names=release_targets(base) if base or args.ci else None)
            if errors:
                print('\n'.join(errors), file=sys.stderr)
                return 1
            for row in PRIVATE_IMPLEMENTATION_COVERAGE:
                print('Private implementation coverage: ' + json.dumps(row, ensure_ascii=False))
            print(f'Publication PASS: {len(load())} source items; code, prose, assumptions and semantic-audit links checked. Legacy audit debt remains explicit.')
    except (ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
