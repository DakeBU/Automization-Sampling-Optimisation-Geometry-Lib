from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
d=r/'compiler-diagnosis70';p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean')
s=p.read_text(encoding='utf-8');t=s.index('theorem actual_projected_rotation');a=s.index('    let μ :=',t);b=s.index(' := by\n',a)
old=s[t:b];result=s[a:b].rstrip()
new=s[t:a]+'    (show Prop from\n'+'\n'.join('  '+line for line in result.splitlines())+'\n    )'
q=d/'header-type-ascription70.proposed.lean';assert not q.exists();q.write_text(new+'\n',encoding='utf-8',newline='\n')
q2=Path('.astis/pbps-actual-rotation70/diagnostic-type-ascription70.lean');assert not q2.exists()
out=s[:t]+new+s[b:];q2.write_text(out,encoding='utf-8',newline='\n')
sha=lambda x:hashlib.sha256(x).hexdigest()
(d/'header-type-ascription70.proposal.json').write_text(json.dumps(dict(
 status='PROPOSED_COMPILER_TYPE_ASCRIPTION_ONLY_NOT_APPLIED',actual_root_PID=os.getpid(),
 exact_sealed_header='runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/header0-proposed-expanded.lean',
 proposed_header=q.as_posix(),proposed_header_RAW_sha256=sha(q.read_bytes()),
 original_header_RAW_sha256=sha((old+'\n').encode()),
 diagnostic_file=q2.as_posix(),production_file_unchanged=True,
 proof_BODY_RAW_sha256=sha(s[b+len(' := by\n'):].encode()),
 recipe='Wrap the same entire public result in (show Prop from ...); indent result by two spaces. No binder, formula, witness, operator, premise or conclusion changes.',
 rationale='Unknown free variable occurs before any trace tactic. Earlier independently compiled header used a def with expected Prop; bare theorem return-type elaboration differs.',
 no_private_Prop_or_provider=True,mathematical_statement_repair=False,
 independent_math_and_source_review_pending=True,no_compiled_theorem_credit=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Proposed explicit Prop ascription preserving all sealed public tokens and exact BODY; canonical file unchanged.')
