from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification75.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration75';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json']
rows=[]
for name in owned:
 b=Path(name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),exact_snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
note=f'Independent exactSCI75 {head}. Original six analytic callers, eight literal actual definitions and ten conclusions: continuous/Borel integrated actual hazard, finite-interval integrability/nonnegative monotonicity, continuous-time closed first crossing with finite-value and infinity/e=0 guards, joint Borel clock, actual Exp(1) pushforward probability law and exact strict survival including infinity, original-state energy cap and extended waiting lower/zero-cap branches. No arbitrary cap/law provider or almost-sure finite wait premise. Recursive actual PDMP paths/iid nonaccumulation/Markov/invariance/terminal kernel/hypocoercivity/main/errors/expected costs/composition and full Exposition/PURIFIED/main/live/Goal remain open.'
entry=dict(key='pbps.actualHazardClock',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual PBPS integrated hazard and first exponential clock',tags=['PBPS','hazard','first-clock','exponential','Borel','energy'],note=note)
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := "arXiv2609.06905v1 Algorithm1 and AppendixA1 equation(A1)"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(note)])+'\n  },\n'
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def analysisMemory : List LemmaMemoryEntry := ['+nl
assert b.count(anchor)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(anchor,anchor+block.encode().replace(b'\n',nl),1))
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as s:s.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file='arXiv2609.06905v1 Algorithm1/AppendixA1(A1)',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note),ensure_ascii=False)+'\n').encode())
p=Path('AutoSamplingTheory/ExampleCases.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock'+nl
assert b.count(anchor)==1 and addition not in b;p.write_bytes(b.replace(anchor,anchor+addition,1))
p=Path('Tests/Basic.lean');b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 523')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 523',b'formalizedTechnicalLemmaCount = 524'))
p=Path(owned[-1]);cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified';cell['evidence'].update(independent_verification=(r/'verified.json').as_posix(),execution_boundary=note,truth_boundary=note)
cell['source_detail_audit'].update(fidelity_boundary=note,gap='The one actual integrated hazard and first waiting law are independently verified. Recursion(A2), iid nonaccumulation/global paths/Markov/invariance/terminal kernel and full mains/costs remain independent.');write(p,cell)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Exact PBPS first hazard clock (2026-10-10)

Independent exact science75 VERIFIED commit {head}. The actual harmonic flow73
and actual bounce/rate74 are true formal parents. For the actual rate along Phi,
Lambda_z(t)=integral_0^t lambda(Phi_s z) ds is jointly continuous/Borel and has
finite-interval integrability, Lambda(0)=0 and nonnegative monotonicity.
The continuous-time first crossing tau_z(e)=inf{{t>=0:Lambda_z(t)>=e}} takes
values in [0,infinity], with inf(empty)=infinity. Its finite sublevels are
exactly {{e<=Lambda_z(t)}}; finite tau attains Lambda(tau)=e, e>0 gives tau>0,
and tau(0)=0. Joint Borel measurability is proved, not supplied.

The ACTUAL pushforward of Exp(1) under e->tau_z(max(e,0)) is a probability
measure W_z, with exact strict survival W_z((t,infinity])=exp(-Lambda_z(t)).
The tail includes infinity. Its actual initial-energy C_z is nonnegative,
Lambda_z(t)<=C_z*t, C_z>0 implies tau_z(e)>=e/C_z, and C_z=0,e>0 implies
tau=infinity. No almost-sure finite wait, arbitrary hazard/cap/law provider,
positive energy/dimension or higher derivative premise is introduced. Original
six analytic callers and legal rank0/zero-energy/e0/alphaeta1 cases persist.
Exact396-line module and nine formula/BODY blocks are independently reviewed.

This closes one first-clock law only. Next dependency-ready edge is the actual
finite stopped postjump recursion(A.2), its joint Borel dependence and inherited
H(z0) invariant, following source-only preread76. No phase at infinity and no
global physical-time phase is assigned to arbitrary zero thresholds. iid Exp
realization, moments/SLLN and nonaccumulation precede global path/Markov proofs.
Invariance/reversal, terminal kernel, hypocoercivity/main/errors/caps, expected
query cost and actual-input composition remain open. TV proximity does not
transfer unbounded costs. Reuse Q_y/same-J and existing reflected-law facts.

Serialized Registry524/imports/Tests, current reader/graph and mandatory
aggregate gates are pending against final admin state. Source review input
contamination was retained as supplemental evidence and repaired by an exact
metadata overlay plus a fresh anti-anchored review; it was never source admission.
ExactSCI, aggregate, remoteCI/main/live, Exposition/PURIFIED and full-paper/Goal
completion remain distinct. PBPS/SPHMC composition precedes GaussianCloud and
midpoint; preserve older Chewi/frontiers/cycles/memory.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#exact-pbps-first-hazard-clock-2026-10-10';write(p,x)
p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
text=f'''
## Exact actual first-clock checkpoint75 (2026-10-10)

Independent science commit {head}. Complete attributed statement and nine-step
formula proof are authored once in declaration_lessons/pbps-actual-hazard-clock.json;
exact full Lean (literal specification and proved internal primitive included)
is adjacent and initially folded. The actual Exp(1) pushforward is normalized,
with strict survival exp(-Lambda_z(t)) including infinite waits. Finite threshold
attainment, joint Borel measurability and original-state energy waiting bounds
retain all original six callers and rank0/zero-energy/e0/alphaeta1 cases.
Actual recursive PDMP/iid nonaccumulation/global path/Markov/invariance/main/errors/
expected-query cost/composition remain open. Integration75 records aggregate and
reader checks separately; no Exposition/PURIFIED/main/live/whole-paper/Goal credit.

'''
p.write_bytes(first+nl+text.encode().replace(b'\n',nl)+rest)
(out/'registry-entry75.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS serialized75 prepared only after exactSCI: Registry524/import/Tests, one cell/handoff/conversion; aggregate and reader pending.')
