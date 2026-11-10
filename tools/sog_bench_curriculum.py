"""Authored difficulty taxonomy and bounded structural QA, not theorem inference."""
from __future__ import annotations

import hashlib
from datetime import datetime
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'benchmarks/samplingoptimisationgeometrybench'


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def curriculum() -> dict:
    data = json.loads((BASE / 'curriculum.json').read_text(encoding='utf-8'))
    if data['schema_version'] != 1 or set(data['levels']) != {f'L{i}' for i in range(1, 6)} or len(data['domains']) != 7:
        raise ValueError('Expected the seven-domain, five-level curriculum')
    return data


def classify(core: dict, policy: dict) -> None:
    if type(core.get('lean_enabled', True)) is not bool:
        raise ValueError('Lean availability must be an explicit Boolean')
    if not core['library_domains'] or len(set(core['library_domains'])) != len(core['library_domains']):
        raise ValueError('Each item needs nonduplicate domain placement')
    if not set(core['library_domains']) <= set(policy['domains']):
        raise ValueError('Unknown curriculum domain')
    if not core['skills'] or not set(core['skills']) <= set(policy['skills']):
        raise ValueError('Unknown or empty reasoning skills')
    expected = {'natural-language', 'lean'} if core.get('lean_enabled', True) else {'natural-language'}
    if set(core['track_levels']) != expected or not set(core['track_levels'].values()) <= set(policy['levels']):
        raise ValueError('Difficulty must be supplied separately for exactly the available QA tracks')
    if not core['difficulty_reason'].strip():
        raise ValueError('Difficulty needs a reasoning-based justification')


def graph_items() -> list[dict]:
    """Read only an explicit local-code slice, never the mixed upstream graph."""
    import astis_site
    policy = curriculum()
    anchors={c['id']:c for c in json.loads((BASE/'cores.json').read_text(encoding='utf-8'))['cores']}
    spec = json.loads((BASE / 'graph_tasks.json').read_text(encoding='utf-8'))
    if spec['schema_version'] != 1:
        raise ValueError('Unsupported structural graph schema')
    sources, names, imports = {}, set(), {}
    for rel in spec['source_files']:
        if '\\' in rel or '..' in Path(rel).parts or not rel.startswith('AutoSamplingTheory/TechnicalLemmas/') or not rel.endswith('.lean'):
            raise ValueError('Graph ML context must use explicitly eligible local technical modules')
        path = ROOT / rel
        text = path.read_text(encoding='utf-8').replace('\r\n', '\n')
        if 'atlas' in text.lower():
            raise ValueError('Restricted-source references require a separate license audit; not eligible for this graph slice')
        sources[rel] = hashlib.sha256(text.encode()).hexdigest()
        name = rel.removesuffix('.lean').replace('/', '.')
        names.add(name)
        imports[name] = re.findall(r'^import ([\w.]+)\s*$', astis_site.sanitize_lean(text), re.M)
    if len(names) != len(spec['source_files']):
        raise ValueError('Duplicate graph source module')
    edges = sorted([a, b] for a, dependencies in imports.items() for b in dependencies if b in names)
    graph = {'kind': 'source-scanned-module-imports', 'direction': 'consumer-to-imported-module',
             'scope': 'induced slice only; omitted imports are not absent from the whole library',
             'nodes': sorted(names), 'edges': edges, 'source_sha256_lf': sources,
             'truth_boundary': 'Syntactic import availability only; not theorem implication or mathematical necessity.'}
    graph_hash = digest(graph)
    adjacency = {a: {b for x, b in edges if x == a} for a in names}
    rows, seen = [], set()
    for task in spec['tasks']:
        if not re.fullmatch(r'sogb-g\d{3}', task['id']) or task['id'] in seen:
            raise ValueError('Duplicate/invalid graph task identity')
        seen.add(task['id'])
        anchor=anchors.get(task.get('core_id'))
        if anchor is None or task['family']!=anchor['family'] or not set(task['library_domains'])<=set(anchor['library_domains']):
            raise ValueError('Graph context must retain its existing source core/family/domain identity')
        if not set(task['targets']) <= names or not task['targets']:
            raise ValueError('Graph targets must exist in the supplied slice')
        classify({**task, 'track_levels': {'natural-language': task['level']}, 'lean_enabled': False,
                  'difficulty_reason': 'Structural operation, not graph distance or mathematical difficulty.'}, policy)
        op = task['operation']
        if op == 'direct-imports':
            if len(task['targets']) != 1:
                raise ValueError('Direct-import query has one target')
            nodes = adjacency[task['targets'][0]]
            question = 'List the direct imported modules of the target within the supplied induced slice.'
        elif op == 'common-imports':
            nodes = set.intersection(*(adjacency[t] for t in task['targets']))
            question = 'List the modules directly imported by every listed target, within this slice.'
        elif op == 'affected-targets':
            removed = task['remove']
            if removed not in names or removed in task['targets']:
                raise ValueError('Remove an existing, nontarget module')
            def reaches(start):
                todo, visited = [start], set()
                while todo:
                    node = todo.pop()
                    if node == removed:
                        return True
                    if node not in visited:
                        visited.add(node)
                        todo.extend(adjacency[node])
                return False
            nodes = {t for t in task['targets'] if reaches(t)}
            question = 'List the target modules that have an import path to the removed module in this snapshot. Does this prove that their mathematical conclusions cannot be proved without it?'
        else:
            raise ValueError('Unsupported graph operation')
        prompt = {'id': task['id'], 'core_id':task['core_id'], 'family': task['family'], 'title': task['title'],
                  'library_domains': task['library_domains'], 'track': 'graph-json', 'level': task['level'],
                  'split': 'public-dev', 'skills': task['skills'], 'question': question,
                  'targets': task['targets'], 'context': graph, 'graph_sha256': graph_hash,
                  'answer_schema': {'nodes': 'list of distinct module ids; order ignored by the scorer', 'entails_mathematical_necessity': 'boolean; whether this evidence certifies mathematical necessity'}}
        if 'remove' in task:
            prompt['remove'] = task['remove']
        answer = {'nodes': sorted(nodes), 'entails_mathematical_necessity': False}
        binding = digest({'prompt': prompt, 'answer': answer})
        rows.append({**prompt, 'binding_sha256': binding, 'answer': answer,
                     'reference_status': 'structural-answer-mechanically-checked; see separate editorial evidence'})
    import sog_bench_graph_slices
    rows += sog_bench_graph_slices.items()
    ids=[row['id'] for row in rows]
    if len(set(ids))!=len(ids) or not all(re.fullmatch(r'sogb-g\d{3}',identity) for identity in ids):
        raise ValueError('Graph identities must be distinct across evidence kinds')
    return rows


