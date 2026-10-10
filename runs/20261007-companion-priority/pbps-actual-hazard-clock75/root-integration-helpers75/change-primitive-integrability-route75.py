from pathlib import Path
import json,os
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean');out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']);b=p.read_bytes();(out/'module.before.exactraw.lean').write_bytes(b);s=b.decode()
old='''    have hc : Continuous (fun s : ℝ => rate xRef (Φ y xRef s z)) :=
      hF.comp (show Continuous (fun s : ℝ => (((y, xRef), z), s)) from
        continuous_const.prodMk continuous_id)
    exact hc.intervalIntegrable _ _'''
new='''    have hsΦ : Continuous (fun s : ℝ => Φ y xRef s z) := by
      dsimp [Φ]
      fun_prop
    have hc : Continuous (fun s : ℝ => rate xRef (Φ y xRef s z)) :=
      hrate.comp (continuous_const.prodMk hsΦ)
    exact hc.intervalIntegrable a b'''
assert s.count(old)==1;s=s.replace(old,new);p.write_text(s,encoding='utf8',newline='\n')
(out/'diagnosis.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),failure_class='API_BLOCKED',retired_route='Definitional matching of hF joint-parameter continuity against the fixed-state interval integrand. Three related failures preserved; no fourth attempt or further heartbeat increase on that expression.',new_route='Direct elementary trigonometric continuity of the fixed actual harmonic orbit, followed by the already proved actual rate continuity and intervalIntegrable.',strict_reduction='Joint primitive continuity application now elaborates; bottleneck isolated to fixed-state interval integrability composition.',same_sealed_statement=True,no_added_hypotheses=True,local_budget_unchanged=800000),indent=2)+'\n',encoding='utf8',newline='\n')
