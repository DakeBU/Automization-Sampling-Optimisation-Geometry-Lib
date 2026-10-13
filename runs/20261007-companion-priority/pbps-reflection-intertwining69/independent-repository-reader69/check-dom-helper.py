import json, os, pathlib, sys
sys.dont_write_bytecode = True
from compare_bounded_dom import compare
out = pathlib.Path(__file__).resolve().parent
expected = json.loads((out/'expected-code-and-reader-payload.before-final-packet.json').read_text(encoding='utf-8'))
result = compare((out/'expected-three-code-panels.preview.html').read_text(encoding='utf-8'), expected)
assert result['scoped_panel_count'] == 3
assert all(x['exact'] for x in result['panel_checks'])
assert result['helper_nested_in_public_proof']
record = dict(schema='bounded-dom-helper-selfcheck-v1', actual_pid=os.getpid(),
    three_code_panels_exact=True, nested_private_helper_exact=True,
    only_owned_preview_examined=True, no_current_reader_acceptance=True)
(out/'bounded-dom-helper-selfcheck.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,sort_keys=True))
