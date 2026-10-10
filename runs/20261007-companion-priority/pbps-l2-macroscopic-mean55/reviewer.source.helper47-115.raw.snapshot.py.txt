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
