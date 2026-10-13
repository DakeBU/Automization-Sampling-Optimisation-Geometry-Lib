from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification76.adoption.json');assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration76';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-jump-recursion.json']
rows=[]
for name in owned:
 b=Path(name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),exact_snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
note=f'Independent exactSCI76 {head}. Original six analytic callers, eleven literal definitions and ten conclusion groups: actual finite stopped postjump recursion(A.2) using actual73 flow, actual74 bounce/rate and actual75 first clock; joint Borel update/records/event times; monotone and absorbing stopping; original initial energy on records and pre-jump arcs; original-energy uniform waiting increment including stopped records; zero-cap/zero-threshold and strictly increasing finite-successor guards. No phase at infinity or global physical-time path for arbitrary zero thresholds. iid Exp1 realization, a.s. positivity/divergence and nonaccumulation remain next independent boundaries; full PDMP/Markov/invariance/kernel/hypocoercivity/main/errors/expected-cost/composition, Exposition/PURIFIED/main/live/Goal remain open.'
entry=dict(key='pbps.actualFiniteJumpRecursion',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual finite PBPS jump recursion and original-energy spacing',tags=['PBPS','recursion','Borel','energy','waiting-time','stopped'],note=note)
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := "arXiv2609.06905v1 AppendixA1 equation(A2) and Ex8"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(note)])+'\n  },\n'
p=Path(owned[0]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def analysisMemory : List LemmaMemoryEntry := ['+nl
assert b.count(anchor)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(anchor,anchor+block.encode().replace(b'\n',nl),1))
with Path(owned[5]).open('ab') as s:s.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file='arXiv2609.06905v1 AppendixA1(A2)/Ex8',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note),ensure_ascii=False)+'\n').encode())
p=Path(owned[1]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion'+nl
assert b.count(anchor)==1 and addition not in b;p.write_bytes(b.replace(anchor,anchor+addition,1))
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 524')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 524',b'formalizedTechnicalLemmaCount = 525'))
p=Path(owned[-1]);c=load(p);assert c['status']=='proved_locally';c['status']='independently_verified';c['evidence'].update(independent_verification=(r/'verified.json').as_posix(),execution_boundary=note,truth_boundary=note)
c['source_detail_audit'].update(fidelity_boundary=note,gap='Actual finite stopped recursion(A2) and original-energy spacing are independently verified. The actual iid Exp1 product, a.s. positivity/divergence and nonaccumulation remain open, followed by global process/Markov/invariance/terminal kernel/full mains/costs.');write(p,c)
p=Path(owned[3]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f'''## Exact finite PBPS jump recursion (2026-10-10)

Independent exact science76 VERIFIED commit {head}. The actual73 flow, actual74
bounce/rate and actual75 first hazard clock are genuine formal parents. The
postjump recursion uses finite(time,phase) or stopped, with event time infinity
for stopped and no assigned phase there. It follows AppendixA1(A2), retaining
the original six analytic callers, eleven literal definitions, rank0, alphaeta1,
zero energy and arbitrary zero thresholds. Joint Borel measurability holds for
updates, every finite record and event time. Event times are monotone; stopping
is absorbing. Original energy H(z0) is retained on active states and pre-jump
arcs, so the same original-energy C0 bounds every outgoing actual rate.
For C0>0, T[n+1]>=T[n]+e[n]/C0 includes already stopped infinity records.
For C0=0 and e[n]>0, an active record stops. Zero thresholds give an immediate
bounce; positive thresholds and active finite successors give strict growth.
Arbitrary zero thresholds do not yet define a global physical-time phase.

The exact412-line theorem and ten formula/BODY steps passed independent math,
strict blind reconstruction and fresh source-first anti-anchored review.
The stale prospective module comment and historical neutral-binder coordinates
remain explicit nonmathematical debts, with reviewer relocation as evidence.
Next dependency-ready leaf77 is the actual countable Exp1 product, its a.s.
positive coordinates and divergent partial sums. Its real consumer is this
recursion's uniform spacing, then event-time nonaccumulation. No assumed iid
sequence/provider, nonexplosion, global path/Markov/invariance/kernel, full
hypocoercivity/main/error/expected-query cost/composition is admitted here.
TV proximity does not transfer unbounded costs. PBPS/SPHMC and composition
precede Gaussian Cloud and midpoint. Preserve Chewi/frontiers/cycles/memory.

Serialized Registry525/imports/Tests, current reader/graph and mandatory
aggregate gates are pending against final admin state.
ExactSCI, aggregate, remoteCI/main/live, Exposition/PURIFIED and full-paper/Goal
completion remain distinct.

'''
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=Path(owned[4]);x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#exact-finite-pbps-jump-recursion-2026-10-10';write(p,x)
p=Path(owned[6]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
text=f'''
## Exact actual finite stopped recursion76 (2026-10-10)

Independent science commit {head}. The complete attributed statement and ten
formula/BODY steps are authored once in declaration_lessons/pbps-actual-finite-jump-recursion.json,
with exact initially folded adjacent Lean. Actual73/74/75 provide the flow,
bounce/rate and first clock; no phase at infinity. Joint Borel recursion,
original initial energy, monotone/stopped times, uniform waiting increments
and zero/strict-growth guards are proved. iid Exp1 thresholds, partial-sum
divergence/nonaccumulation, global PDMP/Markov/invariance/kernel/main/errors/
expected-query cost/composition remain open. Integration76 records aggregate,
reader and graph gates separately; no Exposition/PURIFIED/main/live/Goal credit.

'''
p.write_bytes(first+nl+text.encode().replace(b'\n',nl)+rest)
(out/'registry-entry76.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS serialized76 prepared after exactSCI only: Registry525/import/Tests, one cell/handoff/conversion; aggregate/reader pending.')
