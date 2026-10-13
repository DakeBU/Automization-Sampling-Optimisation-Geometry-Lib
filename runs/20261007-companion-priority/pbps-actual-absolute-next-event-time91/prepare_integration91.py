"""Run only after independent exact-commit verification, in the existing sole lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent
sys.path.insert(0,str(R/'tools'))
import astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED'
science='d62f7b2c89e749953a36d8922124865a4651e55e'
assert state['latest_evidence']['verified_commit']==science
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==science
assert load(r/'root.exact91.adoption.json')['science_commit']==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R).returncode==0
lanes=[v for v in adv.current_advances().values() if v['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration91';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean',
 'docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json',
 'conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
    b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b)
    before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.relative_to(R).as_posix()))
(out/'owned-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8',newline='\n')
def after(name,anchor,text):
    p=R/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
    assert b.count(a)==1 and text.encode() not in b
    p.write_bytes(b.replace(a,a+text.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension','import '+module+'\n')
note=f'Independent science {science}. Under the six original analytic assumptions, actual U reads the next stopped/live record. For each deterministic depth and every Borel finite-valued history horizon b, derive Borel observers/absolute append, all-prefix preservation, strict event equality Brel=B, actual guarded U=a+wait and complete-history append. The actual old-history/U law restricted to B has density D(h,u)=1_(a(h)<u<b(h))*rho(h_last,u-a(h)) against mu_n product real Lebesgue. Every-history density integral and total mass are at most1. Derive next-history joint/marginal transport and all joint ENNReal tests on all old-history events, including null events, without normalization or integrability premises. Direct parents90,89 and canonical exponential-product probability. Fiberwise translation plus Tonelli implements the needed weighted law; no separate broad unweighted shear theorem is claimed. Ordered iteration, final survival/path/count/fullA7, restart/Markov/invariance/hypocoercivity/errors/unbounded costs/main/composition/wholepaper/Goal remain OPEN.'
block='  {\n'+'\n'.join([
 '    key := "pbps.actualAbsoluteNextEventTime"',
 '    localDecl := '+json.dumps(decl),
 '    upstreamDecl := "Actual PBPS next absolute-event-time law"',
 '    upstreamFile := "arXiv2609.06905v1 Appendix A1 A1 A2 A7 coordinate ingredient and Appendix A2"',
 '    status := LemmaMemoryStatus.formalizedLocal',
 '    tags := ["PBPS", "actual-input", "absolute-time", "finite-history", "density"]',
 '    saldUse := "Actual PBPS ordered event-time iteration substrate; no SALD claim"',
 '    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 539')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 539',b'formalizedTechnicalLemmaCount = 540'))
prefix=f'''
## Actual PBPS next absolute-event-time law (2026-10-11)

Independent science {science}. Keep the six original analytic hypotheses and
literal stopped recursion driven by the canonical iid Exp(1) product P. At each
deterministic depth n, H and Hnext are the complete old/next histories. Let
a(h) read the old last record time, and U(w) read the actual next record time;
both use0 on stopped records as an explicit auxiliary fallback.

For every fixed Borel finite-valued history horizon b, possibly globally
unbounded, define d(h)=max(b(h)-a(h),0) and

D(h,u)=1_(a(h)<u<b(h))*rho(h_last,u-a(h)), mu=H_*P, nu=D(mu product du).

Derive Borel H,Hnext,a,U, absolute append A(h,u)=A_rel(h,u-a(h)) and lift
L(h,u)=(A(h,u),u). Every old coordinate is preserved. Absolute append uses
raw-real harmonic flow and cumulative T+max(u-T,0) on a live last record;
negative-time/stopped cases remain auxiliary totalizations.

The relative event Brel={{0<W_n<d(H)}} equals pointwise the actual event
B={{old and next records live; a(H)<U<b(H)}}. On B derive U=a(H)+finite_wait
and Hnext=A(H,U), using the literal next-record recursion. Joint D is Borel
and every abstract history satisfies integral D(h,u)du<=1. With X=(H,U),
Y=(Hnext,U), derive

X_*(P restricted to B)=nu, Y_*(P restricted to B)=L_*nu,
Hnext_*(P restricted to B)=A_*nu, nu(univ)<=1.

All jointly Borel ENNReal tests G(h,u) and F(hnext,u) have Borel parameter
integrals and exact unnormalized iterated-integral identities localized to
every Borel old-history event, including null events. No boundedness,
integrability, positive event mass, finite-wait/no-atom/density/normalization
or independence provider was added. Includes rank0,n=0,zero hazard,stopped,
live infinite waits,b<=a and unrealizable histories.

Independent whole mathematics/kernel and leaf build, fresh blind decoder,
primary-first anti-anchored source review and exact-commit verification passed.
Seven exact BODY regions142-527 accompany the full attributed statement and
formula proof. Direct public parents are90,89 and canonical UnitExponentialProduct
probability normalization. The implemented fiber translation plus Tonelli closes
the needed weighted coordinate law; it does not claim the broader planned
standalone unweighted shear/inverse theorem in source node S91-T.

Only this strict next absolute-coordinate edge closes. Ordered finite iteration,
terminal survival/path/count identification and full(A.7), physical-time
restart/Markovness, invariance/semigroup/all-L2/hypocoercivity, implementation
errors/unbounded costs/main/composition/full papers/Goal remain OPEN. Existing
actual-input nonaccumulation78 and half-open physical-time coverage79 remain
verified; they are not reopened by the missing full path-density assembly.

The existing sole stabilization lane handles aggregate/publication/graph/site
checks. Actual page/fine-branch visual acceptance, main merge, postmerge
purification and live verification remain separate. Continue the four fixed
papers in execution priority, with Chapter1.3 reading standards, no TV transfer
of unbounded costs and no added higher derivatives for midpoint.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=R/owned[4];b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-complete-finite-history-extension-2026-10-11';assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-next-absolute-event-time-law-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual next absolute-event-time91 (2026-10-11)\n\n{note}\n\nSeven exact proof regions with independent source and mathematical acceptance. Whole integration/rendered delivery/merge/purification remain separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualAbsoluteNextEventTime',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_text(json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('Prepared VERIFIED91 in sole lane: Registry540/imports/Tests; aggregate pending.')
