"""Run only after independent exact-commit VERIFIED; reuse the existing lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
load=lambda p:json.loads(Path(p).read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration78';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();s=out/f'{i}.before.exactraw.snapshot';s.write_bytes(b)
 before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=s.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
 assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation';decl=claim['target_declarations'][0]
after(owned[0],'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion','import '+module+'\n')
after(owned[1],'import AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct','import '+module+'\n')
note=f'Independently verified science {science}. Actual fixed-reference PBPS A2 event times under the canonical Exp1 product escape every finite horizon almost surely and have finite bounded-horizon index sets, including index0. Original six source analytic binders; no supplied iid/cap/recurrence/divergence provider. Zero cap stops and absorbs; positive cap controls clocks by actual divergent partial sums. No global physical-time path/Markov/invariance/kernel/hypocoercivity/main/error/expected-cost/composition or whole-paper/Goal completion. Aggregate/visual/main/PURIFIED/live remain distinct.'
block='  {\n'+'\n'.join(['    key := "pbps.actualNonaccumulation"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS event-time nonaccumulation"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 Ex8-Ex9 and SLLN/nonaccumulation"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "nonaccumulation", "exponential", "stopped"]','    saldUse := "PBPS global-path prerequisite; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 526')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 526',b'formalizedTechnicalLemmaCount = 527'))
prefix=f'''\n## Actual PBPS event-time nonaccumulation (2026-10-10)

Independent exact-science commit {science}. The actual finite stopped
recursion76 and canonical countable exponential product77 are genuine parents.
Under the original six analytic source hypotheses, for every fixed y/xRef/z0,
almost surely the actual event times exceed every finite horizon eventually,
and the sublevel event-index set is finite, including initialization index0.
Zero cap forces the first positive-threshold update to stop; absorption covers
all later indices. Positive cap gives T[n]>=sum(k<n,epsilon[k])/C0, including
stopped infinity times. The actual divergent threshold sums then imply escape.
No arbitrary iid/energy/cap/clock/recursion/divergence certificate is assumed.
WithTop atTop is not used as the target: escape does not require eventual stop.
The source direct Exp mean-one SLLN and the independently verified sufficient
ASTIS indicator-SLLN route remain explicit alternatives.

Seven complete formula/BODY steps, exact literal private statement and all
six original conditions passed independent math, blind reconstruction and
fresh source-first review. Next bounded mathematical boundary: construct the
actual state at every finite physical time from these finite stopped records,
including the last active arc on a stopped path; establish its measurability
and exact finite-prefix agreement before Markov/invariance. No global-path,
Markov/invariance/kernel, hypocoercivity/main/error/unbounded expected query
cost/composition claim follows from this clock result alone. Do not transfer
unbounded costs by TV. PBPS/SPHMC and actual-input composition remain first,
then Gaussian Cloud, then midpoint without extra higher derivative bounds.

The single existing stabilization lane carries this VERIFIED child. Serialized
aggregate/site/graph and page visual admission remain pending for this new
integration snapshot. Main merge, PURIFIED/Exposition, live deployment and
whole-paper/Goal completion are separate. The stale prospective module prose
and unused local positivity fact are recorded purification debts; neither
changes the sealed mathematical contract. Preserve all older work and memories.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-countable-exponential-inputs-2026-10-10'
assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-event-time-nonaccumulation-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual event-time nonaccumulation78 (2026-10-10)\n\nIndependent science {science}. Actual finite recursion plus canonical Exp1 inputs now give almost-sure finite-horizon escape and finite event-index sets. The complete six-condition statement and seven formula/BODY steps are authored once in pbps-actual-event-time-nonaccumulation lesson/publication, with adjacent initially folded exact Lean. Next is actual physical-time state construction/measurability; global process/Markov/invariance/main/cost/composition remain open. Aggregate, page visual, main/live and purification remain independently evidence-bound.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualNonaccumulation',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared verified SAU78 inside existing sole lane; Registry527/imports/Tests. Aggregate pending.')
