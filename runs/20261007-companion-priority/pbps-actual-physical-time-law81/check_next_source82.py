"""Read-only source readiness receipt, not an SAU82 claim or theorem credit."""
from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
d=Path('runs/20261007-companion-priority/pbps-process-regularity-preread82')
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=d/'source_freeze82.raw-manifest.json'
assert sha(manifest.read_bytes())=='45253a0383bebeffe048730edfd738b4578f281d1a6b764e95abb2388253d3c1'
m=json.loads(manifest.read_bytes())
for group in ['raw_inputs','raw_outputs']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
paths=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean']
receipt=dict(status='SOURCE_PREREAD_AND_INITIAL_CURRENT_API_RETRIEVAL_ONLY',next_source_manifest=dict(path=manifest.as_posix(),RAW_sha256=sha(manifest.read_bytes())),source_only_candidate='Actual first-event defect bound and stochastic continuity at0, genuine A1.Ex22 consumer',initial_exact_parent_retrieval=[dict(path=p,RAW_sha256=sha(Path(p).read_bytes())) for p in paths],identity_clarification='Actual firstwait law is actual75 ActualHazardClock.actual_integrated_hazard_clock_laws; source preread numerical slot labels are role hints, never Lean declaration identities.',observed_apis=['actual80 existential jointly Borel actual Z with deterministic covered firstarc clause and retained actual definitions','actual76 literal initialized record and successor guarded at infinite wait; first event time requires explicit reduction','actual75 actual W=map(tau o clamp)Exp1 and exact survival exp(-Lambda), continuous Lambda with Lambda0=0','actual UnitExponentialProduct coordinate map exactly Exp1','Pinned Mathlib measureReal_mono/measureReal_compl provide generic probability floor'],still_required=['Safe current snapshot/fetch and current capsule at new scheduling boundary','Bounded reuse/upstream/frontier search completion','Exact complete candidate Statement Seal and independent header/source scope review','Actual new Lean proof and independent full reviews; not credited here'],new_SAU_claimed=False,new_Lean_proof=False,Goal_complete=False)
(r/'next-source82.readiness.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
print('Pinned source-only82 preread rechecked; current actual75/76/80/input APIs identified. No SAU82 admission or proof credit.')
