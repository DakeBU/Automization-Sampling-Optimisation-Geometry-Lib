from pathlib import Path
import hashlib,json,subprocess,os
r=Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
pre=Path('runs/20261007-companion-priority/pbps-reflection-rotation-preproof69')
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.actual_reflection_intertwining'
f=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean')
text=f.read_text(encoding='utf-8'); sealed=(pre/'statement0.definition.lean').read_text(encoding='utf-8').rstrip()
assert sealed in text
assert (pre/'header0-public.lean').read_text(encoding='utf-8').rstrip()+' := by' in text
assert text.count('private def ')==1 and 'sorry' not in text and 'admit' not in text
success=load(r/'focused69-v2/receipt.json');assert success['exit_code']==0 and success['terminal_closed']
log=(r/'focused69-v2/stdout.log').read_text(encoding='utf-8')
assert 'Build completed successfully (3948 jobs).' in log
axioms=log[log.index("'"+decl+"' depends on axioms:"):]
assert all(x in axioms for x in ['propext','Classical.choice','Quot.sound']) and 'sorryAx' not in axioms
names=[f,Path('lean-toolchain'),Path('lake-manifest.json'),
       Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean'),
       Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionL2.lean'),
       Path('AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean'),
       pre/'root.statement-seal69.json',pre/'root.header69.adoption.json',pre/'root.primary69.adoption.json',
       pre/'header0-expanded.lean',pre/'statement0.definition.lean',pre/'header0-public.lean',
       pre/'independent-primary69/source-proof-graph.json',pre/'independent-primary69/source-coverage-inventory.json',
       pre/'independent-primary69/primary-source-expectation-payload.json',
       pre/'independent-header-source69/binder-and-definition-audit.json',
       pre/'root.library-retrieval69.json',pre/'root.library-retrieval69.extension.json',
       r/'focused69-v1/receipt.json',r/'focused69-v2/receipt.json',r/'focused69-v2/stdout.log',r/'focused69-v2/stderr.log']
rows=[]
for p in names:
 b=p.read_bytes();rows.append(dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n'))))
payload=dict(schema='frozen-theorem-only69-before-independent-math-v1',actual_root_pid=os.getpid(),
 checked_base_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
 advance_id='ASTIS-SA-20261009-PBPSActualReflectionIntertwining',declaration=decl,inputs=rows,
 exact_private_Prop_unchanged=True,exact_public_original_callers_unchanged=True,
 focused=dict(actual_PID=success['actual_foreground_pid'],exit_code=0,jobs=3948,axioms=['propext','Classical.choice','Quot.sound']),
 theorem_delta='SAME actual full micro-space compression D=R U inclusion and V0*D=-A0 V0*, preserving all original parent witnesses/conclusions.',
 typed_negative=dict(fingerprint='giant-dependent-witness-rw/adjoint-definition',failure_class='API_BLOCKED',
 residual='v1 timed out at rewrite hVdef/adjoint_comp on line352; no mathematical failure inferred.',
 strict_reduction='v2 uses explicit typed local equality and congrArg/calc, same Statement Seal and heartbeat2M; full target compiles.',
 retired_route='Broad rw of implicit giant dependent hVdef; do not retry unchanged.'),
 remaining_boundary='B21 actual projected rotation/corrector change, B4 dynamics, H1, invariance/nonexplosion, main, implementation errors/caps, expected costs and actual-input composition remain separate.',
 source_review=False,independently_verified=False,integrated=False,full_paper=False,Goal_complete=False)
dest=r/'math-freeze.theorem-only69.json';assert not dest.exists()
dest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS sealed original-input theorem69 frozen for independent math;22 precise inputs, proof bytes will remain unchanged.')
