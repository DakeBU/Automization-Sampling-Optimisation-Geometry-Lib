"""Run only after independent exact-commit VERIFIED; reuse the existing lane."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79')
load=lambda p:json.loads(Path(p).read_bytes())
claim=load(r/'claim.json');state=adv.current_advances()[claim['advance_id']]
assert state['state']=='VERIFIED'
science=state['latest_evidence']['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==science
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
lanes=[s for s in adv.current_advances().values() if s['state']=='STABILIZING']
assert len(lanes)==1 and lanes[0]['advance_id']=='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner']=='companion_root_20261005'
out=r/'integration79';out.mkdir(exist_ok=False)
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
module='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover';decl=claim['target_declarations'][0]
after(owned[0],'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation','import '+module+'\n')
after(owned[1],'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNonaccumulation','import '+module+'\n')
note=f'Independently verified science {science}. With the original six analytic binders and canonical actual input, every finite physical time almost surely lies in a unique actual half-open event interval and selects a unique actual live record with stored time<=t and finite elapsed offset<actual next wait. No positive-wait/index/live-record/clock/nonaccumulation provider premise. Last live arc remains available when next wait is infinity. No global interpolation/measurability/origin/Markov/invariance/kernel/hypocoercivity/main/error/expected-cost/composition or whole-paper/Goal completion. Aggregate/visual/main/PURIFIED/live remain separate.'
block='  {\n'+'\n'.join(['    key := "pbps.actualPhysicalTimeCover"','    localDecl := '+json.dumps(decl),'    upstreamDecl := "Actual PBPS finite physical-time interval coverage"','    upstreamFile := "arXiv2609.06905v1 AppendixA1 A2, E2 and between-jump formula p2.2"','    status := LemmaMemoryStatus.formalizedLocal','    tags := ["PBPS", "actual-input", "physical-time", "interval", "stopped"]','    saldUse := "PBPS measurable physical-time interpolation prerequisite; no SALD claim"','    note := '+json.dumps(note)])+'\n  },\n'
after(owned[1],'def analysisMemory : List LemmaMemoryEntry := [',block)
p=Path(owned[2]);b=p.read_bytes();assert b.count(b'formalizedTechnicalLemmaCount = 527')==1
p.write_bytes(b.replace(b'formalizedTechnicalLemmaCount = 527',b'formalizedTechnicalLemmaCount = 528'))
prefix=f'\n## Actual PBPS finite physical-time interval coverage (2026-10-10)\n\nIndependent exact-science commit {science}. Actual finite recursion76 and\nactual nonaccumulation78 are genuine parents. With the original six analytic\nsource conditions and actual countable Exp1 inputs, almost surely every finite\nphysical time t belongs to one unique half-open event interval T[n]<=t<T[n+1].\nIts unique actual live record a has a.time<=t and finite nonnegative elapsed\nt-a.time strictly below its own actual next wait, including wait=infinity.\nZero-length intervals are empty; no strict positive-wait premise is added.\nA stopped next record does not remove the last live harmonic arc.\n\nNine complete formula/BODY steps and the exact sealed literal statement passed\nindependent mathematics, source-blind reconstruction and fresh source-first\nreview. Every source inventory node/edge was compared; initialization and\nphysical interpolation residuals remain PARTIAL/OPEN. Next bounded boundary is\na jointly measurable actual phase representative with common-AE all-time arc\nagreement and initialization derived from actual positive inputs. A total\nexceptional extension must be explicit; no global off-null-set uniqueness or\nmeasurable-selector/clock/nonexplosion certificate may be assumed.\n\nNo global physical-time interpolation/measurability/origin, path regularity,\nMarkov/invariance/kernel, hypocoercivity/main/error/expected query cost or\nPBPS-SPHMC composition completion follows from interval coverage alone.\nPBPS/SPHMC and actual-input composition remain first, then Gaussian Cloud,\nthen midpoint with no extra higher derivative bound. Do not transfer unbounded\ncost by TV. Preserve all older sources, routes, cycles and collaborator work.\n\nThe single existing stabilization lane carries this VERIFIED child. Serialized\naggregate/site/graph and page visual admission remain pending for this new\nintegration snapshot. Main merge, PURIFIED/Exposition, live deployment and\nwhole-paper/Goal completion remain separate. The explicit direct product import\nis optional purification debt, not a mathematical blocker.\n\n'

after(owned[3],'# Companion-paper formalization handoff',prefix)
p=Path(owned[4]);b=p.read_bytes();old=b'docs/companion-papers-handoff.md#actual-pbps-event-time-nonaccumulation-2026-10-10'
assert b.count(old)==1
p.write_bytes(b.replace(old,b'docs/companion-papers-handoff.md#actual-pbps-finite-physical-time-interval-coverage-2026-10-10',1))
p=Path(owned[5]);b=p.read_bytes();nl=b'\r\n' if b'\r\n' in b else b'\n';first,rest=b.split(nl,1)
txt=f'\n## Actual physical-time interval coverage79 (2026-10-10)\n\nIndependent science {science}. Actual finite recursion plus actual nonaccumulation now give a common-AE unique half-open interval, unique live stored record and finite elapsed<nextwait for every finite physical time. The complete six-condition statement and nine formula/BODY steps are authored once in pbps-actual-physical-time-cover lesson/publication, beside initially folded exact Lean. Next is an actual jointly measurable phase representative with all-time AE arc agreement and input-derived initialization; global process regularity/Markov/invariance/main/cost/composition remain open. Aggregate, page visual, main/live and purification are separate.\n\n'
p.write_bytes(first+nl+txt.encode().replace(b'\n',nl)+rest)
entry=dict(key='pbps.actualPhysicalTimeCover',local_decl=decl,local_file=claim['proposed_files'][0],status='formalized-local',verified_commit=science,evidence=state['latest_evidence'],next_action=note)
with Path(owned[6]).open('ab') as f:f.write((json.dumps(entry,ensure_ascii=False)+'\n').encode())
save(out/'integration-scope.json',dict(owned=owned,science_commit=science,single_stabilization_lane=lanes[0]['advance_id'],child_status='VERIFIED',aggregate='pending',visual='pending',Goal_complete=False))
print('Prepared verified SAU79 inside existing sole lane; Registry528/imports/Tests. Aggregate pending.')
