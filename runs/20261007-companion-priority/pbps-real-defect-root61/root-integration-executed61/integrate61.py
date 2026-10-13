from pathlib import Path
import json,subprocess,hashlib
r=Path('runs/20261007-companion-priority/pbps-real-defect-root61');load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification61.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json')
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
out=r/'integration61';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=Path(name);raw=p.read_bytes();q=snap/(hashlib.sha256(name.encode()).hexdigest()+'.exactraw');q.write_bytes(raw);history.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),lf_sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),exact_snapshot=q.as_posix()))
w(out/'owned-before.json',dict(head=head,owned=history))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
entries=[];rows=[]
for i,(key,upstream,tags) in enumerate([('measure.positiveRealL2SquareRoot','ASTIS genuine positive real L2 square root',['L2','positive','square-root','real-descent']),('pbps.actualPositiveRealDefectRoot','PBPS actual positive real scalar defect root',['PBPS','L2','positive','square-root'])]):
 assert key not in s;decl=plan['mathematical_declarations'][i];file=load(r/'claim.json')['proposed_files'][i]
 note='Independently exact-science61 verified '+head+'. '+('Arbitrary measure and bounded positive real D; actual complex CFC root, conjugated-root positivity and uniqueness establish pointwise conjugation preservation; full fixed-space descent produces bounded positive REAL Gamma, Gamma squared equals D and full-domain quadratic energy. No finite/probability measure, finite L2, nontriviality or caller CFC/root certificate.' if i==0 else 'Original C2, both global Hessian bounds, 0<alpha<=beta, eta>0, beta*eta<=1; genuine every-state normalized reflected Gaussian S, conditional law, stationary marginals and SAME scalar selfadjoint contraction T internally produced. Positive REAL Gamma squared equals I-T*T and every-u normGamma squared equals normu squared minus normTu squared; actual-input Test checks contractivity. Rank zero and alpha*eta=1 retained.')+' Exported real uniqueness, joint GammaP/ontoM/typed B*B, centered root order/inverse/polar, weakH1/dynamics/main/error/cost/composition remain open.'
 entries.append('  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(upstream)+'\n    upstreamFile := "arXiv2609.06905v1 AppendixD1/B10-B11; attributed ASTIS background"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n')
 rows.append(dict(key=key,local_decl=decl,local_file=file,status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=upstream,upstream_file='arXiv2609.06905v1 AppendixD/B; ASTIS background completion',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note))
p.write_text(s.replace(anchor,anchor+''.join(entries)),encoding='utf-8',newline='\n')
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:
 for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
for file,anchor,addition in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.DefectComplexLift','import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot'),('Tests.lean','import Tests.ProximalBPSDefectComplexLift','import Tests.ProximalBPSRealDefectRoot')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 503')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 503','formalizedTechnicalLemmaCount = 505'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS positive real scalar root (2026-10-09)

Independently VERIFIED science commit {head}. Canonical shared
Measure/L2RealSquareRoot constructs a bounded positive REAL Gamma for every
bounded positive real D on arbitrary-measure L2, with Gamma^2=D and
||Gamma u||^2=<Du,u> for every scalar u. Complex CFC is constructed internally;
actual antiunitary pointwise conjugation and complex positive-root uniqueness
prove root preservation of the full real fixed space before descending.
No finite/probability measure, finite-dimensional L2, nontriviality,
caller CFC/root/commutation certificate is assumed.

The actual PBPS consumer retains the original C2, both global Hessian bounds,
0<alpha<=beta, eta>0 and beta*eta<=1, with explicit rank-zero extension and
legal alpha*eta=1. It internally produces the SAME stationary reflected
Gaussian S, selfadjoint contractive mean-preserving T and positive D=I-T^2.
The positive REAL root satisfies ||Gamma u||^2=||u||^2-||T u||^2 for every u;
the genuine original-input Test also checks ||Gamma u||<=||u||.
Every-y normalized S density is distinct from per-observable AE action.

Root and independent focused3916, all10 private providers, fresh anonymous
decoder, primary-first seven-slot source review and nine current formula
proof steps are scoped evidence. This is the full scalar precursor to B.10-B.11.
Printed joint Gamma_P additionally requires the SAME canonical M onto ran(P),
positive-root transport to that closed macro subspace, actual PUP restriction
and typed B*B identity. P is identity only on ran(P), never the full joint space.
Exported real uniqueness and the canonical unique root remain separate.
Centered root order/inverse/polar, weakH1, event dynamics/nonexplosion/invariance,
hypocoercivity, mixing, implementation error and query costs remain separate.
SPHMC/composition actual-input precision and expected work remain open;
TV proximity transfers no unbounded cost. Four-paper priority unchanged.

Earlier complex-lift integration 63c7435 has independently accepted scoped
repository/exposition evidence and all three remote CI workflows terminal
SUCCESS; dense reader layout remains explicitly recorded debt.
Current Registry505/root imports/tests and affected graph/page gates are
serialized integration work. This entry alone certifies no MERGED, live
publication, PURIFIED, completed paper or Goal. All earlier checkpoints remain.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n');p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-positive-real-scalar-root-2026-10-09';w(p,x)
print('Prepared serialized Registry505/imports/Tests/handoff from independently verified exact-science61; aggregate gates pending.')
