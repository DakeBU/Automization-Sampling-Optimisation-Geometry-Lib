from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-ambient-adjoint66'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write_new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace_json(p,x):
 p=Path(p);old=p.read_bytes();nl=b'\r\n' if b'\r\n' in old else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
def insert_after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b;p.write_bytes(b.replace(a,a+addition.encode()+nl,1))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();verification=load(r/'root.exact-verification66.adoption.json')
assert verification['native_verified'] and verification['verified_commit']==head=='a115115d42b3fa2b67885d87fe4d5300af36fcd1'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert load(r.parent/'pbps-polar65/remote-ci65.accepted.json')['status']=='EXACT_INT65_REMOTE_ALL_SUCCESS'
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');cid=plan['active_cells'][0];decl=plan['mathematical_declarations'][0]
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','research-wiki/frontier-cells/'+cid+'.json']
out=r/'integration66';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=root/name;b=p.read_bytes();q=snap/(sha(name.encode())+'.exactraw');q.write_bytes(b);history.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=q.relative_to(root).as_posix()))
write_new(out/'owned-before.json',dict(head=head,owned=history))
key='pbps.ambientAdjointCorrector';title='Actual PBPS ambient adjoint and globally centered corrector';source='arXiv2609.06905v1 Appendix B3 first corrector after B16 before B20'
note='Independently exact-science66 VERIFIED '+head+'. SAME original C2/two Hessians/positive capped eta inputs produce canonical R:L2(J)->kerP with inclusion Rg=g-Pg and all-vector Bambient*=i0 B0*R. Every actual globally centered input produces fP in HP0,fperp=Rf,fV=V0*fperp with B* fperp=i0 Gamma0 fV=GammaP i0 fV, exact Pythagoras and contraction. Genuine Test gives original-input reconstruction,B*f=GammaP i0 fV and squared norm budget. Rank0/alphaeta1 retained. Two literal private Prop expansions are representations only; no extra premise/provider. Full B20/B21,halfturn/H1/dynamics/main/errors/expected costs/composition remain open.'
tags=['PBPS','L2','ambient-adjoint','centering','corrector'];entry='  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(title)+'\n    upstreamFile := '+json.dumps(source)+'\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n'
p=root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def measureMemory : List LemmaMemoryEntry := ['+nl;assert b.count(anchor)==1 and key.encode() not in b;p.write_bytes(b.replace(anchor,anchor+entry.encode().replace(b'\n',nl),1))
row=dict(key=key,local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=title,upstream_file=source,verified_commit=head,evidence=(r/'verified.json').relative_to(root).as_posix(),next_action=note)
with (root/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as f:f.write((json.dumps(row,ensure_ascii=False)+'\n').encode())
insert_after(root/'AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry','import AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector')
insert_after(root/'Tests.lean','import Tests.ProximalBPSPolarIsometry','import Tests.ProximalBPSAmbientAdjointCorrector')
p=root/'Tests/Basic.lean';b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 511')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 511',b'formalizedTechnicalLemmaCount = 512'))
p=root/'research-wiki/frontier-cells'/f'{cid}.json';cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence']['independent_verification']=(r/'verified.json').relative_to(root).as_posix();replace_json(p,cell)
p=root/'docs/companion-papers-handoff.md';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Actual PBPS ambient adjoint and globally centered corrector (2026-10-09)

Independently VERIFIED science commit {head}. SAME original finite real Hilbert
C2/two Hessian/positive capped eta inputs now produce canonical R:L2(J)->kerP
with inclusion Rg=g-Pg and Bambient* g=i0 B0* Rg for every joint g.
For every joint input with zero integral, the actual conditional mean belongs
to SAME HP0. Its fperp=Rf and fV=V0* fperp satisfy the exact Gamma action,
orthogonal squared-norm decomposition and contraction. The genuine Test gives
f=i0 fP+fperp, B*f=GammaP i0 fV and ||fV||^2<=||f||^2-||fP||^2.
Rank0 and alphaeta=1 remain legal; no premise/provider was added.

Two private full literal Prop definitions preserve the sealed public statements
and exact caller conditions; both whole modules and their expansions were
independently reviewed. Six exact BODY formula steps, blind decoder and full
seven-slot source review accepted the bounded source-derived domain adapter.
Printed B20 defines the first corrector; the sharp energy estimate is B23 in
Lemma B.3. Next dependency-ready candidate is SAME actual root/centered-inverse
commutation, a real printed proof ingredient for B23 and B21 rotation. Existing
commutation retrieval is RAW and unvalidated, not a public premise or proof.
Reflection U and conditional half-turn H remain distinct.
B17/H1/B13/B14, event process/nonexplosion/invariance,hypocoercivity/main,
implementation errors and actual-input expected queries/composition are open.
TV proximity transfers no unbounded expected cost. Gaussian Cloud then midpoint
follow the existing four-paper priority; all older frontiers are preserved.

Previous INT65 31ce36e has scoped independent repository/reader acceptance and
all four remote formal/site/contributor workflows SUCCESS. The reviewed64
two-field shared-cell overlay is already applied and is not reapplied here.
Serialized Registry512/imports/Tests and affected reader/graph gates are pending.
No merged/live, full Exposition/PURIFIED, whole-paper or Goal claim is made.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=root/'website/content/samplewiki_companion_frontiers.json';x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-ambient-adjoint-and-globally-centered-corrector-2026-10-09';replace_json(p,x)
print('Prepared serialized66 Registry512/imports/Tests/handoff; mandatory aggregate and reader/graph gates pending. No old64 overlay reapplied.')
