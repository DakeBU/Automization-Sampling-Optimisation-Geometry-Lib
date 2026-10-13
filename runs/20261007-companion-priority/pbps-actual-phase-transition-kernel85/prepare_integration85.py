"""Run only after independent exact-commit VERIFIED, inside the existing sole lane."""
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
out=r/'integration85';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();p=out/f'{i}.before.exactraw.snapshot';p.write_bytes(b);before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=p.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl;assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel';decl=claim['target_declarations'][0]
for p in owned[:2]:after(p,'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity','import '+module+'\n')
note=f'Independent science {science}. Under the original six analytic hypotheses retain actual80 single jointly measurable physical phase with all eleven literal definitions, live-arc/fallback and fixed-parameter common-AE finite-cover/initialization contract. Construct its full-phase probability kernel jointly indexed by y,reference,initial phase and finite time using actual Exp1 clocks. Exact pushforward/event law, Dirac zero-time law and dual L1 plus integral transfer for every bounded Borel real test are derived. IsMarkovKernel means probability fibers only. Actual process Markov/restart/Chapman-Kolmogorov, path reversal/invariance, all-L2 operators/contraction/density, hypocoercivity, implemented errors/unbounded costs/main/composition remain OPEN; actual browser/main/PURIFIED/live separate.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPhaseTransitionKernel"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS full-phase finite-time law and bounded measurable tests"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 p3.1 p5.2 p6.1"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "probability-kernel", "bounded-Borel-test"]','    saldUse := "Actual PBPS source transition-law interface; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 533')==1;p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 533',b'formalizedTechnicalLemmaCount = 534'))
prefix=f'''
## Actual PBPS jointly indexed full-phase law (2026-10-11)

Independent exact-science commit {science}. Retain the original six analytic
hypotheses, eleven literal definitions and the same actual80 physical phase Z.
Its actual Exp(1) clocks produce a full-phase probability kernel K, jointly
Borel in y, reference point, initial phase and every finite nonnegative time.
Every fiber is exactly P.map(Z); each Borel event has the corresponding exact
preimage probability. Fixed-parameter AE initialization gives K(y,r,z,0)=dirac(z).
For every Borel real test g and M>=0 with |g|<=M, both g under K and g(Z) under
P are integrable and their Bochner integrals agree. All are derived outputs.
The same Z and K precede all parameters and tests. Rank0 and M=0 are included.

Probability-fiber IsMarkovKernel does not assert process memorylessness,
restart or Chapman-Kolmogorov. The source failed-terminal-limit0 convention
and all-finite uncovered-initial-phase representative remain distinct. Only
fixed-parameter AE law compatibility is used; neither a parameter-uniform AE
event nor correlated random-parameter substitution is inferred.

Six contiguous formula/BODY regions passed independent mathematics, fresh
source-blind decoding and anti-anchored source review. The independently
reconstructed/reviewed source inventory16/node21/relation29 retains26 dependency
rows including6futureOPEN and3excluded associations. The actual kernel is an
optional representation for future invariance, not an invariance ingredient
or proof. Public kernel producers are exactly actual80 and UnitExp; private
specification/generated constants are retained in the complete kernel audit.
The generated reader graph is an incomplete name-scanned reference view;
actual proof dependencies are certified separately by that kernel audit.

Actual path-law expansion/reversal/invariance, restart/Markov/semigroup,
AE-safe all-L2/Jensen contraction/density/hypocoercivity and implemented errors,
unbounded expected query costs/main/composition remain OPEN. TV does not transfer
unbounded costs. Continue PBPS/SPHMC dependencies and actual-input composition,
then Gaussian Cloud, then midpoint without extra higher derivative assumptions.
Select one strict next edge from the current capsule and primary-source graph.

This VERIFIED child uses the existing sole stabilization lane. Local aggregate,
actual reader page/interactive visual, main merge/PURIFIED/live and full-paper/
Goal completion remain separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-bounded-test-outer-square-integral-continuity-2026-10-11';assert b.count(old)==1;b=b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-jointly-indexed-full-phase-law-2026-10-11',1)
old_date=b'    "updated": "2026-10-10",';assert b.count(old_date)==1;p.write_bytes(b.replace(old_date,b'    "updated": "2026-10-11",',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual jointly indexed full-phase law85 (2026-10-11)\n\nIndependent science {science}. The retained actual80 phase and actual Exp1 clocks yield a jointly Borel full-phase probability kernel, exact pushforward/event law and Dirac0 initialization. Every bounded Borel real test has dual L1 integrability and exact expectation transfer. Six exact adjacent formula/BODY regions; probability fibers do not assert process Markovness. Source failed0 and total fallbackinitialphase remain distinct. Path-law/reversal/invariance/restart/Markov/allL2/main/implementation/error/unbounded cost/composition and actual browser/main/PURIFIED/live remain OPEN.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualPhaseTransitionKernel',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared VERIFIED85 inside sole lane; Registry534/imports/Tests; aggregate pending')
