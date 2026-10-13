from pathlib import Path
import json,subprocess,hashlib
r=Path('runs/20261007-companion-priority/pbps-real-complex-lift60');load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification60.adoption.json');assert v['native_verified'] and v['verified_commit']==head=='0a77416f5ec38702c46ec1358966b9dd4846c8d3';assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json')
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
out=r/'integration60';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=Path(name);raw=p.read_bytes();q=snap/(hashlib.sha256(name.encode()).hexdigest()+'.exactraw');q.write_bytes(raw);history.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),lf_sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),exact_snapshot=q.as_posix()))
w(out/'owned-before.json',dict(head=head,owned=history))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
entries=[];rows=[]
for i,(key,upstream,tags) in enumerate([('measure.positiveRealL2ComplexLift','ASTIS positive real L2 operator complexification',['L2','positive','complexification','fixed-range']),('pbps.actualPositiveDefectComplexLift','PBPS actual positive squared-defect complex lift',['PBPS','L2','positive','complexification'])]):
 assert key not in s;decl=plan['mathematical_declarations'][i];file=load(r/'claim.json')['proposed_files'][i];note='Independently exact-science60 verified '+head+'. '+('Arbitrary measure real positive bounded D; actual compLpL scalar maps, norm-preserving embedding, full pointwise-conjugation fixed range, actual positive bounded complex lift with literal formula/intertwining/conjugation. Reused by actual PBPS consumer.' if i==0 else 'Original C2, both global Hessian bounds, 0<alpha<=beta, eta>0, beta*eta<=1; actual normalized Gaussian reflected kernel produces same verified59 T and D=1-T*T internally. No caller D/positivity/embedding/CFC certificate. Rank zero extension and alpha*eta=1 retained.')+' Complex-root API test only; real-root preservation/descent/Gamma/B11/polar/fullH1/dynamics/main/error/cost/composition remain open.'
 entries.append('  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(upstream)+'\n    upstreamFile := "arXiv2609.06905v1 AppendixD1/B10-B11; attributed ASTIS background"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n')
 rows.append(dict(key=key,local_decl=decl,local_file=file,status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=upstream,upstream_file='arXiv2609.06905v1 AppendixD/B; ASTIS background completion',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note))
p.write_text(s.replace(anchor,anchor+''.join(entries)),encoding='utf-8',newline='\n')
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:
 for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
for file,anchor,addition in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2PullbackRange','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator','import AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift'),('Tests.lean','import Tests.ProximalBPSCenteredDefect','import Tests.ProximalBPSDefectComplexLift')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 501')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 501','formalizedTechnicalLemmaCount = 503'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS positive complex lift (2026-10-08)

Independently VERIFIED science commit {head}. The canonical shared
Measure/L2RealComplexOperator theorem constructs the actual quotient maps
ofReal/Re/Im/pointwise conjugation on arbitrary-measure real and complex L2.
The embedding preserves norm and has exactly the full conjugation-fixed range.
For a bounded positive real D, the actual complex lift satisfies
Dc g = iota D(Re g) + i iota D(Im g), Dc>=0,
Dc iota = iota D and C Dc = Dc C. No finite/probability measure,
finite-dimensional L2, nontriviality or CFC/root certificate is assumed.

The actual PBPS consumer retains the original C2/global lower and upper
Hessian bounds, 0<alpha<=beta, eta>0 and beta*eta<=1, with the explicit
rank-zero extension. It internally obtains the SAME verified59 stationary
reflected Gaussian S, selfadjoint contractive mean-preserving T and positive
D=I-T^2 on the actual marginal nu, then applies the shared theorem.
Every-y normalized S density, disintegration and both stationary marginals
are conclusions; the operator action is AE. Pointwise C is not operator adjoint.

Root focused3915, independent complete mathematics with all26 private providers,
fresh source/identity-blind decoder and primary-first anti-anchored seven-slot
source/current eight formula steps pass. Diff-aware publication inventories
all26 private providers under the accepted public whole-module owner.
The anonymous Test constructs a COMPLEX positive CFC root with proof-local,
target-typed fixed-Mathlib instances; it proves no real root or descent.

NEXT bounded mathematical edge: show this complex positive root preserves
Fix(C), descend it to a bounded positive REAL scalar Gamma with Gamma^2=D,
and prove ||Gamma u||^2=||u||^2-||T u||^2. This is only a B.11 precursor.
Printed joint Gamma_P additionally requires the SAME canonical M onto ran(P),
transport through that isometry and B=(I-P)UP / B*B identification. Source61
scout confirms these distinct domains; P is identity only on ran(P).
Conjugation of D alone does not prove conjugation of its root.
Centered root lower bound/inverse/polar, weakH1, actual event dynamics,
nonexplosion/invariance, hypocoercivity, mixing, implementation errors and
query costs remain separate. SPHMC/composition actual-input precision and
expected work remain open; TV proximity transfers no unbounded cost.
The older conceptual candidate remains raw/unvalidated; no certified functor
or conceptual Lean implication is added. The four-paper priority is unchanged.

Serialized Registry503/root imports/tests, affected graph/page gates and
repository/exposition seals are still integration work; this entry alone
does not certify MERGED, live publication, PURIFIED, a paper or the Goal.
All earlier source/proof/collaborator checkpoints remain below.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n');p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-positive-complex-lift-2026-10-08';w(p,x)
print('Prepared serialized Registry503/imports/Tests/handoff from independent exact-science60; aggregate gates pending.')
