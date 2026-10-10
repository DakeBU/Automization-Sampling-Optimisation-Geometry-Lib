"""Run only after independent exact-commit VERIFIED, in the existing sole lane."""
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
out=r/'integration86';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','website/scripts/declaration_lessons.py']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel','import '+module+'\n')
note=f'Independent science {science}. Under the six original analytic hypotheses retain literal actual P/epsilon/c/Phi/S/rate/Lambda/tau and derive U from actual coordinate0. On A_T={{0<U<=T}}, prove exact finite first-event time density and SAME post-bounce marked law, mass1-exp(-LambdaT)<=1, three bounded Borel real-test L1 outputs and exact weighted Lebesgue integral. Finite mass is not renormalized; infinity/default0 excluded before projection. T0/M0/rank0/flat hazard/zero-normal identity remain included. Five key-lemma and six public BODY regions. Unused-tail conditioning, fullA7/path/reversal/invariance/restart/Markov/allL2/hypocoercivity/implementation/error/unboundedcost/main/composition remain OPEN. No TV-to-unbounded-cost inference; browser/main/PURIFIED/live/wholepaper/Goal separate.'
block='  {\n'+'\n'.join(['    key := "pbps.actualFiniteFirstEventLaw"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS first finite event density and post-bounce marked law"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A1 A2 first density factor implicit A7"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "first-event-density", "finite-subprobability", "post-bounce-law", "bounded-Borel-test"]','    saldUse := "Actual PBPS first density factor for source path law; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 534')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 534',b'formalizedTechnicalLemmaCount = 535'))
prefix=f'''
## Actual PBPS finite first-event density and marked law (2026-10-11)

Independent exact-science commit {science}. Under the six original analytic
hypotheses and the eight literal actual definitions, actual Exp(1) coordinate0
gives U=tau(epsilon0). Restrict to A_T={{0<U<=T}} before projecting its finite
waiting time. Its time law is exactly lambda(Phi_s z) exp(-Lambda_z(s)) ds on
(0,T], and mapping the SAME law through (s,S(Phi_s z)) gives the actual first
post-bounce marked law. Mass is1-exp(-Lambda_z(T))<=1 without renormalization;
the missing probability includes waits beyond T or infinite. Flat hazard,
zero-normal identity reflection, rank0, T=0 and M=0 are included.

For every bounded Borel real test on nonnegative-time x full phase, derive
integrability under the marked law, under actual restricted clocks, and for
the weighted Lebesgue integrand. Their exact Bochner integral identity follows.
Rate continuity, measurable clock/mark, density and all integrability are
produced dependencies, not new source premises. The proof uses the existing
actual75 survival, actual73 flow, actual74 bounce and UnitExponentialProduct;
the strictly new edge is the finite density and actual marked law.

Five explicit key-lemma proofs and six contiguous public BODY/formula regions
are published with initially folded exact Lean adjacent. The independent source
graph has47inventory/38nodes/76relations:73dependencies and3excluded associations,
all72independent primary anchors mapped (65leaf atoms plus7equation-row anchors). Its two sufficient density routes are OR choices,
each internally AND with the common Borel mark. The CDF/FTC route is implemented;
the inverse-hazard alternative is not an extra required premise. The source
graph remains distinct from the exact compiled kernel dependency certificate.

Next strict mathematical edge: derive the actual unused-clock-tail conditioning
at finite recursion depth, with a measurable actual-history interface and exact
canonical iid product law, before iterating first-event factors in(A.7). This is
pending, not a scheduled proof from old result counts; validate it against the
fresh capsule/source graph and ownership/reuse search before claiming a newSAU.

FullA7/final survival/path sigma algebra, density-value bounce adapter, reversal,
outer Tonelli/invariance, restart/Markov/semigroup, AE-safe allL2/Jensen/density,
hypocoercivity/implemented errors/unbounded query costs/main/composition remain
OPEN. TV proximity never transfers unbounded costs. Continue PBPS/SPHMC and
actual-input composition, then Gaussian Cloud, then midpoint without added
higher derivative bounds. Keep their independent theorem boundaries.

This VERIFIED child uses the existing sole stabilization lane. Local aggregate,
actual reader/interactive graph, main merge/PURIFIED/live and complete-paper/Goal
completion are distinct; no whole-paper completion is claimed.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-jointly-indexed-full-phase-law-2026-10-11';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-finite-first-event-density-and-marked-law-2026-10-11',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual finite first-event density and marked law86 (2026-10-11)\n\nIndependent science {science}. Original six analytic hypotheses and literal actual clocks/flow/reflection/hazard give the first finite waiting-time density on(0,T], its SAME post-bounce marked law, mass1-exp(-LambdaT)<=1 and three bounded Borel real-test L1 outputs plus weighted integral identity. No renormalization or added positive hazard/finite wait/regularity premise. Five keylemmas and six contiguous public BODY regions. Unused-tail conditioning/fullA7/path/reversal/invariance/Markov/allL2/main/implementation/error/unboundedcost/composition and actual browser/main/PURIFIED/live/wholepaper/Goal remain OPEN.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualFiniteFirstEventLaw',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED86 inside sole lane; Registry535/imports/Tests; aggregate pending')
