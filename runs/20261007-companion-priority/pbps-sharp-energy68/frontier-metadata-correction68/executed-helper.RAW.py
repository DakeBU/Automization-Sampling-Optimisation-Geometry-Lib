from pathlib import Path
import hashlib, json, os, subprocess, sys

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-sharp-energy68'
d = r / 'exact-science-verification'
out = r / 'frontier-metadata-correction68'
old = 'a3191d97ccf78d58c301d024fc86b2a3289fc0a6'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())
def pin(p):
    p = Path(p); b = p.read_bytes(); lf = b.replace(b'\r\n', b'\n')
    return dict(path=p.resolve().as_posix(), raw_bytes=len(b), raw_sha256=sha(b),
                lf_bytes=len(lf), lf_sha256=sha(lf))
def check(q):
    got = pin(q['path'])
    assert all(got[k] == v for k, v in q.items() if k in got), q['path']
def write(p, obj):
    Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')

assert subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip() == old
assert not subprocess.check_output(['git','diff','--cached','--name-only'], text=True).strip()
lease, run, verdict = [load(d/n) for n in ['lease.final.json','run.json','verification-verdict.json']]
assert sha((d/'lease.final.json').read_bytes()) == '21208906347e72e1fc9d16ab56a6a06f93de9e630125d6cb948478c22d448404'
assert lease['status'] == 'CLOSED_LAST' and lease['owned_file_count_including_self'] == 131
assert not lease['VERIFIED'] and verdict['status'] == 'OBSTRUCTED_EXACT_SCI68_NO_VERIFIED'
logical = sha(json.dumps({k:v for k,v in run.items() if k != 'run_sha256'}, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode())
assert logical == run['run_sha256'] == lease['whole_logical_run_sha256'] == '676999ae7353644770660317bd5a3db2e5ee916651281dfb306c942ef6208f66'
assert sha((d/'named-verification.payload.json').read_bytes()) == '8e66006a8bf61ce251c40ce36b7b5c4c11605da998e373895328ac3e6455d06c'
owned = lease['all_owned_outputs_except_only_self']
assert {Path(q['path']).resolve() for q in owned} | {(d/'lease.final.json').resolve()} == {p.resolve() for p in d.rglob('*') if p.is_file()}
for q in owned:
    check(q)
    assert Path(q['path']).stat().st_mtime_ns <= (d/'lease.final.json').stat().st_mtime_ns

p = root/'research-wiki/frontier-cells/ASTIS-SHARED-hilbert-corrector-square-bound.json'
before = p.read_bytes(); cell = json.loads(before)
assert subprocess.check_output(['git','show',old+':'+p.relative_to(root).as_posix()]) == before
assert cell['route'] == 'shared' and cell['shared_floor_audit']['decision'] == 'new_canonical_shared'
assert cell['shared_floor_audit']['classification'] == 'missing'
test = 'Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence'
production = 'AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound'
assert cell['consumers'] == [production] and test in cell['reuse_plan']['known_consumers']
reason = ('Only the PBPS samplewiki-route currently has evidenced consumers: the actual sharp corrector theorem directly consumes this general Hilbert leaf; the compiled modified-energy Test consumes it transitively through that theorem. Both belong to the same paper route. Preserve the stable cell identity and canonical reusable TechnicalLemmas declaration; no second route, duplicate lemma, or cross-domain dependency is claimed.')
cell['route'] = 'samplewiki-route'
cell['shared_floor_audit']['decision'] = 'new_route_local'
cell['shared_floor_audit']['reason'] = reason
cell['consumers'].append(test)
cell['reuse_plan']['decision_reason'] = reason
after = (json.dumps(cell, ensure_ascii=False, indent=2)+'\n').encode()
def diff(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        assert a.keys() == b.keys()
        return [q for k in a for q in diff(a[k],b[k],path+'/'+k)]
    return [] if a == b else [dict(field=path,before=a,after=b)]
changes = diff(json.loads(before), cell)
assert {q['field'] for q in changes} == {'/route','/shared_floor_audit/decision','/shared_floor_audit/reason','/consumers','/reuse_plan/decision_reason'}
out.mkdir(exist_ok=False)
(out/'before.exactraw.snapshot').write_bytes(before)
(out/'after.exactraw.snapshot').write_bytes(after)
(out/'executed-helper.RAW.py').write_bytes(Path(__file__).read_bytes())
write(out/'correction.json', dict(status='METADATA_ONLY_CORRECTION_NOT_YET_VERIFIED',
    science_commit=old, root_pid=os.getpid(), native_obstruction_lease=pin(d/'lease.final.json'),
    native_obstruction_whole_logical_sha256=logical, native_obstruction_owned_files=131,
    source='.agents/skills/astis-substantive-advance/SKILL.md:134',
    policy='new_canonical_shared requires at least two evidenced routes; the Test is the same PBPS route.',
    finite_field_changes=changes, before=pin(out/'before.exactraw.snapshot'), after=pin(out/'after.exactraw.snapshot'),
    no_Lean_publication_lesson_audit_ledger_changes=True, no_VERIFIED_transition=True,
    reusable_general_declaration_retained=True, stable_cell_identity_retained=True))
p.write_bytes(after)
subprocess.run([sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'],check=True)
paths = [p.relative_to(root).as_posix()] + [q.relative_to(root).as_posix() for q in out.iterdir() if q.is_file()]
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],input=('\0'.join(paths)+'\0').encode(),check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines()) == set(paths)
subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Correct PBPS leaf route classification and record actual transitive consumer'],check=True)
print('PASS metadata-only SCI68B',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(), 'five finite fields; old obstruction unchanged; independent corrected-commit verification pending.')
