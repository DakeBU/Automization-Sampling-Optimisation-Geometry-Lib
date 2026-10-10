from pathlib import Path
import json,hashlib,datetime,subprocess,sys,os,re
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79/independent-math79'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean'
frozen=load(O/'input-freeze79.json')['inputs']
for e in frozen:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
save('dependency-probe1-diagnosis79.json',dict(classification='VERIFIER_OPAQUE_THEOREM_INSPECTION_API',
 finding='Fresh exact complete source theorem and #print axioms succeeded, but appended metadata probe used ci.value? default allowOpaque=false and therefore rejected a theorem. Pinned Declaration.lean line483 documents ci.value? true for theorem values. New immutable probe enables this flag only.',
 original_receipt=info(O/'fresh-whole-module.receipt.json'),production_changed=False,statement_changed=False))
first=(O/'FreshWholeModuleAxiomsDependencies79.lean').read_bytes();second=first.replace(b'ci.value? |',b'ci.value? true |');assert second!=first
probe=O/'FreshWholeModuleAxiomsDependencies79.allowOpaque.lean';assert not probe.exists();probe.write_bytes(second)
assert second.startswith(M.read_bytes())
inputs=[info(Path(e['path'])) for e in frozen]+[info(probe)]
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(probe)]
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'fresh-whole-module-attempt2.stdout.log').open('xb') as out,(O/'fresh-whole-module-attempt2.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print('Fresh full-source corrected dependency probe foreground PID',child.pid,flush=True);code=child.wait()
save('fresh-whole-module-attempt2.receipt.json',dict(command=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,
 started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),inputs=inputs,
 stdout=info(O/'fresh-whole-module-attempt2.stdout.log'),stderr=info(O/'fresh-whole-module-attempt2.stderr.log'),
 full_source_prefix_exact=True,canonical_olean_written=False,native_reasoning_trajectory_claimed=False))
print('FRESH FULL SOURCE ATTEMPT2 EXIT',code,flush=True)
assert code==0
log=(O/'fresh-whole-module-attempt2.stdout.log').read_text(encoding='utf-8')
a=re.search(r'depends on axioms:\s*\[([^\]]+)\]',log,re.S);assert a
names=[x.strip() for x in a.group(1).split(',')];assert set(names)=={'propext','Classical.choice','Quot.sound'}
deps=re.findall(r'ASTIS_DIRECT_DEPENDENCY (\S+)',log)
expected=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation.actual_fixed_reference_event_time_nonaccumulation']
assert set(deps)==set(expected),deps
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits()
save('fake-closure-scan79.json',dict(reviewer='/root/exact_verify77',algorithm='tools.astis.forbidden_pattern_hits same production scan as astis.py check',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M),aggregate_Lake_gate_not_run=True))
assert not hits
for e in inputs:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
save('fresh-compiler-dependency-summary79.json',dict(status='PASS_FULL_SOURCE_STANDARD_THREE_EXACT_ACTUAL_PARENTS',module=info(M),axioms=names,
 direct_ASTIS_dependencies=deps,public_stochastic_provider_premises=[],receipt=info(O/'fresh-whole-module-attempt2.receipt.json'),
 direct_unused_import='UnitExponentialProduct imported explicitly but no direct BODY dependency; actual78 already supplies input-event escape. Optional later import cleanup only.',
 fake_closure_scan=info(O/'fake-closure-scan79.json'),proof_reviewer='/root/exact_verify77',source_review=False,VERIFIED=False,Goal_complete=False))
print('FRESH ELABORATION / AXIOMS / ACTUAL DEPENDENCIES / FAKECLOSURE PASS',flush=True)