def graph_prompt(item: dict) -> dict:
    """Identify only the visible task, never commit to a small answer space."""
    required = ('id', 'core_id', 'family', 'title', 'library_domains', 'track', 'level',
                'split', 'skills', 'question', 'targets', 'context', 'graph_sha256', 'answer_schema')
    optional = ('remove', 'required_statement_constants')
    prompt = {k: item[k] for k in required}
    prompt.update({k: item[k] for k in optional if k in item})
    return {**prompt, 'prompt_sha256': digest(prompt)}


def graph_prompts(items: list[dict]) -> list[dict]:
    return [graph_prompt(item) for item in items]


def parse_graph_record(raw: str) -> dict:
    """Preserve one unambiguous object; never let last-key-wins change an attempt."""
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise ValueError('Duplicate key in graph JSON')
            out[key] = value
        return out

    def nonfinite(value):
        raise ValueError('Non-finite graph JSON number: ' + value)

    value = json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)
    if not isinstance(value, dict):
        raise ValueError('Expected one graph JSON object')
    return value


def bind_graph_submissions(items: list[dict], rows: list[dict], *, allow_legacy: bool = False) -> list[dict]:
    """Operator-side translation after capture; preserve the frozen gold scorer."""
    by_id = {item['id']: item for item in items}
    out = []
    for row in rows:
        identity = row.get('id') if isinstance(row, dict) else None
        if not isinstance(identity, str) or identity not in by_id:
            raise ValueError('Unknown graph response identity')
        item = by_id[identity]
        common = {'id', 'attempt', 'answer'}
        if allow_legacy and set(row) == common | {'binding_sha256'}:
            out.append(dict(row))  # grade_graph still checks the exact historical binding.
            continue
        if (set(row) != common | {'prompt_sha256'}
                or row['prompt_sha256'] != graph_prompt(item)['prompt_sha256']):
            raise ValueError('Response does not identify the exact public graph prompt')
        out.append({k: row[k] for k in ('id', 'attempt', 'answer')} |
                   {'binding_sha256': item['binding_sha256']})
    return out


