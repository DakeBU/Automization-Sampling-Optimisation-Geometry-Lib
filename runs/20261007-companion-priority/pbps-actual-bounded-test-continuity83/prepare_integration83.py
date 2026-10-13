"""Execute after exact-commit VERIFIED admission, in the existing sole lane."""
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
out=r/'integration83';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity','import '+module+'\n')
note=f'Independently verified science {science}. For the actual physical phase, every continuous real test f with global |f|<=M and M>=0 has measurable integrable clock pullbacks, |E f(Z_t)-f(Phi_t z0)|<=2M(1-exp(-Lambda_t)), and E f(Z_t)->f(z0) at ordinary NNReal0 for each fixed initial tuple. Original six analytic hypotheses, literal actual definitions and all prior physical/stochastic clauses retained. C_b and explicit2M are ASTIS elaboration of source C_c small-time step. Outer L2/invariant law/Jensen/contraction/density/Markov/restart/semigroup/hypocoercivity/implementation/main/error/cost/composition and actual browser/main/PURIFIED/live remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualBoundedTestContinuity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS bounded-test clock expectation prerequisite"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 Ex22 and p6.1-p6.2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "bounded-test", "integrability"]','    saldUse := "Source Ex22 pointwise clock-expectation ingredient; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 531')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 531',b'formalizedTechnicalLemmaCount = 532'))
prefix=f'''
## Actual PBPS bounded-test clock expectation (2026-10-10)

Independent exact-science commit {science}. For each fixed y,xRef,z0 and every
continuous real test f on phase space with a global bound |f|<=M and M>=0, the
actual clock pullback f(Z_t) is measurable and integrable for every finite t>=0.
The same actual phase representative satisfies
|E_P f(Z_t)-f(Phi_t z0)| <= 2M (1-exp(-Lambda(z0,t))).
On the measurable phase-flow defect event, the difference is bounded by2M;
off that event it is zero. Integrating its indicator under the actual probability
law and applying the independently verified first-event defect bound proves the
estimate. Continuity of Phi and Lambda at0, Lambda0=0, a squeeze and addition give
E_P f(Z_t)->f(z0) at ordinary nonpunctured NNReal0. No samplewise almost-sure
convergence is inferred from the preceding convergence-in-probability result.

All original six dynamics hypotheses, eleven literal actual definitions and all
prior covered/fallback/common-AE/initialization/defect clauses remain intact. A
single existential phase precedes all f and M. Rank0, M=0, threshold-zero null
inputs and infinite waits are included. The C_b test class and explicit2M bound
are attributed ASTIS elaborations of AppendixA1 Ex22's C_c pointwise ingredient.
Eight contiguous formula/BODY regions passed independent mathematics, a fresh
source-blind decoder and anti-anchored exhaustive primary-source review. The
independently reviewed source graph keeps the optional epsilon/delta branch's
two ingredients conjunctive and its whole route optional; the excluded-boundary
association is explicitly not a proved dependency.

This closes a bounded clock-expectation prerequisite. Outer L2 continuity still
requires its invariant phase law, Jensen/contraction and density arguments.
Markov/restart/semigroup/invariance/hypocoercivity, actual implementation/error/
unbounded expected oracle cost/main theorem and PBPS-SPHMC composition remain OPEN.
TV does not transfer unbounded expected costs. No uniform parameter conclusion
or arbitrary correlated clock replacement is inferred. Continue PBPS/SPHMC and
composition, then Gaussian Cloud, then midpoint without extra higher derivatives.
Choose the next bounded edge from the current capsule and exact source anchors.

This VERIFIED child uses the existing sole stabilization lane. Local aggregate,
actual reader page/interactive visual, main merge/PURIFIED/live and full-paper/
Goal completion remain separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-zero-time-stochastic-continuity-2026-10-10';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-bounded-test-clock-expectation-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual bounded-test expectation83 (2026-10-10)\n\nIndependent science {science}. Every globally bounded continuous real test of the actual physical phase is measurable and integrable under the actual clocks. The explicit2M phase-defect integral estimate yields pointwise clock-expectation continuity at NNReal0. Original six conditions and complete prior physical semantics retained. Eight formula/BODY regions authored once with adjacent folded Lean. C_b/2M are ASTIS elaborations of source C_c. Outer L2/invariance/Markov/semigroup/main/error/cost/composition and actual browser/main/PURIFIED/live remain OPEN.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualBoundedTestContinuity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED83 inside sole existing lane; Registry532/imports/Tests; aggregate pending')
