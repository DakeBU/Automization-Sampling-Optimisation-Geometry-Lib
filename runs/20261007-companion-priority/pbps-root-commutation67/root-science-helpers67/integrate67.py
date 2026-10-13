from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-root-commutation67'
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write_new(p,x):assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def replace_json(p,x):
 b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
def insert_after(p,anchor,addition):
 b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b;p.write_bytes(b.replace(a,a+addition.encode()+nl,1))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification67.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert load(r.parent/'pbps-ambient-adjoint66/remote-ci66.accepted.json')['status']=='EXACT_INT66_REMOTE_ALL_SUCCESS'
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');out=r/'integration67';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]
history=[]
for name in owned:
 p=root/name;b=p.read_bytes();q=snap/(sha(name.encode())+'.exactraw');q.write_bytes(b);history.append(dict(path=name,raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),exact_snapshot=q.relative_to(root).as_posix()))
write_new(out/'owned-before.json',dict(head=head,owned=history))
entries=[
 dict(key='measure.realL2PositiveSquareCommutation',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Positive-square commutation on arbitrary real L2',source='arXiv2609.06905v1 Appendix D1 functional calculus background; ASTIS auxiliary corollary for B23/B21',tags=['L2','positive','CFC','square-root','commutation'],note='Arbitrary measure and positive real-L2 G,D: Commute(G²,D) implies Commute(G,D), by canonical complexification and the same unique positive square root. No probability/finiteness/nontriviality/caller CFC premise. Actual PBPS internally produces positive D=I+T. Not a separately printed paper theorem.'),
 dict(key='pbps.actualRootInverseCommutation',decl=plan['mathematical_declarations'][1],file=claim['proposed_files'][1],title='Same actual PBPS root and centered inverse commutation',source='arXiv2609.06905v1 Appendix B3 proof ingredient for Lemma B3/B23 and B21',tags=['PBPS','L2','same-root','centered-inverse','corrector'],note='Original C2/two Hessians/positive capped eta produce SAME actual Gamma/T/A/HP0/Inv. Internal I+T positivity yields root commutation; exact A0 restriction is selfadjoint, commutes with Gamma0 and Inv, and A0²+Gamma0²=I. The SAME inverse is selfadjoint. Genuine original-input Test gives K=A0Inv selfadjoint and I+K²=Inv². Rank0/alphaeta1 retained. Two literal private Props are representations, never providers/premises. Sharp B23/LemmaB3 energy/B21/H1/dynamics/main/errors/cost/composition remain open.')]
text=''
for x in entries:
 x['note']='Independently exact-science67 VERIFIED '+head+'. '+x['note']
 text+='  {\n    key := '+json.dumps(x['key'])+'\n    localDecl := '+json.dumps(x['decl'])+'\n    upstreamDecl := '+json.dumps(x['title'])+'\n    upstreamFile := '+json.dumps(x['source'])+'\n    status := LemmaMemoryStatus.formalizedLocal\n    tags := ['+', '.join(json.dumps(t) for t in x['tags'])+']\n    saldUse := "PBPS real consumer; no SALD admission"\n    note := '+json.dumps(x['note'])+'\n  },\n'
 p=root/'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl'
 with p.open('ab') as f:f.write((json.dumps(dict(key=x['key'],local_decl=x['decl'],local_file=x['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=x['tags'],upstream_decl=x['title'],upstream_file=x['source'],verified_commit=head,evidence=(r/'verified.json').relative_to(root).as_posix(),next_action=x['note']),ensure_ascii=False)+'\n').encode())
p=root/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def measureMemory : List LemmaMemoryEntry := ['+nl;assert b.count(anchor)==1 and all(x['key'].encode() not in b for x in entries);p.write_bytes(b.replace(anchor,anchor+text.encode().replace(b'\n',nl),1))
insert_after(root/'AutoSamplingTheory/TechnicalLemmas.lean','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder','import AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute')
insert_after(root/'AutoSamplingTheory/ExampleCases.lean','import AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector','import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation')
insert_after(root/'Tests.lean','import Tests.ProximalBPSAmbientAdjointCorrector','import Tests.ProximalBPSActualRootCommutation')
p=root/'Tests/Basic.lean';b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 512')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 512',b'formalizedTechnicalLemmaCount = 514'))
for cid in plan['active_cells']:
 p=root/'research-wiki/frontier-cells'/f'{cid}.json';cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence']['independent_verification']=(r/'verified.json').relative_to(root).as_posix();replace_json(p,cell)
p=root/'docs/companion-papers-handoff.md';b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Same PBPS root and centered inverse commutation (2026-10-09)

Independently VERIFIED science commit {head}. The arbitrary-real-L2 positive
square commutation leaf is now consumed internally for SAME actual PBPS roots.
Original finite real Hilbert/Borel/C2/two Hessians/positive capped eta callers
produce Commute Gamma T and GammaP A, the exact selfadjoint restriction A0 on
SAME HP0, A0²+Gamma0²=I, and SAME inverse selfadjoint/commuting with A0.
The genuine original-input Test derives K=A0 Inv selfadjoint and I+K²=Inv².
No positivity of T/A/A0, caller CFC/provider, new nontriviality or strict endpoint
premise appears. Rank0 and alphaeta=1 remain legal.

Two literal private Prop definitions preserve the complete sealed statements;
both full modules and ten literal formula/BODY steps have independent math,
blind decoder and primary-first seven-slot source admission. Reviewed metadata
accurately attributes older ambient-adjoint Test reconstruction/norm budget,
links generic background to D1 and lists only used generic Mathlib APIs.
Next dependency-ready target is printed B20/B23 sharp corrector energy and
Lemma B3 (B19/B22/B24): exact1/(2gamma), then half/three-halves norm equivalence.
Its complete draft headers are not proofs, and B21 rotation remains independent.
Weak H1/B2, dynamics/hypocoercivity/main/invariance/nonexplosion, implementation
errors and actual-input expected cost/composition remain open. TV proximity
does not transfer unbounded expected cost. Four-paper priority and older routes
remain intact; no merged/live/full Exposition/PURIFIED/whole-Goal claim.

INT66 eb3d5ff has all four remote workflows SUCCESS and scoped independent
science/shared/historical-reader acceptance. Its local final-admin graph cache
freshness was withheld; this cycle must regenerate against final current cells
after admin writes. That debt must not be silently upgraded by old receipts.
Serialized Registry514/imports/Tests and current reader/graph gates are pending.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=root/'website/content/samplewiki_companion_frontiers.json';x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#same-pbps-root-and-centered-inverse-commutation-2026-10-09';replace_json(p,x)
print('Prepared serialized67 Registry514/imports/Tests/handoff; mandatory aggregate/current reader and graph gates pending.')
