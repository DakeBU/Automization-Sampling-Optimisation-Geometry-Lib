from pathlib import Path
import json,subprocess,hashlib
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification62.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json')
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
out=r/'integration62';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=Path(name);raw=p.read_bytes();q=snap/(hashlib.sha256(name.encode()).hexdigest()+'.exactraw');q.write_bytes(raw);history.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),lf_sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),exact_snapshot=q.as_posix()))
w(out/'owned-before.json',dict(head=head,owned=history))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
entries=[];rows=[]
for i,(key,upstream,tags) in enumerate([('measure.positiveRealL2SquareRootUnique','ASTIS positive real L2 square-root uniqueness',['L2','positive','square-root','uniqueness']),('pbps.actualUniquePositiveRealDefectRoot','PBPS actual unique positive real scalar defect root',['PBPS','L2','positive','square-root','uniqueness'])]):
 assert key not in s;decl=plan['mathematical_declarations'][i];file=load(r/'claim.json')['proposed_files'][i]
 note='Independently exact-science62 verified '+head+'. '+('On arbitrary-measure real L2, bounded positive A/B with equal squares are equal. Canonical complex lifts and actual complex positive-root uniqueness descend through the isometric real embedding. No finite/probability measure, finite L2, nontriviality or caller CFC certificate.' if i==0 else 'Original C2/two global Hessian bounds,0<alpha<=beta,eta>0,betaeta<=1 internally produce SAME stationary reflected S/T/D and positive REAL root Gamma. ALL positive alternative roots with same square equal Gamma; their energy is not a premise. Quantifier lies outside every-u energy. Genuine actual-input Test checks alternative-root contractivity. Rank zero and alphaeta=1 retained.')+' Printed joint GammaP/ontoM/typed B*B, centered order/inverse/polar,H1/dynamics/main/error/cost/composition remain open.'
 entries.append('  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(upstream)+'\n    upstreamFile := "arXiv2609.06905v1 AppendixD1/B10-B11; attributed ASTIS background"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n')
 rows.append(dict(key=key,local_decl=decl,local_file=file,status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=upstream,upstream_file='arXiv2609.06905v1 AppendixD/B; ASTIS background completion',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note))
p.write_text(s.replace(anchor,anchor+''.join(entries)),encoding='utf-8',newline='\n')
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:
 for row in rows:f.write(json.dumps(row,ensure_ascii=False)+'\n')
for file,anchor,addition in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRoot','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRoot','import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique'),('Tests.lean','import Tests.ProximalBPSRealDefectRoot','import Tests.ProximalBPSRealDefectRootUnique')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 505')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 505','formalizedTechnicalLemmaCount = 507'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS unique positive real scalar root (2026-10-09)

Independently VERIFIED science commit {head}. Shared Measure/L2RealSquareRootUnique
proves that bounded positive REAL operators A,B on the SAME arbitrary-measure L2
with A*A=B*B are equal. Canonical complex lifts, complex positive-root uniqueness
and real isometry injectivity supply the proof. No finite/probability measure,
finite L2, Nontrivial or caller CFC/root/energy certificate is assumed.

The actual PBPS consumer retains C2, both global Hessian bounds,0<alpha<=beta,
eta>0,betaeta<=1, rank-zero extension and legal alphaeta=1. It produces SAME
stationary reflected S/T/D and positive REAL Gamma from original inputs, then
proves ALL positive alternative same-square roots equal Gamma. This universal
quantifier is outside the every-u energy and assumes no alternative energy.
Root520 and independent3700 focused3918, zero private providers, fresh anonymous
decoder, primary-first seven-slot source/current seven formula steps pass.
Exact science verification remains separate from aggregate/reader/remote CI.

NEXT selected mathematical edge is the genuine printed macro B10/B11: canonical
M onto exact lpMeas=ran(P), same U/T identification, transport via e and typed
B_macro.adjoint composed B_macro. I_H_P-A_macro^2 holds on H_P; fulljoint defect
is P-A_joint^2. No fulljoint identity substitution or caller completeness.
Centered root lower order/inverse/polar, H1/dynamics/nonexplosion/invariance,
hypocoercivity/main/implementation errors/costs remain separate. SPHMC and
actual-input precision/expected-query-cost composition remain open;
TV proximity transfers no unbounded cost. Four-paper priority unchanged.

Previous scalar-root integration d1b150d has independently accepted scoped
repository/exposition evidence and all three remote CI workflows terminal SUCCESS.
Copy-tail and dense graph layout debts remain explicitly recorded. Registry507/
imports/Tests and affected reader/graph admission are serialized work below.
No MERGED/live/PURIFIED/full-paper/Goal claim. All earlier checkpoints preserved.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n');p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-unique-positive-real-scalar-root-2026-10-09';w(p,x)
print('Prepared serialized Registry507/imports/Tests/handoff from independently verified exact-science62; aggregate gates pending.')
