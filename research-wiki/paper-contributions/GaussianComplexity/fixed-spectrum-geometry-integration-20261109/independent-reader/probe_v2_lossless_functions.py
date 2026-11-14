"""FIXTURE ONLY: extract pure helpers; never execute application/sourceV/lifecycle code."""
from pathlib import Path
import ast, gzip, hashlib, json
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O = S / 'application-helper-review-v2'
assert not O.exists()
p = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/apply_reviewed_shared_v2.py'
raw = p.read_bytes(); sha = lambda b: hashlib.sha256(b).hexdigest()
assert sha(raw) == '6589347d7588d7932c8f6330c1a3809afe41864f6b9a1dc7a8d60265da31e9f9'
tree = ast.parse(raw)
names = {'rows', 'differences', 'spans', 'append_integration'}
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
assert {n.name for n in nodes} == names
namespace = {'json': json}
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<extracted-pure-functions-only>', 'exec'), namespace)
assert not any(n.name == 'baseline_check' for n in nodes)
original = (R / 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json').read_bytes()
metadata = {'state': 'FIXTURE_ONLY_NOT_ACTUAL_SOURCEV_OR_STAB', 'Unicode': 'κ, θ, 研究',
            'nested': {'claim': False, 'strings': ['quote"', 'backslash\\', 'newline\n']}}
fixtures = {'actual-candidate-raw-copy-only': original,
            'synthetic-all-CRLF': original.replace(b'\n', b'\r\n'),
            'synthetic-mixed-EOL': b'{\r\n  "evidence": {\n    "old": {"proof": "\\u03ba", "array": [1, {"key": true}]}\r\n  },\n  "tail": "stable"\r\n}\n',
            'synthetic-minified': b'{"evidence":{"x":1},"other":"unchanged"}',
            'synthetic-array-last': b'{\n "evidence": {"x": true, "old": [1,2,{"a":"b"}]}, "end": 3\n}\n'}
results = []
O.mkdir()
for name, data in fixtures.items():
    result, insertion = namespace['append_integration'](data, metadata)
    offset = insertion['character_insertion_offset']; added = insertion['inserted_text']
    inverse = (result.decode()[:offset] + result.decode()[offset + len(added):]).encode()
    assert inverse == data and insertion['inverse_restores_exact_before']
    assert namespace['differences'](json.loads(data), json.loads(result)) == ['/evidence/canonical_integration']
    parsed = json.loads(result); assert parsed['evidence'].pop('canonical_integration') == metadata
    assert parsed == json.loads(data)
    for suffix, content in [('before', data), ('after', result)]:
        (O / (name + '.' + suffix + '.FIXTURE.raw.json.gz')).write_bytes(gzip.compress(content, mtime=0))
    results.append({'name': name, 'scope': 'Explicit synthetic/candidate-copy fixture only; no actual accepted sourceV or STAB',
                    'before_sha256': sha(data), 'after_sha256': sha(result), 'inverse_exact': True,
                    'only_new_JSON_path': '/evidence/canonical_integration',
                    'old_CRLF_bytes_preserved_by_inverse': data.count(b'\r\n')})
negative = [b'{"evidence":{}}', b'{"evidence":{"canonical_integration":{"old":true}}}']
for data in negative:
    try:
        namespace['append_integration'](data, metadata)
    except AssertionError:
        pass
    else:
        raise AssertionError('Expected refusal of empty evidence or old canonical object')
valid_rows = b'{"event":"FIXTURE_ONLY"}\n'
assert namespace['rows'](valid_rows) == [{'event': 'FIXTURE_ONLY'}]
for data in [b'', b'{"event":"FIXTURE_ONLY"}', b'[]\n', valid_rows + b'\n']:
    try:
        namespace['rows'](data)
    except (AssertionError, json.JSONDecodeError):
        pass
    else:
        raise AssertionError('Expected incomplete/blank/non-object JSONL refusal')
record = {'state': 'PURE_HELPER_FIXTURES_ONLY_PASS', 'reviewed_helper_sha256': sha(raw),
          'extracted_function_names': sorted(names), 'fixture_cases': results,
          'refuses_old_canonical_overwrite_and_empty_evidence': True,
          'raw_rows_complete_newline_nonblank_object_guards': True,
          'original_main_application_executed': False, 'sourceV_fixture_treated_as_real': False,
          'shared_files_mutated': False}
(O / 'pure-helper-fixture-report.json').write_bytes((json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode())
(O / 'helper-v2.original.raw.py.gz').write_bytes(gzip.compress(raw, mtime=0))
(O / 'fixture-driver.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
assert p.read_bytes() == raw
print(json.dumps({'state': record['state'], 'report_sha256': sha((O / 'pure-helper-fixture-report.json').read_bytes()),
                  'fixtures': len(fixtures), 'application_executed': False}, indent=2))
