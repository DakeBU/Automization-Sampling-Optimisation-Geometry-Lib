from pathlib import Path
import json,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81')
p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-ideal-half-turn-kernel.json')
c=json.loads(p.read_bytes())
bad='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEventTimeNonaccumulation.actual_fixed_reference_event_time_nonaccumulation'
good='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws'
assert bad in c['parents']
for k in ['parents']:c[k]=[good if x==bad else x for x in c[k]]
for d,k in [(c['reuse_plan'],'reused_declarations'),(c['proof_digestion'],'existing_substrate')]:d[k]=[good if x==bad else x for x in d[k]]
p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
e=dict(classification='IMPLEMENTATION_FAILED',scope='Pre-proof DAG metadata identity typo only; exact header/source/Statement Seal mathematical bytes unchanged.',incorrect_proposal_identity=bad,correct_actual_consumed_identity=good,reason='Joint wait measurability is actual75 ActualHazardClock; nonaccumulation is already internal to actual80. Proposal raw historical typo retained, current Frontier Cell and forthcoming actual Lean/publication parents corrected.',statement_changed=False)
(r/'parent-identity-correction81.json').write_text(json.dumps(e,indent=2)+'\n')
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as a
a.checkpoint_advance('ASTIS-SA-20261010-PBPSIdealHalfTurnKernel',worker_id='companion_root_20261005',route_fingerprint='ideal-reference/kernel-product-map/fixed-time-AE/initial-law',progress_signature='header-sealed/body-first-focused-started/parent-identity-corrected',mathematical_delta='Exact statement sealed after two independent prospective reviews; first full BODY under focused compiler. Metadata parent typo corrected in canonical cell with raw historical proposal retained.',exact_residual='Focused compilation, independent BODY/semantic reviews and publication/integration OPEN. Correct parent identity recorded in runs/20261007-companion-priority/pbps-actual-physical-time-law81/parent-identity-correction81.json; no theorem/body result credit.')