def coverage(cores: list[dict], graphs: list[dict], reviews: dict | None = None) -> dict:
    import sog_bench_graph_review
    policy = curriculum()
    accepted = sum((reviews or {}).get(c['id'], {}).get('editorial') in {'accepted', 'accepted-after-repair'} for c in cores)
    cells = []
    for domain in policy['domains']:
        for level in policy['levels']:
            counts = {t: sum(domain in c['library_domains'] and c['track_levels'].get(t) == level for c in cores)
                      for t in ('natural-language', 'lean')}
            counts['graph-json'] = sum(domain in g['library_domains'] and g['level'] == level for g in graphs)
            reviewed = sum(domain in c['library_domains'] and c['track_levels'].get(t) == level
                           and (reviews or {}).get(c['id'], {}).get('editorial') in {'accepted', 'accepted-after-repair'}
                           for c in cores for t in ('natural-language', 'lean'))
            cells.append({'domain': domain, 'level': level, 'draft_views': counts,
                          'independently_reviewed': reviewed, 'review_kind': 'AI editorial only', 'gap': not any(counts.values())})
    return {'unique_mathematical_cores': len(cores), 'mathematical_views': sum(len(c['track_levels']) for c in cores),
            'graph_tasks': len(graphs), 'independent_review': 'pending', 'difficulty_calibration': 'not-measured',
            'editorial_accepted_mathematical_cores': accepted,
            'mathematical_editorial_status': 'complete-for-current-cores' if cores and accepted == len(cores) else ('partial' if accepted else 'pending'),
            'graph_editorial_status': sog_bench_graph_review.summary(graphs)['editorial_status'],
            'cells': cells, 'note': policy['coverage_policy']}


def grade_graph(items: list[dict], submissions: list[dict]) -> dict:
    known = {r['id']: r for r in items}
    given = {}
    for row in submissions:
        identity = row['id']
        if identity not in known or identity in given or type(row.get('attempt')) is not int or row['attempt'] != 1:
            raise ValueError('Expected one first-attempt record per known graph question')
        if row.get('binding_sha256') != known[identity]['binding_sha256']:
            raise ValueError('Submission does not bind the exact graph/question snapshot')
        given[identity] = row
    scores = []
    for identity, item in known.items():
        answer = given.get(identity, {}).get('answer')
        valid = (isinstance(answer, dict) and set(answer) == {'nodes', 'entails_mathematical_necessity'}
                 and isinstance(answer['nodes'], list) and all(isinstance(n, str) for n in answer['nodes'])
                 and len(set(answer['nodes'])) == len(answer['nodes'])
                 and type(answer['entails_mathematical_necessity']) is bool)
        structural = int(valid and set(answer['nodes']) == set(item['answer']['nodes']))
        boundary = int(valid and answer['entails_mathematical_necessity'] is False)
        scores.append({'id': identity, 'submitted': identity in given, 'valid_schema': valid,
                       'structural_exact': structural, 'truth_boundary': boundary, 'points': structural * boundary,
                       'max_points': 1})
    return {'scope': 'structured graph QA only; not mathematical proof or Lean grading',
            'question_count': len(items), 'submitted': len(given), 'results': scores,
            'points': sum(r['points'] for r in scores), 'max_points': len(items),
            'scoring_policy': 'One point only when both the exact structural set and truth-boundary gate pass; the constant boundary answer earns no standalone credit.'}


def validate_run_metadata(metadata: dict) -> None:
    strings = ('run_id', 'model', 'model_version', 'created_at', 'prompt_profile', 'attempt_policy')
    if not all(isinstance(metadata.get(k), str) and metadata[k].strip() for k in strings):
        raise ValueError('Missing run identity, model/version, time or evaluation profile')
    if metadata['attempt_policy'] != 'first-attempt' or metadata['prompt_profile'] != 'given-snapshot':
        raise ValueError('Only first-attempt, given-snapshot graph scoring is supported')
    if not isinstance(metadata.get('tools'), list) or not all(isinstance(t, str) for t in metadata['tools']):
        raise ValueError('Record tools as a list; this is provenance, not enforcement')
    if 'seed' not in metadata or not (metadata['seed'] is None or type(metadata['seed']) is int):
        raise ValueError('Record an integer seed, or null if unavailable')
    if datetime.fromisoformat(metadata['created_at']).tzinfo is None:
        raise ValueError('Run time must contain a timezone')
