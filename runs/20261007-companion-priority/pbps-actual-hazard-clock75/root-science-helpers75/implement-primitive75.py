from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-clock-preproof75');r=pre.parent/'pbps-actual-hazard-clock75'
seal=json.loads((pre/'root.statement-seal75.json').read_bytes());header=Path(seal['header']['path']).read_text(encoding='utf8');assert hashlib.sha256(header.encode()).hexdigest()==seal['header']['RAW_sha256']
assert json.loads((r/'preproof-admission.json').read_bytes())['status']=='CLAIMED_EXPLORING_NOT_PROVED'
prefix,telescope=header.split('theorem actual_integrated_hazard_clock_laws\n',1)
binders=telescope.split(' :\n    actual_integrated_hazard_clock_statement',1)[0]
lets=header[header.index('    let c :'):header.index('    let τ :')]
first=header[header.index('    Continuous (fun a : ((E × E)'):header.index('    (∀ y xRef : E, ∀ z : E × E, ∀ e t : ℝ≥0,')]
cap=header[header.index('    (∀ y xRef : E, ∀ z : E × E, 0 ≤ C'):header.index('    (∀ y xRef : E, ∀ z : E × E, ∀ e : ℝ≥0,\n      (0 < C')].removesuffix(' ∧\n')
assert cap.endswith('))')
body='''
  have hf := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hb := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hΦ : Continuous (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) := hf.1
  have hrate : Continuous (fun a : E × (E × E) => rate a.1 a.2) := hb.2.1
  have hrate0 (xRef : E) (z : E × E) : 0 ≤ rate xRef z :=
    (hb.2.2.2.2.2.2.2.1 xRef z).1
  have henergy (y xRef : E) (s : ℝ) (z : E × E) :
      H y xRef (Φ y xRef s z) = H y xRef z := hf.2.2.2.2.2.2.2.1 y xRef s z
  have hcap (y xRef : E) (z : E × E) (s : ℝ) :
      rate xRef (Φ y xRef s z) ≤ C y xRef z :=
    (hb.2.2.2.2.2.2.2.2.2 y xRef z).2 (Φ y xRef s z) (henergy y xRef s z) |>.2.2
  have hC (y xRef : E) (z : E × E) : 0 ≤ C y xRef z := by
    dsimp [C]
    positivity
  have hF : Continuous (fun a : ((E × E) × (E × E)) × ℝ =>
      rate a.1.1.2 (Φ a.1.1.1 a.1.1.2 a.2 a.1.2)) := by
    exact hrate.comp (continuous_fst.fst.snd.prodMk
      (hΦ.comp ((continuous_fst.fst).prodMk
        (continuous_snd.prodMk continuous_fst.snd))))
  have hΛ : Continuous (fun a : ((E × E) × (E × E)) × ℝ≥0 =>
      Λ a.1.1.1 a.1.1.2 a.1.2 a.2) := by
    exact (intervalIntegral.continuous_parametric_primitive_of_continuous hF).comp
      (continuous_fst.prodMk (NNReal.continuous_coe.comp continuous_snd))
  have hInt (y xRef : E) (z : E × E) (a b : ℝ) :
      IntervalIntegrable (fun s : ℝ => rate xRef (Φ y xRef s z)) volume a b := by
    have hc : Continuous (fun s : ℝ => rate xRef (Φ y xRef s z)) :=
      hF.comp (continuous_const.prodMk continuous_id)
    exact hc.intervalIntegrable _ _
  have hbasic (y xRef : E) (z : E × E) :
      Λ y xRef z 0 = 0 ∧ (∀ t : ℝ≥0, 0 ≤ Λ y xRef z t) ∧
      Monotone (Λ y xRef z) := by
    refine ⟨by simp [Λ], ?_, ?_⟩
    · intro t
      exact intervalIntegral.integral_nonneg_of_forall t.coe_nonneg
        (fun s => hrate0 xRef (Φ y xRef s z))
    · intro s t hst
      exact intervalIntegral.integral_mono_interval (le_refl 0) s.coe_nonneg
        (show (s : ℝ) ≤ t from hst)
        (Filter.Eventually.of_forall (fun u => hrate0 xRef (Φ y xRef u z)))
        (hInt y xRef z 0 t)
  have hbound (y xRef : E) (z : E × E) (t : ℝ≥0) :
      Λ y xRef z t ≤ C y xRef z * (t : ℝ) := by
    have hi := intervalIntegral.integral_mono_on t.coe_nonneg
      (hInt y xRef z 0 t) (intervalIntegrable_const (μ := volume))
      (fun s _ => hcap y xRef z s)
    simpa only [intervalIntegral.integral_const, sub_zero, smul_eq_mul, mul_comm] using hi
  exact ⟨hΛ, hΛ.measurable, fun y xRef z t => hInt y xRef z 0 t,
    hbasic, fun y xRef z => ⟨hC y xRef z, hbound y xRef z⟩⟩
'''
text=prefix+'private theorem actual_hazard_primitive_laws\n'+binders+' :\n'+lets+first+cap+' := by\n'+''.join(s[2:]+'\n' for s in lets.splitlines())+'  change\n'+first+cap+'\n'+body+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock\n'
p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean');assert not p.exists();p.write_text(text,encoding='utf8',newline='\n')
(r/'primitive-first-attempt.json').write_text(json.dumps(dict(status='INTERNAL_PRIMITIVE_EDGE_ONLY_FULL75_UNPROVED',actual_root_PID=os.getpid(),sealed_header_sha256=seal['header']['RAW_sha256'],public75_theorem_implemented=False,truth_boundary='Internal cumulative-hazard prerequisites only; full sealed ten-clause actual first-clock theorem remains open.',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
