from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-polar65';r64=r.parent/'pbps-centered-root64'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write_new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace_json(p,x):
 p=Path(p);old=p.read_bytes();nl=b'\r\n' if b'\r\n' in old else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
def insert_after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b;p.write_bytes(b.replace(a,a+addition.encode()+nl,1))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();verification=load(r/'root.exact-verification65.adoption.json')
assert verification['native_verified'] and verification['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert load(r64/'remote-ci64.accepted.json')['status']=='EXACT_INT64_REMOTE_ALL_SUCCESS'
assert load(r64/'root.stale-cell-overlay64.adoption.json')['status']=='EXACT_TWO_FIELD_OVERLAY_ACCEPTED_NOT_YET_APPLIED'
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');cid=plan['active_cells'][0];decl=plan['mathematical_declarations'][0]
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','research-wiki/frontier-cells/'+cid+'.json','research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json']
out=r/'integration65';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir();history=[]
for name in owned:
 p=root/name;b=p.read_bytes();q=snap/(sha(name.encode())+'.exactraw');q.write_bytes(b);history.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=q.relative_to(root).as_posix()))
write_new(out/'owned-before.json',dict(head=head,owned=history))
key='pbps.actualPolarIsometry';title='Actual PBPS typed polar isometry and adjoint corrector';source='arXiv2609.06905v1 B16 and B3 first corrector'
note='Independently exact-science65 VERIFIED '+head+'. Original C2/two Hessians/positive capped eta produce SAME actual laws/e/U/T/root/centered inverse. Exact B0:HP0->kerP and V0=B0 Inv satisfy B0=V0 Gamma0,V0.adjoint composed V0=I and all-vector norm equality. Genuine original-input Test gives B0.adjoint=Gamma0 V0.adjoint, adjoint contraction and residual annihilation. No onto/reverse product. Rank0/alphaeta1 retained. B21 root commutation/rotation, B17/H1/operator inequalities,dynamics/main/errors/expected costs/composition remain open.'
tags=['PBPS','L2','polar','isometry','adjoint-corrector'];entry='  {\n    key := '+json.dumps(key)+'\n    localDecl := '+json.dumps(decl)+'\n    upstreamDecl := '+json.dumps(title)+'\n    upstreamFile := '+json.dumps(source)+'\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in tags)+']\n    saldUse := "Actual PBPS consumer; no SALD admission"\n    note := '+json.dumps(note)+'\n  },\n'
p=root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def measureMemory : List LemmaMemoryEntry := ['+nl;assert b.count(anchor)==1 and key.encode() not in b;p.write_bytes(b.replace(anchor,anchor+entry.encode().replace(b'\n',nl),1))
row=dict(key=key,local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',sald_use='Actual PBPS consumer; no SALD change',tags=tags,upstream_decl=title,upstream_file=source,verified_commit=head,evidence=(r/'verified.json').relative_to(root).as_posix(),next_action=note)
with (root/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as f:f.write((json.dumps(row,ensure_ascii=False)+'\n').encode())
insert_after(root/'AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse','import AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry')
insert_after(root/'Tests.lean','import Tests.ProximalBPSCenteredRootOrderInverse','import Tests.ProximalBPSPolarIsometry')
p=root/'Tests/Basic.lean';b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 510')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 510',b'formalizedTechnicalLemmaCount = 511'))
p=root/'research-wiki/frontier-cells'/f'{cid}.json';cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence']['independent_verification']=(r/'verified.json').relative_to(root).as_posix();replace_json(p,cell)
overlay=r64/'stale-cell-metadata-overlay64';p=root/'research-wiki/frontier-cells/ASTIS-SHARED-l2-real-positive-square-order.json';assert p.read_bytes()==(overlay/'cell.before.exactraw.snapshot.json').read_bytes();approved=(overlay/'cell.after.proposed.json').read_bytes();assert sha(approved)=='b2fb3d143f61a86502f0614dbc194c5f5c7fa0ae30132a742e7e6ff634822ab1';p.write_bytes(approved)
write_new(out/'stale-cell-overlay64.applied.json',dict(status='EXACT_SEPARATELY_REVIEWED_TWO_FIELDS_APPLIED',canonical_path=p.relative_to(root).as_posix(),canonical_after_RAW_sha256=sha(approved),independent_adoption=(r64/'root.stale-cell-overlay64.adoption.json').relative_to(root).as_posix(),changed_fields=['source_anchor','evidence.truth_boundary'],source_Lean_publication_lesson_audit_unchanged=True,remaining='Other nested source_detail/purification metadata and reader debt stay explicitly outside this overlay; no full Exposition/PURIFIED claim.'))
p=root/'docs/companion-papers-handoff.md';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Actual PBPS typed polar isometry and adjoint corrector (2026-10-09)

Independently VERIFIED science commit {head}. SAME original finite real Hilbert
C2/two Hessian/positive capped eta inputs now produce the actual typed B16
B0:HP0->kerP and V0=B0 Inv. The exact closed conditional kernel is distinct
from global joint centering. B0=V0 Gamma0, V0.adjoint composed V0=I, and
all-vector norm preservation are proved. Rank0 and alphaeta=1 remain legal.

The original-input Test derives B0.adjoint=Gamma0 V0.adjoint, adjoint
contraction and V0.adjoint(g-V0(V0.adjoint g))=0. No onto kerP or reverse
product identity is asserted; no root/gap/unit/H1/floor premise was added.
Fresh compiler3945/standard3, independent math, blind decoder, source-first
full seven-slot review and all5 literal BODY formula steps are accepted.

Next dependency-ready candidate: SAME actual root/reflection commutation
and centered restriction for the printed B21 idealized rotation/corrector
argument. Retrieval is RAW/unvalidated until source66/seal/compile/review.
The reflection U and conditional half-turn H are different operators.
B17/H1/B13/B14, events/nonexplosion/invariance,hypocoercivity/main mixing,
implementation errors and actual-input expected queries/composition remain
open. TV proximity transfers no unbounded expected cost. Gaussian Cloud then
midpoint follow the existing four-paper priority; older frontiers are preserved.

Previous INT64 0aef19c has scoped independent repository/reader acceptance
with explicit debt and all remote formal/site/contributor workflows SUCCESS.
Its two stale shared-cell attribution/status fields have a separately reviewed
exact overlay; other reader/purification debt remains. Serialized Registry511,
imports/Tests and affected reader/graph gates are pending below. No merged/live,
full Exposition/PURIFIED, whole-paper or Goal completion is claimed.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=root/'website/content/samplewiki_companion_frontiers.json';x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#actual-pbps-typed-polar-isometry-and-adjoint-corrector-2026-10-09';replace_json(p,x)
print('Prepared serialized65 Registry511/imports/Tests/handoff + exact reviewed64 metadata overlay; mandatory aggregate and reader/graph gates pending.')
