"""Execute only after independent exact-science VERIFIED, in the existing sole lane."""
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
out=r/'integration84';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity','import '+module+'\n')
note=f'Independently verified science {science}. Under the original six analytic hypotheses, retain the entire actual83 phase and derive exact q_y=volume.tilted(-V-quadratic) and nu_y=q_y.prod(stdGaussian) probability. For every continuous real f with |f|<=M and M>=0, its actual independent-clock expectation A_t f is state measurable, its square discrepancy is nu_y-integrable and <=4M², and the outer square integral tends0 at ordinary NNReal0. C_b/4M² are ASTIS elaborations of source C_c bounded-test ingredient; no phase-invariance premise. Full all-L2 AE operator/invariance/Jensen/contraction/density/Markov/restart/semigroup/hypocoercivity/implementation/main/error/unbounded cost/composition and actual browser/main/PURIFIED/live remain OPEN.'
block='  {\n'+'\n'.join(['    key := "pbps.actualOuterBoundedL2Continuity"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS bounded-test outer square-integral prerequisite"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 Ex22 p6.2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "bounded-test", "dominated-convergence"]','    saldUse := "Source Ex22 bounded-test outer square-integral ingredient; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 532')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 532',b'formalizedTechnicalLemmaCount = 533'))
prefix=f'''
## Actual PBPS bounded-test outer square-integral continuity (2026-10-11)

Independent exact-science commit {science}. Retain the full actual83 physical
phase contract and the original six analytic hypotheses. Derive, rather than
assume, the exact conditional Gibbs probability q_y and initial phase law
nu_y=q_y x N(0,I). For each fixed y,xRef, every continuous real test with
|f|<=M and M>=0 has state-measurable actual clock expectation A_t f(z).
Its square discrepancy is integrable under nu_y and bounded everywhere by4M².
The actual83 expectation limit holds for every initial phase. Finite-probability
filter dominated convergence therefore gives integral (A_t f-f)² dnu_y ->0
at ordinary nonpunctured NNReal0. No phase invariance is a premise of this
bounded-test argument, and no samplewise AS limit is inferred.

The source uses C_c; bounded real C_b and explicit4M² are attributed ASTIS
elaborations. The same Z precedes every test and bound; rank0 and M=0 are
included. Eight exact contiguous formula/BODY regions passed independent
mathematics, fresh source-blind decoding and anti-anchored source review.
The independently rebuilt/reviewed source graph has47inventory/23nodes/
39relations:37dependency rows including5futureOPEN and2excluded associations.
Normalization alternatives remain whole OR routes with their ingredients AND.
The future density node is distinct from invariant-law/Jensen contraction.

This closes the bounded-test outer square-integral ingredient. Full all-L2
equivalence-class operators, phase invariance, Jensen/contraction and C_c
density remain OPEN, along with actual restart/Markov/semigroup/hypocoercivity,
implementation/error/unbounded expected oracle cost/main and PBPS-SPHMC
composition. TV does not transfer unbounded expected costs. Continue the current
PBPS/SPHMC dependencies/composition, then Gaussian Cloud, then midpoint without
adding higher derivative assumptions. Select the next strict mathematical edge
from the current capsule and independently reconstructed primary-source graph.

This VERIFIED child uses the existing sole stabilization lane. Local aggregate,
actual reader page/interactive visual, main merge/PURIFIED/live and full-paper/
Goal completion remain separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-bounded-test-clock-expectation-2026-10-10';assert b.count(old)==1;p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-bounded-test-outer-square-integral-continuity-2026-10-11',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual bounded-test outer square-integral84 (2026-10-11)\n\nIndependent science {science}. Exact conditional Gibbs and Gaussian product probabilities are derived from the six original hypotheses. The same actual83 phase gives state-measurable clock expectations;4M² dominates their squared discrepancy, and finite-probability filter DCT yields the outer integral limit0 at NNReal0. Eight exact adjacent formula/BODY regions; source C_c to C_b extension explicitly attributed. Full all-L2/invariance/contraction/density/process/main/error/unbounded cost/composition and actual browser/main/PURIFIED/live remain OPEN.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualOuterBoundedL2Continuity',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared independently VERIFIED84 inside sole existing lane; Registry533/imports/Tests; aggregate pending')
