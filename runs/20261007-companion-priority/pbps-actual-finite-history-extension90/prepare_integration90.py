"""Existing sole stabilization owner; execute only after exact independent VERIFIED."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;load=lambda p:json.loads(p.read_bytes())
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']];assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit'];assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert load(r/'root.exact90.adoption.json')['science_commit']==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration90';out.mkdir(exist_ok=False)
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
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity','import '+module+'\n')
note=f'Independent science {science}. Same six original analytic hypotheses and literal stopped iid exponential-clock recursion. Derive Borel actual full next history H_(n+1), total complete-history append A(h,s) and lift L(h,s)=(A(h,s),s); preserve every old coordinate on every abstract history/real s. Live append uses cumulative T+max(s,0), raw-real harmonic flow and actual reflection; stopped append absorbs. Negative time is an auxiliary totalization only. On B={{0<W_n<d(H_n)}} for every fixed Borel finite-valued history cap d (possibly globally unbounded), derive pointwise actual H_(n+1)=A(H_n,finiteWait), restricted joint/marginal next-history pushforward laws and mass<=1, plus all jointly Borel ENNReal next-history/wait test identities localized to every Borel old-history event. No bounded/integrable test, positive event mass, normalization, density/finite-wait/no-atom/constructor provider. Four actual compiled public parents: conditional density89, history/tail87, harmonic flow and bounce rate; survival88 is not an AND dependency. Only one actual complete-history extension edge within S87-I5/G86-11 closes. Unrestricted next-history laws, ordered absolute-time iteration/final survival/path/count assembly/fullA7, physical-time residual restart/Markovness, global nonexplosion/invariance/hypocoercivity/errors/unbounded costs/main/composition/wholepaper/Goal remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualFiniteHistoryExtension"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS complete finite-history extension"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A1 A2 A7 update iteration ingredient and AppendixA2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "finite-history", "measurability", "restricted-law"]','    saldUse := "Actual PBPS ordered finite-event iteration substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 538')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 538',b'formalizedTechnicalLemmaCount = 539'))
prefix=f'''
## Actual PBPS complete finite-history extension (2026-10-11)

Independent science {science}. The six original analytic hypotheses and actual
stopped iid exponential-clock recursion are unchanged. For each deterministic
event depth n, H_n and H_(n+1) are COMPLETE tagged histories. Derive their actual
next-history measurability and the Borel total append A(h,s), preserving all old
coordinates and appending the last record:

live(T,z) -> live(T+max(s,0), S(Phi_s z)); stopped -> stopped.

L(h,s)=(A(h,s),s) is Borel. The raw real flow at negative s with clipped time
increment and stopped branch are auxiliary totalizations, not asserted physical
dynamics. For EVERY fixed Borel finite-valued d on old histories (possibly
globally unbounded), use89 D_d, mu_n and nu_d=D_d(mu_n product real Lebesgue).
For B_d={{0<W_n<d(H_n)}}, X_n=(H_n,finite_wait) and
Y_n=(H_(n+1),finite_wait), derive pointwise on actual B_d:

H_(n+1)=A(X_n), Y_n=L(X_n),
(Y_n)_*(P restricted to B_d)=L_*nu_d,
(H_(n+1))_*(P restricted to B_d)=A_*nu_d, (L_*nu_d)(univ)<=1.

Every jointly Borel F:Hist_(n+1) x real -> extended nonnegative reals has a
Borel parameter integral. For every Borel OLD-history event E,

integral_(B_d and H_n in E) F(Y_n) dP
  = integral_E [integral_real F(L(h,s)) D_d(h,s) ds] mu_n(dh).

No boundedness/integrability, positive event probability, normalization,
finite-wait/no-atom/density/constructor or independence premise was added.
Includes n=0,d=0,stopped/live-infinite waits, null events, rank zero and
unrealizable histories; missing outside-cutoff mass is not normalized.
Four genuine public kernel parents are conditional density89, actual
history/tail87, harmonic flow and bounce rate. Survival88 is not an AND parent.
Six exhaustive BODY regions120-340 accompany the attributed full statement and
formula proof with adjacent initially folded exact Lean. Independent whole
mathematics, fresh source-blind decoding, anti-anchored primary-first source
review and distinct two-field total-append formula repair acceptance are
separate native evidence. Lean, Statement Seal and decoder input did not change.

Only one actual complete-history extension edge inside S87-I5/G86-11 closes.
Unrestricted next-history law, ordered absolute-time iteration and final
survival/path/count assembly/full(A.7), physical-time residual memorylessness,
random stopping/restart/Markovness, global nonexplosion/invariance/semigroup/
all-L2/hypocoercivity, implementation/errors/unbounded costs/main/composition
and wholepaper/Goal remain OPEN. Read a fresh capsule and exact primary source
before choosing the next bounded actual-process edge; proof ingredients stay
dependencies, never new public hypotheses.

Use the existing sole stabilization lane. Actual page/fine-branch visual
acceptance, full Exposition Seal, main merge, postmerge PURIFIED and live
verification remain separate. Four-paper priorities and Chapter1.3 reading
requirements remain in execution metadata. PBPS/SPHMC and actual-input
composition precede Gaussian Cloud, then midpoint. No TV transfer of unbounded
costs or extra higher-derivative midpoint assumptions.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=R/owned[4];b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-conditional-finite-next-wait-density-2026-10-11';assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-complete-finite-history-extension-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual complete finite-history extension90 (2026-10-11)\n\n{note}\n\nSix exact proof regions; separately reviewed two-field total-append formula correction. Existing sole lane; local aggregate/actual browser/main/PURIFIED/live remain distinct.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualFiniteHistoryExtension',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared independently VERIFIED90 in sole lane; Registry539/imports/Tests; aggregate pending.')
