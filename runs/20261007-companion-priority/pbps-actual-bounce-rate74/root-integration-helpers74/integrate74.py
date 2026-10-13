from pathlib import Path
import hashlib,json,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 p=Path(p);nl=b'\r\n' if b'\r\n' in p.read_bytes() else b'\n';p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode().replace(b'\n',nl))
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();v=load(r/'root.exact-verification74.adoption.json')
assert v['native_verified'] and v['verified_commit']==head
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['mathematical_declarations'])==1
out=r/'integration74';out.mkdir(exist_ok=False);snap=out/'before';snap.mkdir()
owned=['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/ExampleCases.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounce-rate.json']
rows=[]
for name in owned:
 b=Path(name).read_bytes();p=snap/(sha(name.encode())+'.exactraw');p.write_bytes(b);rows.append(dict(path=name,RAW_sha256=sha(b),exact_snapshot=p.as_posix()))
(out/'owned-before.json').write_text(json.dumps(dict(head=head,owned=rows),indent=2)+'\n',encoding='utf8',newline='\n')
note=f'Independent exactSCI74 {head}. All original six analytic callers, no new premise; actual zero-safe Borel bounce, continuous nonnegative rate, norm/involution/pairing and exact weighted SUM energy preservation, flipped-rate difference and pointwise same-energy-layer Lambda majorant. Internal beta-Lipschitz producer, rank0/alphaeta1/zero-energy/zero-normal legal. Actual clocks/path/nonexplosion/invariance/Markov/terminal kernel/main/errors/expected-query cost/composition and full Exposition/PURIFIED/main/live/Goal remain open.'
entry=dict(key='pbps.actualBounceRate',decl=plan['mathematical_declarations'][0],file=claim['proposed_files'][0],title='Actual PBPS zero-safe bounce, rate and energy-layer bound',tags=['PBPS','reflection','bounce','rate','energy','Borel'],note=note)
block='  {\n'+'\n'.join(['    key := '+json.dumps(entry['key']),'    localDecl := '+json.dumps(entry['decl']),'    upstreamDecl := '+json.dumps(entry['title']),'    upstreamFile := "arXiv2609.06905v1 Section2 Algorithm1 and AppendixA1 Proposition3.1 construction"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ['+', '.join(json.dumps(t) for t in entry['tags'])+']','    saldUse := "PBPS consumer; no SALD admission"','    note := '+json.dumps(note)])+'\n  },\n'
p=Path('AutoSamplingTheory/TechnicalLemmas/Registry.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'def analysisMemory : List LemmaMemoryEntry := ['+nl
assert b.count(anchor)==1 and entry['key'].encode() not in b;p.write_bytes(b.replace(anchor,anchor+block.encode().replace(b'\n',nl),1))
with Path('research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl').open('ab') as s:s.write((json.dumps(dict(key=entry['key'],local_decl=entry['decl'],local_file=entry['file'],status='formalized-local',sald_use='PBPS consumer; no SALD change',tags=entry['tags'],upstream_decl=entry['title'],upstream_file='arXiv2609.06905v1 Section2 Algorithm1/AppendixA1',verified_commit=head,evidence=(r/'verified.json').as_posix(),next_action=note),ensure_ascii=False)+'\n').encode())
p=Path('AutoSamplingTheory/ExampleCases.lean');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow'+nl;addition=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate'+nl
assert b.count(anchor)==1 and addition not in b;p.write_bytes(b.replace(anchor,anchor+addition,1))
p=Path('Tests/Basic.lean');b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 522')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 522',b'formalizedTechnicalLemmaCount = 523'))
p=Path(owned[-1]);cell=load(p);assert cell['status']=='proved_locally';cell['status']='independently_verified'
cell['evidence'].update(independent_verification=(r/'verified.json').as_posix(),execution_boundary=note,truth_boundary=note)
cell['source_detail_audit'].update(fidelity_boundary=note,gap='Actual deterministic bounce/rate/energy-layer laws are verified. Integrated hazard/first-clock and iid recursive path/nonexplosion, invariance and full paper/error/cost/composition remain independent.');write(p,cell)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';anchor=b'# Companion-paper formalization handoff'+nl+nl;assert b.startswith(anchor)
prefix=f"""## Exact PBPS bounce rate (2026-10-10)

Independent exact science74 VERIFIED commit {head}. The actual residual is
h=gradientV(x)-gradientV(xRef), R_h p=p-2 inner(p,h)h/norm(h)^2 with R_0=I,
S(x,p)=(x,R_h p), lambda=sqrt(eta) max(0,inner(p,h)). The complete ten-clause
theorem proves joint Borel S, continuous/Borel nonnegative lambda, zero branch,
involution/norm/pairing laws, actual weighted SUM H conservation and exact
flipped-rate difference. For E=H(z0), SAME-H-layer z satisfies the two radii and
lambda(z)<=sqrt(eta) beta sqrt(2E)(sqrt(2 eta E)+norm(c-xRef)),
c=y-eta gradientV(xRef). Beta-Lipschitz gradient is produced internally at r=0.
All six original analytic callers persist; no nonzero-normal, positive-energy,
positive-dimension, higher derivative or supplied-Lipschitz premise is added.
The exact211-line module and seven formula/BODY steps have independent math,
strict blind reconstruction, source review and exact-science verification.

This closes actual deterministic jump/rate prerequisites only. The verified
harmonic flow73 is a sibling for the later path construction, not a74 import.
Next bounded edge is actual rate-composed-with-flow integrated hazard and first
clock, following the independent prospective75 source plan. Algorithm1 has no
refresh clock. Recursive paths, iid clocks/nonexplosion, Markov memorylessness,
invariance/reversal, terminal kernel, full hypocoercivity/main/errors/caps,
expected-query costs and actual-input composition remain open. TV proximity
does not transfer unbounded costs. Existing Q_y/same-J disintegration and actual
reflected-law relation must be reused; no reference-law duplicate.

Serialized Registry523/imports/Tests, current reader/graph and mandatory
aggregate gates are pending against final admin state. ExactSCI, aggregate,
remoteCI/main/live, Exposition/PURIFIED and full-paper/Goal completion stay
distinct. PBPS/SPHMC actual-input composition precedes GaussianCloud/midpoint;
preserve older Chewi/frontiers/cycles/memory.

"""
p.write_bytes(anchor+prefix.encode().replace(b'\n',nl)+b[len(anchor):])
p=Path('website/content/samplewiki_companion_frontiers.json');x=load(p);x['execution']['current_checkpoint']='docs/companion-papers-handoff.md#exact-pbps-bounce-rate-2026-10-10';write(p,x)
p=Path('conversion-windows/ASTIS-SW-PBPS-2026.md');b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
text=f"""
## Exact bounce-rate checkpoint74 (2026-10-10)

Independent science commit {head}. Complete attributed statement and seven-step
formula proof are authored once in declaration_lessons/pbps-actual-bounce-rate.json;
exact full Lean including its complete private literal specification is adjacent
and initially folded. Actual S is zero-safe Borel and preserves the weighted SUM H.
Actual lambda is continuous, has the exact flipped-rate difference, and obeys the
printed SAME-H-layer Lambda bound with internal beta-Lipschitz producer. Original
six callers and legal zero-energy/rank0/zero-normal/alphaeta1 cases persist.
Actual integrated hazard/clock/recursive PDMP/nonexplosion/invariance/main/errors/
expected-querycost/actual-input composition remain open. Integration74 records
aggregate and current-reader checks separately; no Exposition/PURIFIED/main/live
or whole-paper/Goal completion follows.

"""
p.write_bytes(first+nl+text.encode().replace(b'\n',nl)+rest)
(out/'registry-entry74.json').write_text(json.dumps(entry,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS serialized74 prepared only after exactSCI: Registry523/import/Tests, one cell/handoff/conversion; aggregate and reader pending.')
