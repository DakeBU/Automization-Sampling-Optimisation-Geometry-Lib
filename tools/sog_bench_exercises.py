"""Numbered source exercises, not a second theorem-status registry."""
from __future__ import annotations

import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'benchmarks/samplingoptimisationgeometrybench/textbook_exercises.json'


def primary_url(value) -> bool:
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    parsed = urlsplit(value)
    return parsed.scheme == 'https' and bool(parsed.hostname) and parsed.username is None and parsed.password is None


def resolve(identity: str, known: dict, data: dict | None = None) -> dict:
    import sog_bench as bench
    data = json.loads(DATA.read_text(encoding='utf-8')) if data is None else data
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Unsupported textbook-exercise schema')
    records = data['exercises']
    if len({r['id'] for r in records}) != len(records):
        raise ValueError('Duplicate numbered exercise')
    rows = [r for r in records if r['id'] == identity]
    if len(rows) != 1:
        raise ValueError('Unknown numbered textbook exercise')
    row = rows[0]
    book = data['books'][row['book_id']]
    if (not re.fullmatch(r'[0-9a-f]{64}', book['pdf_sha256'])
            or type(book['pdf_pages']) is not int or book['pdf_pages'] < 1
            or not book['authors'] or not all(isinstance(a, str) and a.strip() for a in book['authors'])
            or not all(isinstance(book[k], str) and book[k].strip()
                       for k in ('title', 'edition', 'rights_boundary'))
            or not primary_url(book['pdf_url'])
            or ('html_url' in book and not primary_url(book['html_url']))):
        raise ValueError('Exercise work needs pinned primary source, authors and rights boundary')
    if urlsplit(book['pdf_url']).hostname == 'arxiv.org':
        if (not re.fullmatch(r'https://arxiv.org/pdf/\d+\.\d+v[1-9]\d*', book['pdf_url'])
                or book['edition'] != 'arXiv:' + book['pdf_url'].rsplit('/', 1)[1]
                or ('html_url' in book and book['html_url'].split('#', 1)[0] !=
                    book['pdf_url'].replace('/pdf/', '/html/'))):
            raise ValueError('arXiv exercise work needs an exact matching version, not latest')
    for key in ('book_page', 'pdf_page'):
        if type(row[key]) is not int or not 1 <= row[key] <= book['pdf_pages']:
            raise ValueError('Exercise needs explicit one-based page conventions')
    end_keys = {'book_page_end', 'pdf_page_end'}
    if end_keys & row.keys():
        if not end_keys <= row.keys():
            raise ValueError('Exercise page ranges need both printed and PDF end pages')
        for key in ('book_page', 'pdf_page'):
            end = row[key + '_end']
            if type(end) is not int or not row[key] < end <= book['pdf_pages']:
                raise ValueError('Exercise end page must follow its start and be within the source')
    number = row['number']
    if not re.fullmatch(r'[A-Z0-9]+(?:\.[A-Za-z0-9]+)*', number):
        raise ValueError('Invalid source exercise number')
    rel = row['publication_file']
    path = Path(rel)
    if (path.is_absolute() or '..' in path.parts or '\\' in rel
            or not rel.startswith('website/content/publications/') or path.suffix != '.json'):
        raise ValueError('Use a canonical local publication record')
    publication = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    entries = [p for p in publication['items'] if p['id'] == identity]
    if len(entries) != 1:
        raise ValueError('Missing canonical exercise publication')
    item = entries[0]
    if (item['source']['edition'] != book['edition']
            or not re.search(r'\bExercise\s*' + re.escape(number) + r'(?![\w]|\.[A-Za-z0-9])', item['source']['anchor'])
            or str(item['chapter']).lstrip('0') != str(row['chapter']).lstrip('0')):
        raise ValueError('Canonical source edition/number/chapter mismatch')
    parts = {p['id'] for p in item['obligations']}
    sources = []
    covered = set()
    for binding in item['bindings']:
        name = binding['declaration']
        declaration = known.get(name)
        if (declaration is None or declaration.has_placeholder
                or not name.startswith('AutoSamplingTheory.TechnicalLemmas.')
                or not re.fullmatch(r'[A-Za-z0-9_.]+', name)
                or not binding['supports'] or not set(binding['supports']) <= parts
                or not binding['audit_id']):
            raise ValueError('Each exercise part needs actual owned, source-bound declarations')
        covered.update(binding['supports'])
        sources.append({'declaration': name, 'source_file': declaration.source_file,
                        'source_line': declaration.source_line,
                        'source_sha256_lf': bench.text_hash(ROOT / declaration.source_file),
                        'supports': binding['supports'], 'cell': binding['cell'],
                        'audit_id': binding['audit_id'], 'boundary': binding['boundary'],
                        'assumption_deltas': binding['assumption_deltas']})
    if covered != parts:
        raise ValueError('Unmapped source exercise part; partial coverage cannot disappear')
    return {**row, 'book': book, 'source_entry_sha256': bench.sha(bench.encoded(item)),
            'wording_status': 'original faithful mathematical restatement; not reproduced source prose',
            'canonical_source': item['source'], 'source_statement': item['statement'],
            'source_assumptions': item['assumptions'], 'parts': item['obligations'],
            'answer_declarations': sources}


