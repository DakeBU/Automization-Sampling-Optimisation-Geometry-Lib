"""Only the existing stabilization owner may execute, after exact science verification."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;load=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration89';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
before=[]
for i,name in enumerate(owned):
 b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b)
 before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
save(out/'owned-before.json',before)
def after(name,anchor,addition):
 p=R/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
 assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival','import '+module+'\n')
note=f'Independent science {science}. Same six original analytic hypotheses and literal stopped actual recursion. For every deterministic event depth n, every fixed Borel finite-valued cutoff d on full histories (no global bound), derive jointly Borel strict finite next-wait density D(h,s), the genuine Mathlib withDensity kernel K(h)=D(h,s)ds on every abstract history, uniform mass<=1/IsFiniteKernel, actual joint history/time measure identity, and all jointly Borel nonnegative extended test identities on every Borel history event A. No positive event probability, normalization, finite-wait/no-atom/density provider or bounded/integrable test premise. Restrict actual86 Ioc law further by Iio; never equate endpoint masses. Stopped histories have zero finite kernel; infinite waits remain outside finite component. Actual87 history/tail product, actual86 deterministic density, actual75 hazard, actual flow/rate and actual77 product are six genuine compiled parents; adjacent survival88 is not an AND dependency. Only density component of S87-I5/G86-11 closes. Ordered-time iteration, final survival/path factor, fullA7, residual restart/Markovness, global nonexplosion/invariance/hypocoercivity, implementation/errors/unbounded costs/main/composition/wholepaper/Goal OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualConditionalNextWaitDensity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS conditional finite next-wait density"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A1 A2 A7 strict finite density and AppendixA2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "conditional-density", "finite-history", "subprobability-kernel"]','    saldUse := "Actual PBPS ordered finite-event iteration substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 537')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 537',b'formalizedTechnicalLemmaCount = 538'))
prefix=f'''
## Actual PBPS conditional finite next-wait density (2026-10-11)

Independent science {science}. The six source analytic hypotheses and actual
stopped independent exponential-clock recursion are unchanged. At each
deterministic event depth n, let H_n be the full history with law mu_n. For every
fixed Borel finite-valued cutoff d(h), possibly unbounded across histories,

D_d(h,s) = 1_(0<s<d(h)) rate(Phi_s z) exp(-Lambda_z(s))

on a live last record; it is zero on stopped records. D_d is jointly Borel.
The genuine Mathlib density kernel satisfies K_d(h,ds)=D_d(h,s)ds for EVERY
abstract history, has mass at most1, and is a finite subprobability kernel.
For B_d={{0<W_n<d(H_n)}} and X_n=(H_n,finite_wait_time),

(X_n)_*(P restricted to B_d) = D_d (mu_n product real Lebesgue).

Every jointly Borel F:Hist_n x real -> extended nonnegative reals has a Borel
parameter integral. For every Borel history event A,

integral_(B_d and H_n in A) F(X_n) dP
  = integral_A [integral_real F(h,s) D_d(h,s) ds] mu_n(dh).

There is no boundedness/integrability premise on F, no positive mu_n(A),
normalization, density/independence provider, or finite-wait/no-atom premise.
Strict Ioo density follows by restricting actual86 Ioc law by Iio; no endpoint
mass equivalence is asserted. Stopped records have zero finite kernel; live
infinite waits remain outside this component. Includes n=0, d=0, zero hazards,
null A, rank zero and unrealizable histories. Kernel mass<=1 does not bound its
pointwise density.

Six genuine public compiled parents: actual87 full history/unused-tail product,
actual86 deterministic first-event density, actual75 hazard/clock, actual
harmonic flow and bounce rate, and actual77 unit-exponential product.
Survival88 is adjacent and is not a fabricated AND dependency. Six exhaustive
exact BODY regions accompany a complete attributed statement and formula proof,
with adjacent initially folded Lean. Independent whole mathematics, fresh
source-blind decoding and primary-first anti-anchored source review remain
separate native evidence. A distinctly reviewed one-field exposition overlay
removed the premature duplicate mass bound from step2; its proof stays in step4.
Lean, Statement Seal and decoder input did not change.

Only the finite-density component of S87-I5/G86-11 closes. Ordered-time
disintegration/iteration, final survival/path factor assembly, full(A.7),
physical-time residual memorylessness/random restart/Markovness, global
nonexplosion/invariance/semigroup/all-L2/hypocoercivity, implementation errors,
unbounded expected oracle costs, main theorem and composition remain OPEN.
Choose the next bounded edge from a fresh capsule and exact primary source,
using these conditional density and survival parents without provider premises.

Use the existing sole stabilization lane. Actual page/fine-branch visual
acceptance, full Exposition Seal, main merge, postmerge PURIFIED and live
verification remain separate. Do not infer them from DOM/SVG source checks.
Four-paper priorities and reading requirements remain in execution metadata.
PBPS/SPHMC and actual-input composition precede Gaussian Cloud, then midpoint;
no higher-derivative assumptions or TV transfer of unbounded costs.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=R/owned[4];b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-history-dependent-next-wait-survival-2026-10-11';assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-conditional-finite-next-wait-density-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual conditional finite next-wait density89 (2026-10-11)\n\n{note}\n\nSix exact proof regions; separately reviewed one-field exposition sequencing correction. Existing sole lane; local aggregate/actual browser/main/PURIFIED/live remain distinct.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualConditionalNextWaitDensity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared independently VERIFIED89 in sole lane; Registry538/imports/Tests; aggregate pending.')
