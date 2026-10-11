"""Execute only after an independent verifier admits the exact science commit."""
from pathlib import Path
import hashlib,json,subprocess,sys
R=Path(__file__).resolve().parents[3];r=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
load=lambda p:json.loads(p.read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED';science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).strip()
assert subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R).returncode==0
lanes=[v for v in adv.current_advances().values() if v['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration93';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
    b=(R/name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b)
    before.append(dict(path=name,raw_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.relative_to(R).as_posix()))
(out/'owned-before.json').write_bytes((json.dumps(before,indent=2)+'\n').encode())
def after(name,anchor,text):
    p=R/name;b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
    assert b.count(a)==1 and text.encode() not in b
    p.write_bytes(b.replace(a,a+text.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath';decl=claim['target_declarations'][0]
for name in owned[:2]:after(name,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix','import '+module+'\n')
note=f'Independent science {science}. Six source analytic assumptions and actual stopped iid exponential-clock recursion unchanged. For every finite n and deterministic finite nonnegative horizon T, the unnormalized joint complete-history/coordinate-product-path law on N(T)=n is the pushforward of ordered-prefix density times terminal survival. One jointly measurable actual phase supplies pointwise interpolation on raw survived events, fixed-T endpoint nullity, measurable count, AE finite cardinalities, raw disjointness and full-probability union. All nonnegative tests measurable for the stated sigma algebras and count-sector mass identities are proved. No extra probability, density, measurability, nonexplosion or integrability provider. Hazard stitching, pre-jump left limits, infinite full A7, Skorokhod compatibility, restart/Markovness, invariance/hypocoercivity, errors/cost/main/composition/four-paper completion remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualFiniteCountPath"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS finite-count complete-history and coordinate-path law"','    upstreamFile := "arXiv2609.06905v1 Appendix A1 A7 finite-count ingredient and Appendix A2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "finite-count", "history", "path-law"]','    saldUse := "Actual PBPS finite path-law substrate; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=R/owned[2];b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 541')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 541',b'formalizedTechnicalLemmaCount = 542'))
prefix=f'''## Actual PBPS finite-count complete-path law (2026-10-11)

Independent science {science}. The six original analytic assumptions,
canonical iid Exp(1) input and literal stopped recurrence are unchanged.
For each finite n and fixed T>=0, let K_n be the ordered prescribed history,
Gamma_n its finite interpolation, q_n the prefix density, and W the remaining
no-event survival from its terminal state. The proved actual joint law is

(H_n,Z_T)_*(P restricted to {{N(T)=n}})=(K_n,Gamma_n)_*((q_n W) m_n).

This includes joint measurability of total interpolation and density, measurable
count, pointwise complete-path identification on raw strict survived events C_n,
fixed-T endpoint nullity and AE count/cardinality interpretation. The raw C_n
are disjoint and their union has probability one. All nonnegative tests
measurable for the stated sigma algebras satisfy the corresponding integral
identity; each density mass is P(N(T)=n)<=1. Covers n=0, T=0, rank0, stopped and
infinite-wait cases. The path sigma algebra is coordinate-product. Fixed-T AE
no-event-at-T is not a uniform assertion over all real horizons.

Whole mathematics/kernel, source-blind decoding, primary-first source review,
nine adjacent formula/Lean regions and exact science-commit verification passed.
The sole implementation syntax correction opens the standard Classical scope;
its independent kernel/source transfer preserves the exact Statement Seal.

Aggregate publication/graph/site gates are handled by the existing sole lane.
Actual paper-page/fine-branch visual acceptance, main merge and postmerge
purification remain separate. Hazard stitching, pre-jump left limits, full A7,
Skorokhod compatibility, restart/Markovness, invariance, hypocoercivity, errors,
expected cost, main results and actual-input composition remain OPEN.
The four-paper Goal remains active. Next mathematical edge: source-faithful
hazard/left-limit rewriting and full A7, after this packet's aggregate delivery.

'''
p=R/owned[3];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';s=b.decode();start=s.index('## Actual PBPS finite-count complete-path law in progress');end=s.index('## Actual PBPS ordered finite-prefix law',start)
p.write_bytes((s[:start]+prefix.replace('\n',nl.decode())+s[end:]).encode())
p=R/owned[4];b=p.read_bytes();old=b'#actual-pbps-finite-count-complete-path-law-in-progress-2026-10-11';assert b.count(old)==1
p.write_bytes(b.replace(old,b'#actual-pbps-finite-count-complete-path-law-2026-10-11',1))
p=R/owned[5];b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual finite-count complete-path93 (2026-10-11)\n\n{note}\n\nNine source-reviewed adjacent formula/Lean regions. Aggregate/visual/main merge/purification acceptance remain distinct.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualFiniteCountPath',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with (R/owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
(out/'integration-scope.json').write_bytes((json.dumps(dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False),indent=2)+'\n').encode())
print('Prepared VERIFIED93 in sole lane: Registry542/imports/Tests; aggregate pending.')