def answers(cores: list[dict]) -> dict:
    """Named owned producers; not fixed Lean questions or new Bench lemmas."""
    return {d['declaration']: d for c in cores if c.get('textbook_exercise')
            for d in c['textbook_exercise']['answer_declarations']}


def compile_contexts(cores: list[dict]) -> dict:
    import sog_bench as bench
    import sog_bench_review as review
    return {name: review.context_binding({
        'source_file': row['source_file'],
        'binding_sha256': bench.sha(bench.encoded({'declaration': name, 'scope': 'owned-answer-module'}))
    }) for name, row in answers(cores).items()}


def probe(cores: list[dict]) -> str:
    records = answers(cores)
    modules = sorted({r['source_file'].removesuffix('.lean').replace('/', '.') for r in records.values()})
    return ('/- Trusted owned exercise-answer audit, not a reconstruction challenge. -/\n'
            + ''.join('import ' + m + '\n' for m in modules) + '\n'
            + ''.join('#check @' + n + '\n#print axioms ' + n + '\n' for n in sorted(records)))


def checked_axioms(output: str, names) -> dict:
    allowed = {'propext', 'Classical.choice', 'Quot.sound'}
    result = {}
    for name in names:
        match = re.search(re.escape(name) + r"'?\s+depends on axioms:\s*\[([^\]]*)\]", output)
        if match:
            axioms = sorted(a.strip() for a in match[1].split(',') if a.strip())
        elif re.search(re.escape(name) + r"'?\s+does not depend on any axioms", output):
            axioms = []
        else:
            raise ValueError('No transitive axiom evidence for named owned answer: ' + name)
        if set(axioms) - allowed:
            raise ValueError('Unapproved axiom in named exercise answer')
        result[name] = axioms
    return result


def source_prompt(exercise: dict) -> dict:
    """Bibliographic context only: no solution, declaration names or part answers."""
    return {'id': exercise['id'], 'title': exercise['book']['title'],
            'authors': exercise['book']['authors'], 'edition': exercise['book']['edition'],
            'exercise': exercise['number'], 'book_page': exercise['book_page'],
            'pdf_page': exercise['pdf_page'],
            **{key: exercise[key] for key in ('book_page_end', 'pdf_page_end') if key in exercise},
            'source_url': exercise['book']['pdf_url'] + '#page=' + str(exercise['pdf_page']),
            'wording_status': exercise['wording_status']}


def projection(cores: list[dict], reviews: dict, compiled: bool) -> list[dict]:
    """Per-question editorial state, source mapping and compile scope stay separate."""
    rows = {}
    for core in cores:
        exercise = core.get('textbook_exercise')
        if not exercise:
            continue
        entry = rows.setdefault(exercise['id'], {
            **exercise, 'questions': [], 'owned_answer_build_recorded': compiled,
            'formal_scope': 'named owned core answers; not full exercise/formal QA certification'})
        entry['questions'].append({'core_id': core['id'],
            'editorial': reviews[core['id']]['editorial'],
            'tracks': core['track_levels']})
    return [rows[key] for key in sorted(rows)]
