from pathlib import Path
import hashlib,json,os
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean');r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']);b=p.read_bytes();(out/'module.before.exactraw.lean').write_bytes(b);s=b.decode()
old='(intervalIntegral.continuous_parametric_primitive_of_continuous hF).comp'
new='''(intervalIntegral.continuous_parametric_primitive_of_continuous
      (f := fun (q : (E × E) × (E × E)) (s : ℝ) =>
        rate q.1.2 (Φ q.1.1 q.1.2 s q.2)) (μ := volume) (a₀ := 0) hF).comp'''
assert s.count(old)==1;s=s.replace(old,new)
old='hF.comp (continuous_const.prodMk continuous_id)'
new='hF.comp (show Continuous (fun s : ℝ => (((y, xRef), z), s)) from\n        continuous_const.prodMk continuous_id)'
assert s.count(old)==1;s=s.replace(old,new);p.write_text(s,encoding='utf8',newline='\n')
(out/'diagnosis.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),failure_class='API_BLOCKED',diagnosis='The curried integrand f was not inferred from the uncurry-continuity argument; unresolved unification caused subsequent deterministic timeouts. Supply the exact actual integrand/volume/zero endpoint and fixed-state composition explicitly.',mathematical_route_changed=False,statement_changed=False,new_assumptions=False,prior_negative='focused-primitive-initial',maxHeartbeats_raised=False),indent=2)+'\n',encoding='utf8',newline='\n')
