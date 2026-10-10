"""Execute only after exact science commit is independently VERIFIED."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());claim=load(r/'claim.json')
state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING'];assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration87';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw','import '+module+'\n')
note=f'Independent science {science}. Same six source analytic hypotheses and literal actual76 stopped recursion driven by actual77 iidExp1. For every deterministic n, actual history R0..Rn consumes raw coordinates k<n: derive ambient and F_n measurability, pointwise prefix causality, unchanged full infinite raw tail starting n, history-tail independence/product law and unnormalized restricted-tail pushforward, including n0/stopped/null A. Truncation is only a measurable proof factorization. Closes only probability substrate of G86-11/S87I1-I3; conditional random-hazard next-wait survival/density/final survival/iteration S87I4-I5/fullA7, random stopping/physical-time residual memorylessness/restart/Markov/invariance/allL2/main/error/unboundedcost/composition/wholepaper/Goal remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualFiniteHistoryTailLaw"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS deterministic finite history and unused entire clock tail"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A1 A2 deterministic iteration implicit A7 and AppendixA2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "finite-history", "prefix-measurability", "infinite-tail", "independence"]','    saldUse := "Actual PBPS conditional-iteration substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 535')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 535',b'formalizedTechnicalLemmaCount = 536'))
prefix=f'''
## Actual PBPS finite history and unused-clock tail law (2026-10-11)

Independent science {science}. For each deterministic event depth n, retain the
actual76 stopped recursion and the actual77 infinite iid Exp(1) product. The
history H_n=(R_0,...,R_n) uses only raw coordinates k<n; the entire raw tail
Y_n(w)_k=w_(n+k) starts at source E_(n+1). Under the same six source analytic
hypotheses, derive ambient measurability, pointwise prefix causality, explicit
F_n history measurability, unchanged tail law, history-tail independence and
joint product law. For every Borel history event A, including null events,
(Y_n)_*(P restricted to H_n^-1(A))=P(H_n^-1(A))*P without normalization.

The truncated threshold stream is only a measurable proof factorization; it
never changes the actual input distribution or dynamics. n=0, tagged stopped
histories, infinite waits and rank zero are included. All measurability, iid,
independence and law ingredients are produced internally, not source binders.
Six contiguous exact BODY regions accompany complete attributed restatement
and stepwise formula proofs. The independent source-blind reconstruction,
whole-source/kernel mathematics and primary-first anti-anchored source review
are separate evidence; three exposition-only fields were independently repaired.

Only S87-I1/I2/I3, the probability substrate of global G86-11, is closed. S87-I4
conditional random-hazard next-wait survival and S87-I5 finite density/final
survival/iteration remain OPEN. The immediate smaller next mathematical edge is
the unnormalized conditional next-wait survival identity under actual finite
history, using this entire-tail product law and actual75 deterministic survival.
Confirm it from the fresh capsule/source graph, source seal and reuse search
before assigning it. No random stopping index or physical-time residual clock
can be substituted into this deterministic-depth theorem.

FullA7/path law/reversal/invariance/restart/Markov/semigroup/allL2/hypocoercivity,
implementation/error/unbounded query costs/main/composition remain OPEN. Keep
PBPS/SPHMC and actual-input composition first, Gaussian Cloud second, midpoint
third without extra higher derivatives. No TV transfer of unbounded costs.
This VERIFIED child enters the existing sole stabilization lane; local aggregate,
reader visual/interactive checks, main merge, PURIFIED, live, wholepaper and Goal
completion remain distinct. Existing renderer scan includes the next compiler-option
wrapper as informational context in the literal-Prop disclosure; all actual
Prop and six BODY regions remain intact. No new renderer change is credited.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-finite-first-event-density-and-marked-law-2026-10-11';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-finite-history-and-unused-clock-tail-law-2026-10-11',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual finite history and unused-clock tail law87 (2026-10-11)\n\n{note}\n\nSix exact proof regions and adjacent folded literal Lean are published. Existing sole lane; local aggregate/browser/main/PURIFIED/live remain separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualFiniteHistoryTailLaw',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED87 in existing sole lane; Registry536/imports/Tests; aggregate pending')
