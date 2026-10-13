from pathlib import Path
import base64, hashlib, json, os, subprocess, sys

r = Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
o = r/'independent-repository-reader69'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode()
lf = lambda b: b.replace(b'\r\n',b'\n')
def check(p, z):
    b = Path(p).read_bytes()
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], p
    if z['LF_recipe'].startswith('not applicable'):
        assert z.get('LF_bytes') is None and z.get('LF_sha256') is None
    else:
        assert len(lf(b)) == z['LF_bytes'] and sha(lf(b)) == z['LF_sha256'], p
    return b

lease = load(o/'lease.final.json')
assert sha((o/'lease.final.json').read_bytes()) == '9526ce7abb2b52e5a090dc33f60a8236bf1ad648d49f204b56bee746242184de'
assert lease['status'] == 'CLOSED_LAST' and lease['last_owned_write']
assert lease['owner'] == '/root/independent_primary69'
m = load(o/'manifest.final.json')
assert sha((o/'manifest.final.json').read_bytes()) == lease['manifest_RAW_sha256'] == '7f983589f3edaf4a148fcd456aa44c76b959f46eb474e143b609dd3e2cc05dff'
rows = m['entries']; assert len(rows) == m['regular_file_count'] == 333
assert sha(canonical(rows)) == lease['finite_owned_closure_sha256'] == 'e424f57b3796d4b9c446fbc5068b0e6073d877e6ca00444279f2557500eccba6'
actual = {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}
assert actual == {z['name'] for z in rows} | {'manifest.final.json','lease.final.json'}
assert len(actual) == lease['owned_file_count'] == 335
last = (o/'lease.final.json').stat().st_mtime_ns
for z in rows:
    p = o/z['name']; check(p,z); assert p.stat().st_mtime_ns <= last, p
assert (o/'manifest.final.json').stat().st_mtime_ns <= last
run = load(o/'review-run.json'); h = run.pop('run_sha256')
assert sha(canonical(run)) == h == lease['whole_logical_run_sha256'] == 'a1c83bdd11ccafd04eff0d19226384a432c36a4178d1e92b5f918244b8631b6a'
for key in ['COMPLETE_NAMED_DECISION','COMPLETE_NAMED_REVIEW_DECISION_INPUT',
            'COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_LF_INPUT','FINITE_REVIEW_COVERAGE']:
    z = lease[key]; check(o/z['name'],z)
inputs = load(o/'RAW-input-payload.json')['inputs']; assert len(inputs) == 132
for row in inputs:
    a,z = row['attribution'],row['payload']; b = base64.b64decode(z['RAW_base64'])
    assert len(b) == z['RAW_bytes'] == a['RAW_bytes']
    assert sha(b) == z['RAW_sha256'] == a['RAW_sha256']
    assert Path(a['original_path']).read_bytes() == b, a['name']
    if z['binary']: assert 'LF_base64' not in z
    else: assert base64.b64decode(z['LF_base64']) == lf(b)
d = load(o/'repository-reader69.decision.json')
head = subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip()
assert head == d['checked_science_commit'] == lease['checked_science_commit'] == '2d286c283a6fb5dfc13180204bb0da54531a5c67'
assert d['verdict'] == 'ACCEPT_LOCAL_REPOSITORY_AND_SCOPED_READER69'
assert not d['blocking_findings'] and not d['required_repairs'] and len(d['checks']) == 13
assert all(z['decision'] == 'PASS_BOUNDED' for z in d['checks'])
for key in ['repository_aggregate','scoped_reader','current_affected_graph']: assert d['scope'][key]
for key in ['Goal_complete','PURIFIED','full_Exposition_Seal','live','main','wholepaper','new_mathematical_source_verdict']: assert not d['scope'][key]
cp = Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-reflection-intertwining.json')
assert sha(cp.read_bytes()) == d['final_cell_RAW_sha256']
assert sha(Path('_site/data/underlying-lean-graph.json').read_bytes()) == d['final_graph_RAW_sha256']
assert sha((r/'final-reader-repository-packet69.json').read_bytes()) == d['final_root_packet_RAW_sha256']
sys.path.insert(0,str(Path('tools').resolve()))
sys.path.insert(0,str(Path('website/scripts').resolve())); import publication_reader
assert publication_reader.graph_input_digest() == d['current_publication_inputs_sha256']
dest = r/'root.repository69.adoption.json'; assert not dest.exists()
payload = dict(status='NATIVE_REPOSITORY_READER69_ADOPTED', actual_root_PID=os.getpid(),
    accepted_scoped_aggregate=True, accepted_current_graph=True, exact_science_commit=head,
    native_owned_files=335, current_inputs=108, complete_named_inputs=132,
    whole_logical_run_sha256=h, native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
    native_complete_named_RAW_sha256=lease['COMPLETE_NAMED_REVIEW_DECISION_INPUT']['RAW_sha256'],
    native_verdict=d['verdict'], retained_nonblocking_observations=d['nonblocking_observations'],
    native_files_mutated=False, zero_postclose_owned_writes=True,
    retained_root_adapter_negative='integration69/adopt-native-repository-reader PID34780 EXIT1: missing tools import path; all preceding335/132 native checks passed; no adoption or native write occurred.',
    native_LF_recipe='Text:CRLF to LF only; binary:RAW only. Root packet binary LF projection is not native binary semantics.',
    aggregate=True, scoped_reader=True, full_Exposition_Seal=False, PURIFIED=False,
    main_live=False, full_paper=False, Goal_complete=False)
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact native CLOSED335 adopted;108 current/132 named inputs;13 bounded checks; no full paper claim.')
