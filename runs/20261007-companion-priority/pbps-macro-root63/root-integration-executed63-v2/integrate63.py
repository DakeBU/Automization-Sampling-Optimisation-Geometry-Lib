from pathlib import Path
import json,subprocess,hashlib
r=Path('runs/20261007-companion-priority/pbps-macro-root63');load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification63.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();plan=load(r/'publication-plan.json')
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
out=r/'integration63';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=Path(name);raw=p.read_bytes();q=snap/(hashlib.sha256(name.encode()).hexdigest()+'.exactraw');q.write_bytes(raw);history.append(dict(path=name,raw_sha256=hashlib.sha256(raw).hexdigest(),lf_sha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest(),exact_snapshot=q.as_posix()))
w(out/'owned-before.json',dict(head=head,owned=history))
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');s=p.read_text(encoding='utf-8');anchor='def measureMemory : List LemmaMemoryEntry := [\n';assert s.count(anchor)==1
key='pbps.actualUniquePositiveMacroscopicDefectRoot';assert key not in s;decl=plan['mathematical_declarations'][0];file=load(r/'claim.json')['proposed_files'][0];tags=['PBPS','L2','macroscopic','square-root','Gram','uniqueness']
note='Independently exact-science63 verified '+head+'. Original C2/two global Hessian bounds,0<alpha<=beta,eta>0,betaeta<=1 internally produce SAME stationary reflected S/T/U, canonical M onto complete HP=lpMeas=ran(P), and scalar positive root transported by SAME e. A=e T e^-1, typed leakage B:HP-to-joint, GammaP^2=I_HP-A^2=B.adjoint composed B, norm/energy for EVERY macro class and ALL positive same-square macro uniqueness without alternative energy. Rank0 and alphaeta=1 retained. Fulljoint Gram remains P-AJ^2. Other B5, centered root order/inverse/polar,H1/dynamics/main/error/cost/composition remain open.'
entry='  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := "PBPS actual unique positive macroscopic defect root and typed Gram"\n    upstreamFile := "arXiv2609.06905v1 AppendixB1-B5 first Gram/B10-B11; attributed ASTIS completion"\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n'
p.write_text(s.replace(anchor,anchor+entry),encoding='utf-8',newline='\n')
row=dict(key=key,local_decl=decl,local_file=file,status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl='PBPS actual unique positive macroscopic defect root and typed Gram',upstream_file='arXiv2609.06905v1 AppendixB1-B5 first Gram/B10-B11; ASTIS background completion',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note)
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('a',encoding='utf-8',newline='\n') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
for file,anchor,addition in [('AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.RealDefectRootUnique','import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot'),('Tests.lean','import Tests.ProximalBPSRealDefectRootUnique','import Tests.ProximalBPSMacroscopicDefectRoot')]:
 p=Path(file);s=p.read_text(encoding='utf-8');assert s.count(anchor+'\n')==1 and addition not in s;p.write_text(s.replace(anchor+'\n',anchor+'\n'+addition+'\n'),encoding='utf-8',newline='\n')
p=Path('Tests/Basic.lean');s=p.read_text(encoding='utf-8');assert s.count('formalizedTechnicalLemmaCount = 507')==1;p.write_text(s.replace('formalizedTechnicalLemmaCount = 507','formalizedTechnicalLemmaCount = 508'),encoding='utf-8',newline='\n')
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');x=load(p);assert x['status']=='proved_locally';x['status']='independently_verified';x['evidence']['independent_verification']=(r/'verified.json').as_posix();w(p,x)
p=Path('docs/companion-papers-handoff.md');s=p.read_text(encoding='utf-8');anchor='# Companion-paper formalization handoff\n\n';assert s.startswith(anchor)
prefix=f'''## Actual PBPS unique positive macroscopic defect root (2026-10-09)

Independently VERIFIED science commit {head}. SAME original-input stationary
reflected kernel, real conditional operator T and joint reflection U now feed
the canonical onto isometry e from marginal L2 to exact complete HP=lpMeas=ran(P).
A=e T e^-1; B:HP-to-joint is actual leakage. SAME positive real root transports
to GammaP=e Gamma e^-1, with GammaP^2=I_HP-A^2=B.adjoint composed B, all-macro
norm/energy and ALL positive same-square macro uniqueness. Alternatives require
no supplied energy. Fulljoint Gram remains P-AJ^2. C2/two Hessian/positive capped
eta, rank0 and alphaeta=1 retained; zero extra public certificates/private providers.

Root39868 and independent3376 focused3920, followed by exactSCI63 verifier41344
focused3920, fresh anonymous decoder and independent primary-first seven-slot
review/current eight formula steps accepted. The initial
step3 excerpt binding failure was preserved and only its source span/bytes fixed;
independent presentation review confirms all8 literal excerpts. Full rendered
Exposition Seal/post-merge purification remain separate.

The SCI63 remote site and formalization workflows failed at the same Frontier
Cell process enum/salvage fields, with publication229 passing. The three fields
were corrected only after exact-review closure; source/Lean/lesson/audit bytes
and publication binding/context were checked unchanged. Corrected repository
acceptance still requires the actual serialized gates below.

NEXT mathematical work is centered root restriction/coercivity/invertibility and
B15 operator lower order/B16 normalized polar isometry. Exact constants:
rho=(1-alphaeta)/(1+alphaeta), gamma=2sqrt(alphaeta)/(1+alphaeta).
An inverse belongs only on the centered space; norm lower bounds alone do not
certify the printed operator order. Genuine earlier sharp Test consumers must
be connected through their actual production parents, never imported into production.
H1/event process/nonexplosion/invariance/hypocoercivity/main mixing/implementation
errors/actual-input expected-query costs and SPHMC composition remain separate.
Gaussian Cloud then midpoint follow the existing four-paper priority.
TV proximity transfers no unbounded expected cost.

Previous integration44dc6d6 has independent scoped repository/reader admission and
all three GitHub workflows terminal SUCCESS, including formalization37833436296.
Serialized Registry508/imports/Tests and affected reader/graph gates remain pending
below. No MERGED/live/PURIFIED/full paper/Goal claim. Earlier checkpoints preserved.

'''
p.write_text(s.replace(anchor,anchor+prefix,1),encoding='utf-8',newline='\n');p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-unique-positive-macroscopic-defect-root-2026-10-09';w(p,x)
print('PASS prepared serialized Registry508/imports/Tests/handoff from independently verified science63; aggregate/reader/graph gates pending.')
