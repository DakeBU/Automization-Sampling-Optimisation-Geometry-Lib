from pathlib import Path
import hashlib,json,os

r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
d=r/'compiler-diagnosis70'
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean')
s=p.read_text(encoding='utf-8')
t=s.index('theorem actual_projected_rotation')
a=s.index('    let μ :=',t)
b=s.index(' := by\n',a)
sealed=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/header0-proposed-expanded.lean')
assert sealed.read_text(encoding='utf-8')==s[t:b]+'\n'
name='actual_projected_rotation_statement'
binders=s[t:a]
definition=binders.replace('theorem actual_projected_rotation','private def '+name,1).rstrip()+' Prop :=\n'+s[a:b]
theorem=binders.rstrip()+' '+name+' (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη'
new=s[:t]+definition+'\n\n'+theorem+s[b:].replace(' := by\n  classical',' := by\n  unfold '+name+'\n  classical',1)
q=d/'header-named-literal70.proposed.lean'
q2=Path('.astis/pbps-actual-rotation70/diagnostic-named-literal70.lean')
assert not q.exists() and not q2.exists()
q.write_text(definition+'\n\n'+theorem+'\n',encoding='utf-8',newline='\n')
q2.write_text(new,encoding='utf-8',newline='\n')
sha=lambda x:hashlib.sha256(x).hexdigest()
origins=[Path('.astis/pbps-ambient-adjoint66/apply-private-statement66.py'),
 Path('runs/20261007-companion-priority/pbps-ambient-adjoint66/elaboration-boundary66.diagnosis.json'),
 Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66/independent-type-diagnosis66/diagnosis-summary.json'),
 Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean')]
pins=[]
for i,x in enumerate(origins):
 z=x.read_bytes(); snap=d/f'named-literal-reuse-origin{i}.exactraw.snapshot'; assert not snap.exists();snap.write_bytes(z)
 pins.append(dict(path=x.as_posix(),RAW_sha256=sha(z),RAW_bytes=len(z),snapshot=snap.as_posix()))
(d/'header-named-literal70.proposal.json').write_text(json.dumps(dict(
 status='PROPOSED_LITERAL_STATEMENT_REPRESENTATION_NOT_APPLIED',actual_root_PID=os.getpid(),
 sealed_header=sealed.as_posix(),sealed_RAW_sha256=sha(sealed.read_bytes()),
 proposed_header=q.as_posix(),proposed_RAW_sha256=sha(q.read_bytes()),
 diagnostic_file=q2.as_posix(),diagnostic_RAW_sha256=sha(q2.read_bytes()),
 production_unchanged_RAW_sha256=sha(p.read_bytes()),
 recipe='Exact sealed result is the value of one private Prop-valued definition with identical original binders. Public theorem takes identical binders and asserts that literal value; BODY only gains unfold. No mathematical provider or extra premise.',
 reused_retired_inline_routes=pins,
 diagnosis='66 independently diagnosed identical dependent-type generalization failure and retired direct/id/show/async inline routes; 69 already uses reviewed literal statement representation. Stop repeating these routes in70.',
 public_inline_syntax_changed=True,public_semantic_statement_changed=False,
 all_formulas_and_witnesses_preserved=True,reader_requires_full_literal_statement_adjacent_fold=True,
 independent_math_and_source_review_pending=True,no_compiled_theorem_credit=True),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact named literal candidate prepared; previous66 retired-route diagnosis reused; canonical unchanged.')
