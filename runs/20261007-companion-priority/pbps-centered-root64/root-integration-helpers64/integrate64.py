from pathlib import Path
import json,subprocess,hashlib
r=Path('runs/20261007-companion-priority/pbps-centered-root64');load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification64.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json');claim=load(r/'claim.json')
owned=['AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
out=r/'integration64';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=Path(name);raw=p.read_bytes();q=snap/(hashlib.sha256(name.encode()).hexdigest()+'.exactraw');q.write_bytes(raw);history.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),lf_sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),exact_snapshot=q.as_posix()))
w(out/'owned-before.json',dict(head=head,owned=history))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
descriptions=[('measure.realL2PositiveSquareOrder','Arbitrary real L2 positive square order','PBPS arXiv2609.06905v1 D1 order/root background; ASTIS internal complexification completion',['L2','positive','operator','square-order'],'Arbitrary measure and real scalar-valued L2: positive A,B with positive B squared-A squared internally yield positive B-A, using three canonical complex lifts and internal complex CFC. No caller CFC/nontriviality/finite-L2 premise; zero/trivial case included. Genuine consumer is actual PBPS B15 centered root order.'),('pbps.actualCenteredRootOrderInverse','Actual PBPS centered root order and bounded inverse','arXiv2609.06905v1 B15; C2/C3/C4; B16 actual input',['PBPS','L2','centered','root-order','bounded-inverse'],'Original C2/two global Hessian bounds,0<alpha<=beta,eta>0,betaeta<=1. SAME actual laws/e/U/T/GammaP, compact-gradient closure and literal conditional action internally give C4 sharp contraction, GammaP0 >= gamma I with gamma=2sqrt(alphaeta)/(1+alphaeta), exact HP0=ker inner(e1,.), unit, both inverse cancellations and norm inverse<=1/gamma. Rank0/alphaeta=1 retained. Full-space inverse excluded; completed polar, H1/B13/B14, dynamics/main/error/cost/composition remain open.')]
entries=[]
for i,(key,title,source,tags,note0) in enumerate(descriptions):
 assert key not in s;decl=plan['mathematical_declarations'][i];file=claim['proposed_files'][i];note='Independently exact-science64 verified '+head+'. '+note0
 entries.append('  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(title)+'\n    upstreamFile := '+json.dumps(source)+'\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n')
 row=dict(key=key,local_decl=decl,local_file=file,status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=title,upstream_file=source,verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note)
 with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
p.write_text(s.replace(anchor,anchor+''.join(entries)),encoding='utf-8',newline='\n')
for file,anchor,addition in [('AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareRootUnique','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder'),('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot','import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse'),('Tests.lean','import Tests.ProximalBPSMacroscopicDefectRoot','import Tests.ProximalBPSCenteredRootOrderInverse')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 508')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 508','formalizedTechnicalLemmaCount = 510'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS centered root order and bounded inverse (2026-10-09)

Independently VERIFIED science commit {head}. Original C2/two global Hessian
bounds and positive capped eta internally yield the printed B15 operator order
Gamma0 >= gamma I on the SAME exact complete HP0=ker inner(e1,.), where
gamma=2sqrt(alpha eta)/(1+alpha eta)>0. Both inverse cancellations and the
bounded inverse norm <=1/gamma are conclusions. Canonical actual laws/e/U/T
and SAME GammaP are retained. Rank0 and alphaeta=1 remain legal.

Canonical arbitrary-real-L2 positive square order has a genuine actual B15
consumer. The actual C4 estimate joins the SAME compact-gradient closure from
RoughMeanGradient and GaussianMarginalPoincare; no gap/root/onto/unit certificate
became a public premise. Test derives norm preservation and ker P membership
of normalized actual leakage directly from original inputs.

Next: B16 polar map from HP0 into the exact closed microscopic complement,
its factorization and V.adjoint composed V=I. No surjectivity onto the whole
microscopic space is claimed. H1/B13/B14, events/nonexplosion/invariance,
hypocoercivity/main mixing, implementation errors and actual-input expected
query costs/PBPS-SPHMC composition remain separate. Gaussian Cloud then midpoint
follow the existing four-paper priority. TV proximity transfers no unbounded cost.

Previous integration ee6bdf2 has independent scoped repository/reader admission
and all GitHub workflows terminal SUCCESS. Serialized Registry510/imports/Tests
and affected reader/graph gates remain pending below. No merged/live/PURIFIED,
full paper or whole Goal completion. Earlier checkpoints are preserved.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n')
p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-centered-root-order-and-bounded-inverse-2026-10-09';w(p,x)
print('Prepared serialized Registry510/imports/Tests/handoff from independently verified science64; full aggregate and reader/graph gates pending.')
