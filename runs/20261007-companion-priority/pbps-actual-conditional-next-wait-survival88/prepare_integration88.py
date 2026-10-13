"""Run only after independent exact science-commit VERIFIED admission."""
from pathlib import Path
import json,hashlib,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;load=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration88';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=R/p;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
 assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw','import '+module+'\n')
note=f'Independent science {science}. Same six original analytic hypotheses and literal actual stopped recursion. For every deterministic event depth n, Borel duration d of complete history H_n and Borel event A, derive joint next-wait event measurability, Borel weight q_d in [0,1], and P(H_n in A and live next wait>d(H_n))=integral_A q_d d(map H_n P). Stopped histories have zero weight; live infinite waits survive all finite durations. No normalization, boundedness of d or law/measurability provider premise. Actual87 joint history/tail law, actual75 hazard survival and actual77 coordinate law are compiled parents. Only S87-I4 closes. S87-I5 conditional finite-wait density, ordered-time disintegration/iteration, final factor/fullA7, random-depth and physical-time residual restart/Markov/invariance/cost/main/composition/wholepaper/Goal remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualConditionalNextWaitSurvival"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS history-dependent next-wait conditional survival"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A1 A2 survival implicit A7 and AppendixA2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "conditional-survival", "finite-history", "random-duration"]','    saldUse := "Actual PBPS finite-event iteration substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 536')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 536',b'formalizedTechnicalLemmaCount = 537'))
prefix=f'''
## Actual PBPS history-dependent next-wait survival (2026-10-11)

Independent science {science}. Keep the original six analytic hypotheses and
literal actual stopped recursion. For each deterministic event depth n let
H_n=(R_0,...,R_n), with law mu_n. For every Borel finite-valued nonnegative
duration function d on the complete history space and Borel history event A,
derive the exact unnormalized identity

P(H_n in A and R_n live and next wait > d(H_n))
  = integral_A q(h_n,d(h)) mu_n(dh),

where q(live(T,z),u)=exp(-Lambda_z(u)) and q(stopped,u)=0. The joint survival
event is Borel; the weight is Borel and lies in [0,1] on every history, including
unrealizable histories. d itself is a fixed Borel test function; d(H_n) can be
random. d need not be bounded and A need not have positive probability.
Live infinite waits survive every finite duration; stopped records have no
fictitious next phase. n=0, zero rates, null events and rank zero are included.

The proof consumes actual87 joint history/tail product, actual75 joint Borel
hazard/clock and deterministic survival, and actual77 coordinate law. These are
internal dependencies, never additional source premises. Five exhaustive exact
BODY regions accompany attributed complete statement and stepwise formula
proofs, with adjacent initially folded Lean. Independent whole mathematics,
source-blind decoding and primary-first anti-anchored source review are separate
native evidence. No mathematical or exposition repair was required.

Only S87-I4 conditional survival is now closed. S87-I5 conditional finite-wait
density, ordered-time disintegration/iteration and final factor assembly remain
OPEN; full(A.7) is not completed. The next bounded mathematical edge must be
selected from a fresh capsule and pinned source: derive the conditional finite
next-wait density, reusing the existing actual86 deterministic first-event law
and this history-dependent integration. Inspect exact requirements for a Borel
time-varying test before sealing it; do not introduce density providers.

Physical-time residual memorylessness, random-depth stopping/restart/Markovness,
path law/reversal/invariance/semigroup/all-L2/hypocoercivity, implementation
error/unbounded query cost/main/composition remain OPEN. Keep PBPS/SPHMC and
actual-input composition first, Gaussian Cloud second, midpoint third without
extra higher derivatives. No TV transfer of unbounded costs. This independently
VERIFIED child uses the existing sole stabilization lane. Local aggregate,
actual page/fine-branch visual checks, main merge, PURIFIED, live, wholepaper and
Goal completion remain distinct; no browser acceptance is inferred from DOM.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=R/owned[4];b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-finite-history-and-unused-clock-tail-law-2026-10-11';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-history-dependent-next-wait-survival-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual conditional next-wait survival88 (2026-10-11)\n\n{note}\n\nFive exact proof regions and adjacent folded Lean. Existing sole lane; local aggregate/actual browser/main/PURIFIED/live remain distinct.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualConditionalNextWaitSurvival',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared independently VERIFIED88 in existing sole lane; Registry537/imports/Tests; aggregate pending.')
