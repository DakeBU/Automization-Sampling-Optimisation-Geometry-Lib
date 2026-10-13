"""Run only after independent exact-commit VERIFIED; reuse the existing lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80')
load=lambda p:json.loads(Path(p).read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration80';out.mkdir(exist_ok=False)
owned=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','conversion-windows/ASTIS-SW-PBPS-2026.md','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl']
before=[]
for i,name in enumerate(owned):
 b=Path(name).read_bytes();s=out/f'{i}.before.exactraw.snapshot';s.write_bytes(b)
 before.append(dict(path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),snapshot=s.as_posix()))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(out/'owned-before.json',before)
def after(p,anchor,addition):
 p=Path(p);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';a=anchor.encode()+nl
 assert b.count(a)==1 and addition.encode() not in b
 p.write_bytes(b.replace(a,a+addition.encode().replace(b'\n',nl),1))
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability';decl=claim['target_declarations'][0]
after(owned[0],'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover','import '+module+'\n')
after(owned[1],'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover','import '+module+'\n')
note=f'Independently verified science {science}. Original six analytic source conditions and literal actual recursion yield a total phase representative jointly Borel in deterministic parameters, finite physical time and actual input stream. It agrees with every covering live harmonic arc; uncovered exceptional inputs use explicitly attributed initial-phase fallback. For each fixed deterministic parameter tuple, on one actual-product AE event it agrees with a live arc for every finite time and starts at z0. No uniform parameter AE event or correlated random-parameter substitution follows. Path regularity/adaptedness/Markov/invariance/kernel/hypocoercivity/main/error/expected-cost/composition remain open. Aggregate/visual/main/PURIFIED/live and whole-paper/Goal completion remain separate.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPhysicalTimeMeasurability"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS joint physical-time phase measurability and AE initialization"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A2, E2 and between-jump formula p2.2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "measurable", "initialization"]','    saldUse := "PBPS actual physical-time law/kernel construction prerequisite; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 528')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 528',b'formalizedTechnicalLemmaCount = 529'))
prefix=f'''
## Actual PBPS jointly measurable physical-time phase (2026-10-10)

Independent exact-science commit {science}. Actual finite recursion, harmonic
flow, positive actual inputs and interval coverage are genuine parents. Under
the original six analytic conditions, the actual phase has a total representative
jointly Borel in deterministic parameters, finite time and the input stream.
Every actual covering live interval selects its exact harmonic arc. When no
interval covers t, the initial-phase fallback is an explicit ASTIS representative
convention. A last live interval with infinite next wait remains an actual arc.

For every fixed deterministic parameter tuple, one actual-product almost-sure
event supports all finite times simultaneously and the representative starts
at z0. The proof derives positive first waiting time from actual positive inputs;
it does not add a positive-wait, clock, selector or nonexplosion provider premise.
Joint measurability does not turn these separate fixed-parameter AE statements
into a uniform event or justify arbitrary correlated random initialization.

Nine complete formula/BODY steps and the exact sealed statement passed independent
mathematics, source-blind reconstruction and fresh source-first review. Actual
interval assembly, measurability and fixed-parameter AE initialization are now
closed within this precise boundary. Path regularity, adaptedness, Markov and
probability-kernel semantics, invariant law, hypocoercivity, main error and expected
query cost, and actual-input PBPS-SPHMC composition remain OPEN. These results do
not complete PBPS or the four-paper Goal; no unbounded cost is transferred by TV.

PBPS/SPHMC and their actual-input composition remain first, then Gaussian Cloud,
then midpoint with no added higher derivative bound. Preserve all older sources,
routes, cycles and collaborator work. The single existing stabilization lane
carries this VERIFIED child. Serialized aggregate/site/graph and page visual
admission remain pending for this new integration snapshot. Main merge,
PURIFIED/Exposition, live deployment and whole-paper/Goal completion remain separate.

'''
after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-finite-physical-time-interval-coverage-2026-10-10';assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-jointly-measurable-physical-time-phase-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual jointly measurable physical-time phase80 (2026-10-10)\n\nIndependent science {science}. The actual finite recursion, harmonic flow and interval cover now produce a total jointly Borel phase, exact on every covering live interval, with explicit ASTIS fallback on uncovered exceptional inputs. For each fixed deterministic parameter tuple, one common-AE event gives all-time actual arc agreement and initialization at z0. No uniform parameter AE or arbitrary correlated random initialization is inferred. Complete original six-condition statement and nine formula/BODY steps are authored once in pbps-actual-physical-time-measurability lesson/publication beside folded exact Lean. Process regularity/adaptedness/Markov/kernel/invariance/main/cost/composition remain open. Aggregate, page visual, main/live and purification are separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualPhysicalTimeMeasurability',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared verified SAU80 inside existing sole lane; Registry529/imports/Tests. Aggregate pending.')
