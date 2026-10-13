from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification73.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration73';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json']
rows=[]
for name in owned:
 b=Path(name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),exact_snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
note=f'Independent exactSCI73 {head}. All original six analytic callers, no new premise; joint continuity/Borel, zero/group/inverse, actual two-equation derivative, nonnegative conserved weighted SUM energy, and exact pi endpoint on finite-dimensional real E. Rank0/alphaeta1/zero-energy legal. No random path/clock/bounce/Markov law, invariance/nonexplosion/main/errors/cost/composition or full Exposition/PURIFIED/main/live/Goal credit.'
entry=dict(key='pbps.actualHarmonicFlow',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual PBPS harmonic flow, derivative and conserved energy',tags=['PBPS','harmonic-flow','energy','Borel'],note=note)
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := "arXiv2609.06905v1 Section2 Algorithm1 and AppendixA1 Proposition3.1 construction"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(note)])+'\n  },\n'
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def analysisMemory : List LemmaMemoryEntry := ['+nl
assert b.count(anchor)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(anchor,anchor+block.encode().replace(b'\n',nl),1))
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as s:s.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file='arXiv2609.06905v1 Section2 Algorithm1/AppendixA1',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note),ensure_ascii=False)+'\n').encode())
p=Path('AutoSamplingTheory/ExampleCases.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow'+nl
assert b.count(anchor)==1 and addition not in b;p.write_bytes(b.replace(anchor,anchor+addition,1))
p=Path('Tests/Basic.lean');b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 521')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 521',b'formalizedTechnicalLemmaCount = 522'))
p=Path(owned[-1]);cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified'
cell['evidence'].update(independent_verification=(r/'verified.json').as_posix(),execution_boundary=note,truth_boundary=note)
cell['source_detail_audit'].update(fidelity_boundary=note,gap='Deterministic flow/energy is verified. Actual bounce/rate/clock/random recursion, nonexplosion, law invariance and full paper/error/cost/composition remain independent.');write(p,cell)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Exact PBPS harmonic flow (2026-10-10)

Independent exact science73 VERIFIED commit {head}. For
c=y-eta gradientV(xRef), the actual harmonic flow is
X_t=c+cos(t)(x-c)+sqrt(eta)sin(t)p,
P_t=-sin(t)/sqrt(eta)(x-c)+cos(t)p.
The complete nine-clause theorem proves joint continuity and joint Borel
measurability, zero/group/both inverse laws, the actual two ODE derivatives,
nonnegativity and conservation of the weighted SUM energy
(eta^-1 norm(x-c)^2+norm(p)^2)/2, and the exact pi endpoint (2c-x,-p).
It retains all six original analytic callers; rank0/alphaeta1/zero energy
remain legal. C2 V and positive eta suffice inside this deterministic proof.

This is an ingredient of Algorithm1/Proposition3.1, not its stochastic
construction. Actual reflection/bounce/rate, clock measurable recursion,
nonexplosion, invariance/reversal, actual H/K/B27/B28 and full B4/H1,
main/error/cap/expected-query-cost/composition results remain open.
Q_y and same-J Gaussian disintegration and the actual reflected-law relation
already exist; reuse those before adding any reference-law copy.
Next source-first bounded edge is the actual bounce/rate ingredient used by
the half-turn nonexplosion construction. TV does not transfer unbounded cost.

Serialized Registry522/imports/Tests, current reader/graph and mandatory
aggregate gates are pending against final admin state. ExactSCI, aggregate,
remote CI, main/live, full Exposition/PURIFIED and full-paper/Goal completion
remain distinct. PBPS/SPHMC actual-input composition comes first, then
GaussianCloud and midpoint; preserve older Chewi/frontiers/cycles/memory.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#exact-pbps-harmonic-flow-2026-10-10';write(p,x)
p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
text=f'''
## Exact harmonic-flow checkpoint73 (2026-10-10)

Independent science commit {head}. The complete attributed statement and
six-step formula proof are authored once in declaration_lessons/
pbps-actual-harmonic-flow.json; the exact full Lean, including its private
literal proposition specification, is adjacent and initially folded.
For c=y-eta gradientV(xRef), the exact deterministic flow conserves
(eta^-1 norm(x-c)^2+norm(p)^2)/2 and sends (x,p) to (2c-x,-p) at pi.
All nine clauses and original six callers are retained with no extra premise.
Actual bounce/rate/clocks/PDMP/nonexplosion/invariance/main/errors/expected
cost and actual-input composition remain open. Integration73 records reader
and aggregate checks separately; no full Exposition/PURIFIED/main/live or
whole-paper/Goal badge is inferred.

'''
p.write_bytes(first+nl+text.encode().replace(b'\n',nl)+rest)
(out/'registry-entry73.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS serialized73 prepared only after exactSCI: Registry522/import/Tests, one cell/handoff/conversion; aggregate and reader pending.')
