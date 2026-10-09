from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification72.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==2
out=r/'integration72';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md']+['research-wiki/frontier-cells/'+c+'.json' for c in plan['active_cells']]
rows=[]
for name in owned:
 b=Path(name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),exact_snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
entries=[dict(key='pbps.hilbertCorrectorPerturbation',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Hilbert corrector perturbation algebra with actual PBPS consumer',tags=['PBPS','Hilbert','corrector','perturbation'],memory='analysisMemory',note='Explicit auxiliary structural assumptions on one complete real Hilbert space; exact C(u+Gr,v-Ar)-C(u,v)=inner(u,Inv r)+norm(r)^2/2. Actual72 supplies all conditions internally. No probabilistic or actual-r_rho producer.'),dict(key='pbps.actualCorrectorPerturbation',decl=plan['mathematical_declarations'][1],file=claim['proposed_files'][1],title='Actual PBPS corrector perturbation on the same centered space',tags=['PBPS','L2','conditional-expectation','corrector','perturbation'],memory='measureMemory',note='Same original six analytic callers/twelve witnesses/all actual71 clauses; same C/A0/Gamma0/Inv exact perturbation for every u,v,r in HP0. Generic conditions produced internally. Arbitrary r is not actual r_rho; actual H/K/B27/B28, dynamics/nonexplosion/main/errors/cost/composition remain open.')]
for e in entries:
 e['note']='Independent exactSCI72 '+head+'. '+e['note']+' Rank0/alphaeta1 legal; no extra caller, onto or higher regularity. Full Exposition/PURIFIED/main/live/Goal not inferred.'
 block='  {\n'+'\n'.join(['    key := '+json.dumps(e['key']),'    localDecl := '+json.dumps(e['decl']),'    upstreamDecl := '+json.dumps(e['title']),'    upstreamFile := "arXiv2609.06905v1 B20 and LemmaB4 Ex28-Ex34"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in e['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(e['note'])])+'\n  },\n'
 p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=('def '+e['memory']+' : List LemmaMemoryEntry := [').encode()+nl
 assert b.count(anchor)==1 and e['key'].encode() not in b;p.write_bytes(b.replace(anchor,anchor+block.encode().replace(b'\n',nl),1))
 with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as stream:stream.write((json.dumps(dict(key=e['key'],local_decl=e['decl'],local_file=e['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=e['tags'],upstream_decl=e['title'],upstream_file='arXiv2609.06905v1 B20/B4 perturbation',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=e['note']),ensure_ascii=False)+'\n').encode())
p=Path('AutoSamplingTheory/ExampleCases.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorChange'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation'+nl
assert b.count(anchor)==1 and addition not in b;p.write_bytes(b.replace(anchor,anchor+addition,1))
p=Path('Tests/Basic.lean');b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 519')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 519',b'formalizedTechnicalLemmaCount = 521'))
for cid in plan['active_cells']:
 p=Path('research-wiki/frontier-cells')/(cid+'.json');cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified'
 cell['evidence'].update(independent_verification=(r/'verified.json').as_posix(),execution_boundary=entries[1]['note'],truth_boundary=entries[1]['note'])
 cell['source_detail_audit'].update(fidelity_boundary=entries[1]['note'],gap='Perturbation algebra independently verified. Actual H/K/r_rho/B27/B28,dynamics/main/errors/cost/composition remain separate.')
 write(p,cell)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Exact PBPS corrector perturbation (2026-10-10)

Independent exact science72 VERIFIED commit {head}. The same B20 corrector
on the same centered HP0 obeys C(u+Gamma0 r,v-A0 r)-C(u,v)
=inner(u,Inv r)+norm(r)^2/2 for every u,v,r in HP0. One reusable complete-real-
Hilbert algebra leaf is consumed inside the actual PBPS original-six-input
theorem. Twelve witnesses, all actual71 clauses and the exact half/sign remain.
Two connected publication cells belong to one SAU; no second SAU or fake consumer.
Rank0/alphaeta1 remain legal, with no extra caller, onto or higher derivative.

Arbitrary r is not the source r_rho. The actual Algorithm1 half-turn endpoint
H_y, its joint Borel/nonexplosive construction, reversal and same-J lift, actual
K/B7/r_rho/B27/B28, full B4/H1, main/error/cap/cost/composition results remain open.
Q_y and same-J Gaussian disintegration ALREADY exist in
GaussianConditionalKernel.exists_tilted_isCondKernel; the actual affine reflected
law relation also exists. Reuse these before introducing any reference-law copy.
Next source-first work is the earliest deterministic flow/bounce/rate construction
ingredient with a real Proposition3.1 nonexplosion consumer. The independent
prospective73 source plan is planning only, no new proof or completion credit.

Serialized Registry521/imports/Tests and current reader/graph gates are pending
against final admin state. Independent exactSCI, aggregate/reader, remote CI,
main/live, full Exposition/PURIFIED and whole-paper/Goal completion are distinct.
PBPS/SPHMC and their actual-input composition precede GaussianCloud and midpoint;
older Chewi/frontiers/cycles/memory persist. TV does not transfer unbounded cost.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#exact-pbps-corrector-perturbation-2026-10-10';write(p,x)
p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
note=f'''
## Exact perturbation checkpoint72 (2026-10-10)

Independent science commit {head}; canonical full statements and six/four-step
formula proofs are authored once in declaration_lessons/pbps-hilbert-corrector-
perturbation.json and declaration_lessons/pbps-actual-corrector-perturbation.json.
Their complete exact Lean is adjacent and initially folded on the original
companion page. One SAU joins the auxiliary Hilbert lemma to actual PBPS inputs.

For the SAME C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0(Invu),v),
C(u+Gamma0 r,v-A0 r)-C(u,v)=inner(u,Inv r)+norm(r)^2/2.
All original actual71 clauses persist. Arbitrary r is not actual r_rho;
Algorithm1 H/K/B27/B28, full dynamics/main/errors/cost/composition remain open.
Serialized reader/aggregate admission is recorded separately in integration72;
this is not a full Exposition Seal, PURIFIED, main/live or whole-paper completion.

'''
p.write_bytes(first+nl+note.encode().replace(b'\n',nl)+rest)
(out/'registry-entries72.json').write_text(json.dumps(entries,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS serialized72 aggregate prepared after exactSCI only:Registry521,actual import,two connected cells,handoff/conversion; gates/reader pending.')
