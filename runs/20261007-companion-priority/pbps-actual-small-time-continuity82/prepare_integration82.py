"""Execute only after independent exact-commit verification, in the sole lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING'];assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration82';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel','import '+module+'\n')
note=f'Independently verified science {science}. The actual jointly measurable phase satisfies measurable phase-flow defect <=1-exp(-Lambda_t), via the actual firstwait survival law and initial live arc. Each fixed y,xRef,z0 and positive real delta has measurable norm-tail probability tending to0 as NNReal t tends to0, including value0 by actual AE initialization. Original six conditions and full physical representative clauses retained. Full L2 strong continuity/Markov/restart/semigroup/invariance/hypocoercivity/implementation/main/cost/composition and visual/main/PURIFIED/live remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualSmallTimeContinuity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS first-event defect and zero-time stochastic continuity prerequisite"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 Ex22 and p6.1-p6.2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "first-event", "stochastic-continuity"]','    saldUse := "Source Ex22 pointwise small-time ingredient; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 530')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 530',b'formalizedTechnicalLemmaCount = 531'))
prefix=f'''
## Actual PBPS zero-time stochastic continuity (2026-10-10)

Independent exact-science commit {science}. The actual physical phase now obeys
P[Z_t != Phi_t(z0)] <= 1-exp(-Lambda(z0,t)), with the event measurable, for every
fixed y,xRef,z0 and finite t>=0. The zeroth coordinate under the actual exponential
product has Exp(1) law, so the already proved inverse-hazard survival probability
applies to the actual first wait. Before that wait, the initialized live interval
gives Z_t=Phi_t(z0). The defect event is contained in the first-event event; it is
not asserted equal, because an ineffective bounce or later return is possible.

For each real delta>0, the measurable phase norm-tail probability tends to0 as
NNReal t tends to0 in its ordinary nonpunctured neighborhood filter. Flow continuity
at0 and Lambda0=0 prove this by an eventual inclusion and probability squeeze.
The explicit source energy-cap Ct alternative is optional and unused. Finite/top
waits, rank0, threshold0 null inputs, halfopen endpoints and all prior measurable
representative/covered/fallback/common-AE clauses remain intact. All original six
analytic hypotheses are retained; no phase or probability-law producer is a premise.

Nine exact formula/BODY regions passed independent mathematical review, a fresh
source-blind reconstruction and primary-first exhaustive source coverage. A stale
prospective-header docstring and premature survival-step bound were corrected as
documentation only; the mathematical statement and BODY remained byte-identical.
This is the pointwise actual smalltime prerequisite of AppendixA1 Ex22. Full L2
strong continuity still requires its separate invariant-law/Jensen/contractivity,
dominated-convergence and density arguments. Process Markov/restart/semigroup,
invariance/hypocoercivity, implementation/error/query-cost/main and actual-input
PBPS-SPHMC composition remain OPEN. No arbitrary correlated input substitution or
uniform parameter event/limit is inferred. TV does not transfer unbounded costs.

Continue dependency-ready actual PBPS/SPHMC and composition work, then Gaussian
Cloud, then midpoint with no added higher derivatives. Select one next bounded
mathematical edge from the current capsule and source anchor, not old counts.
This VERIFIED child uses the sole existing stabilization lane. Local aggregate,
reader visual/main merge/PURIFIED/live and full-paper/Goal completion are separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#ideal-pbps-half-turn-returned-position-probability-kernel-2026-10-10';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-zero-time-stochastic-continuity-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual small-time stochastic continuity82 (2026-10-10)\n\nIndependent science {science}. Actual phase-flow defect <=1-exp(-Lambda_t) and every positive-threshold norm-tail probability tend to0 at NNReal0, under actual clocks for each fixed initial tuple. Original six hypotheses and complete actual phase semantics retained. Nine formula/BODY regions authored once beside exact folded Lean. Source Ex22 fullL2/invariance/Markov/semigroup/main/error/cost/composition remain OPEN; local aggregate, actual reader visual, main/PURIFIED/live distinct.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualSmallTimeContinuity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED82 inside sole existing lane; Registry531/imports/Tests; aggregate pending')
