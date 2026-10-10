from pathlib import Path
import json, os

p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean')
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
b=p.read_bytes(); (out/'module.before.exactraw.lean').write_bytes(b); s=b.decode('utf8')
old='''    exact (hτle y xRef z 0 0).2 (by simp only [NNReal.coe_zero, (hbasic y xRef z).1])'''
new='''    exact (hτle y xRef z 0 0).2 (by
      simpa only [NNReal.coe_zero, (hbasic y xRef z).1] using (le_refl (0 : ℝ)))'''
assert s.count(old)==1; s=s.replace(old,new)
old='''    have ht : Measurable (fun e : ℝ => τ y xRef z (Real.toNNReal e)) :=
      hτmeas.comp
        (show Measurable (fun e : ℝ => ((y, xRef), z, Real.toNNReal e)) from
          measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal))'''
new='''    have hi : Measurable (fun e : ℝ => ((y, xRef), z, Real.toNNReal e)) :=
      measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal)
    have ht0 := hτmeas.comp hi
    have ht : Measurable (fun e : ℝ => τ y xRef z (Real.toNNReal e)) := ht0'''
assert s.count(old)==1; s=s.replace(old,new)
p.write_text(s,encoding='utf8',newline='\n')
(out/'diagnosis.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),
    failure_class='API_BLOCKED',
    strict_reduction='Folded primitive laws resolved all prior zero-value and IVT rewriting errors. Zero threshold now has only reflexive 0<=0 to discharge. Remaining timeout isolated to expected-type-driven elaboration of measurable composition.',
    repair='Infer the measurable composition without an expected result type, then ascribe its beta-reduced fixed-clock type. No heartbeat increase or mathematical route/statement change.',
    same_sealed_statement=True,no_added_hypotheses=True,
    unchanged_local_budget=1200000,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
