"""Integrate only independently commit-verified science through the existing lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R).returncode==0
lanes=[v for v in adv.current_advances().values() if v['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration92';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean',
 'docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json',
 'conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
    b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b)
    before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.relative_to(R).as_posix()))
(out/'owned-before.json').write_bytes((json.dumps(before,indent=2)+'\n').encode())
def after(name,anchor,text):
    p=R/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
    assert b.count(a)==1 and text.encode() not in b
    p.write_bytes(b.replace(a,a+text.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime','import '+module+'\n')
note=f'Independent science {science}. With the six original analytic hypotheses, canonical iid Exp(1) product P and literal stopped recursion, every finite n and T>=0 has a strict ordered-prefix complete-history law. Delta_n(T) is the open ordered time simplex with actual subtype comap of product Lebesgue measure. K gives all n+1 live time/state records; q is the product of n pre-bounce rates and elapsed segment survivals. Derive joint Borel K/q, actual history/observer/guard measurability, nonnegative real product, pointwise full-history reconstruction, H_*(P restricted to B)=K_*(q m), all nonnegative extended Borel test identities and integral q=P(B)<=1. Covers n0/T0/rank0/stopped/top/zero-input boundaries without new density or integrability providers. No terminal survival: not an exactly-n count law or full A7. Terminal survival/path/count assembly, restart/Markovness, invariance/hypocoercivity/errors/unbounded costs/main/composition/four-paper Goal remain OPEN.'
block='  {\n'+'\n'.join([
 '    key := "pbps.actualOrderedPrefix"','    localDecl := '+json.dumps(decl),
 '    upstreamDecl := "Actual PBPS strict ordered-prefix complete-history law"',
 '    upstreamFile := "arXiv2609.06905v1 Appendix A1 A1 A2 A7 finite iteration ingredient and Appendix A2"',
 '    status := LemmaMemoryStatus.formalizedLocal',
 '    tags := ["PBPS", "actual-input", "ordered-simplex", "finite-history", "density"]',
 '    saldUse := "Actual PBPS finite path-law substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 540')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 540',b'formalizedTechnicalLemmaCount = 541'))
prefix=f'''
## Actual PBPS ordered finite-prefix law (2026-10-11)

Independent science {science}. The six original analytic assumptions and
literal stopped exponential-clock recursion are unchanged. For every finite n
and T>=0, let Delta_n(T)={{0<s1<...<sn<T}}, with subtype comap m_n of product
Lebesgue measure. K_n(s) stores all n+1 live time/state records, initialized at
(0,z0), with each next state S Phi_(s_i-s_(i-1)) z_(i-1). Let

q_n(s)=product_i lambda(Phi_gap z_(i-1)) exp(-Lambda_(z_(i-1))(gap)).

A_n requires all-live, strictly increasing stored times and postinitial times
below T; it does not itself constrain record0. The actual H_n starts at(0,z0),
and B_n=H_n^-1(A_n). Derive Borel simplex/guard, joint parameter measurability
of K_n and q_n, actual H_n and time observers, and nonnegativity of qReal_n.
Every raw input in B_n reconstructs its entire history pointwise from observed
times. The actual unnormalized history law and all Borel ENNReal tests satisfy

H_n*(P restricted to B_n)=K_n*(q_n m_n),
integral_B_n F(H_n)dP=integral_Delta_n F(K_n(s))q_n(s)dm_n,
integral_Delta_n q_n dm_n=P(B_n)<=1.

The actual absolute-time one-step law91 supplies the recurrence. Exact event
splitting, state/history append, product factorization, Lebesgue insertion,
subtype Tonelli and the n=0 base close finite induction. No density, independence,
normalization, positive event probability or integrability premise was added.
n=0,T=0,rank0,stopped/infinite waits and raw zero clocks remain explicit.

Independent whole mathematics/kernel, blind decoding, primary-first source and
ten formula/Lean proof-region reviews and exact-commit verification passed.
Two implementation-only naming/visibility corrections were independently
reviewed; the full sealed public proposition never changed. Direct public
parents are actual91, harmonic flow, bounce rate, integrated hazard and the
canonical exponential-product probability normalization.

This closes the strict first-n prefix law, not an exactly-n count law: there is
no terminal survival factor. Terminal survival, endpoint/count/path identity,
hazard stitching and full A7 remain OPEN, as do restart/Markovness, invariance,
hypocoercivity, implementation errors, expected costs, main results and original
actual-input composition. Existing nonaccumulation78, interval coverage79 and
physical-time measurability80 remain verified. Four-paper Goal remains active.

Aggregate publication/site gates use the existing sole stabilization lane.
Rendered page/fine-branch acceptance, main merge, postmerge purification and
live deployment remain distinct. Continue the fixed four-paper priorities and
Chapter1.3 reader contract in execution metadata.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=R/owned[4];b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-next-absolute-event-time-law-2026-10-11';assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-ordered-finite-prefix-law-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual ordered finite-prefix92 (2026-10-11)\n\n{note}\n\nTen exact source-reviewed formula/Lean regions. Aggregate/rendered delivery/main merge/purification remain separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualOrderedPrefix',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_bytes((json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n').encode())
print('Prepared VERIFIED92 in sole lane: Registry541/imports/Tests; aggregate pending.')
