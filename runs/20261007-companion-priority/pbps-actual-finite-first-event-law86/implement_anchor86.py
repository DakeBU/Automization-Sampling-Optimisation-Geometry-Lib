from pathlib import Path
R=Path('E:/Samplinglib')
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean'
s=M.read_text(encoding='utf-8-sig')
assert 'theorem actual_finite_first_event_law\n' not in s
header=s[s.index('    {E : Type*}'):s.index(' : Prop :=')]
definitions=s[s.index('    let P :'):s.index('    ∀ y xRef : E')]
definitions='\n'.join(x[2:] for x in definitions.splitlines())+'\n'
conclusion=s[s.index('    ∀ y xRef : E'):s.index('\n\n-- Internal FTC')]
conclusion='\n'.join(x[2:] for x in conclusion.splitlines())
proof=r'''
  rcases ActualHazardClock.actual_integrated_hazard_clock_laws hα hαβ hV hH hη hβη with
    ⟨hΛC, _, _, hΛbasic, _, _, hτM, hW, _, _⟩
  have hflow := ActualHarmonicFlow.actual_harmonic_flow_laws hα hαβ hV hH hη hβη
  have hb := ActualBounceRate.actual_bounce_rate_energy_laws hα hαβ hV hH hη hβη
  have hinput :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws
  letI : IsProbabilityMeasure P := hinput.1
  intro y xRef z
  have hφ : Continuous (fun s : ℝ => Φ y xRef s z) :=
    hflow.1.comp (continuous_const.prodMk (continuous_id.prodMk continuous_const))
  let l : ℝ → ℝ := fun s => rate xRef (Φ y xRef s z)
  have hl : Continuous l := hb.2.1.comp (continuous_const.prodMk hφ)
  have hn (s : ℝ) : 0 ≤ l s := hb.2.2.2.2.2.2.2.1 xRef (Φ y xRef s z) |>.1
  let g : ℝ → WithTop ℝ≥0 := fun e => τ y xRef z (Real.toNNReal e)
  have hgM : Measurable g :=
    hτM.comp (measurable_const.prodMk (measurable_const.prodMk measurable_real_toNNReal))
  have hUM : Measurable (U y xRef z) := hgM.comp (measurable_pi_apply 0)
  have hFM : Measurable (F y xRef z) := measurable_subtype_coe.comp (hUM.untopD 0)
  have hJM : Measurable (J y xRef z) :=
    measurable_real_toNNReal.prodMk (hb.1.comp (measurable_const.prodMk hφ.measurable))
  have hUlaw : P.map (U y xRef z) = (expMeasure (1 : ℝ)).map g := by
    calc
      P.map (U y xRef z) = (P.map (fun sample : ℕ → ℝ => sample 0)).map g :=
        (Measure.map_map hgM (measurable_pi_apply 0)).symm
      _ = (expMeasure (1 : ℝ)).map g := by rw [(hinput.2.1 0).2.2]
  have hsurv (t : ℝ≥0) :
      P.real {sample | (t : WithTop ℝ≥0) < U y xRef z sample} =
        Real.exp (-Λ y xRef z t) := by
    calc
      P.real {sample | (t : WithTop ℝ≥0) < U y xRef z sample} =
          (P.map (U y xRef z)).real (Set.Ioi (t : WithTop ℝ≥0)) :=
        (map_measureReal_apply hUM measurableSet_Ioi).symm
      _ = Real.exp (-Λ y xRef z t) := by
        rw [hUlaw]
        exact (hW y xRef z).2 t
  have hLC : Continuous (Λ y xRef z) :=
    hΛC.comp (continuous_const.prodMk continuous_id)
  have hdC : Continuous (d y xRef z) :=
    hl.mul (hLC.comp continuous_real_toNNReal).neg.rexp
  have hdn (s : ℝ) : 0 ≤ d y xRef z s := mul_nonneg (hn s) (Real.exp_pos _).le
  refine ⟨hUM, hFM, hJM, ?_⟩
  intro T
  have hAM : MeasurableSet (A y xRef z T) :=
    (measurableSet_Ioi.preimage hUM).inter (measurableSet_Iic.preimage hUM)
  let D : Measure ℝ := (volume.restrict (Set.Ioc 0 (T : ℝ))).withDensity
    (fun s => ENNReal.ofReal (l s * Real.exp (-(∫ u in (0 : ℝ)..s, l u))))
  have hρD : ρ y xRef z T = D := by
    apply withDensity_congr_ae
    filter_upwards [ae_restrict_mem measurableSet_Ioc] with s hs
    simp only [d, Λ, Real.coe_toNNReal s hs.1.le, l]
  have hmap : (P.restrict (A y xRef z T)).map (F y xRef z) = ρ y xRef z T := by
    apply Measure.ext_of_Iic
    intro a
    by_cases ha : 0 ≤ a
    · rw [finite_wait_real_cdf P (U y xRef z) hUM (Λ y xRef z)
        (hΛbasic y xRef z).1 hsurv T a ha, hρD]
      rw [first_density_measure_Iic l hl hn (T : ℝ) a T.coe_nonneg ha]
      congr 2
      simp only [Λ, l, NNReal.coe_min, Real.coe_toNNReal a ha]
    · have hneg : a < 0 := lt_of_not_ge ha
      have hpre : (F y xRef z) ⁻¹' Set.Iic a = ∅ := by
        apply Set.eq_empty_iff_forall_notMem.mpr
        intro sample hs
        exact (not_le_of_gt hneg) (le_trans (NNReal.coe_nonneg _) hs)
      have hint : Set.Iic a ∩ Set.Ioc (0 : ℝ) (T : ℝ) = ∅ := by
        apply Set.eq_empty_iff_forall_notMem.mpr
        intro s hs
        exact (not_lt_of_ge hs.2.1.le) (lt_of_le_of_lt hs.1 hneg)
      rw [Measure.map_apply hFM measurableSet_Iic, hpre]
      rw [hρD, withDensity_apply _ measurableSet_Iic,
        Measure.restrict_restrict measurableSet_Iic, hint]
      simp
  letI : IsFiniteMeasure (ρ y xRef z T) := by rw [← hmap]; infer_instance
  have hmarked : (P.restrict (A y xRef z T)).map
      (fun sample => J y xRef z (F y xRef z sample)) = (ρ y xRef z T).map (J y xRef z) := by
    rw [← hmap, Measure.map_map hJM hFM]
    rfl
  have hmass : (ρ y xRef z T) Set.univ =
      ENNReal.ofReal (1 - Real.exp (-Λ y xRef z T)) := by
    rw [hρD]
    exact first_density_measure_mass l hl hn (T : ℝ) T.coe_nonneg
  have hmassnn : 0 ≤ 1 - Real.exp (-Λ y xRef z T) := by
    exact sub_nonneg.mpr (Real.exp_le_one_iff.mpr (neg_nonpos.mpr (hΛbasic y xRef z).2.1 T))
  have hmassreal : (ρ y xRef z T).real Set.univ =
      1 - Real.exp (-Λ y xRef z T) := by
    rw [measureReal_def, hmass, ENNReal.toReal_ofReal hmassnn]
  have hmassle : (ρ y xRef z T) Set.univ ≤ 1 := by
    rw [hmass]
    exact (ENNReal.ofReal_le_one).mpr (sub_le_self _ (Real.exp_pos _).le)
  refine ⟨hAM, hmap, hmarked, inferInstance, hmassreal, hmassle, ?_⟩
  intro h hh M hM hbound
  have hIntMark : Integrable h ((ρ y xRef z T).map (J y xRef z)) :=
    Integrable.of_bound hh.aestronglyMeasurable M
      (Filter.Eventually.of_forall fun a => by simpa only [Real.norm_eq_abs] using hbound a)
  have hIntP : Integrable (fun sample => h (J y xRef z (F y xRef z sample)))
      (P.restrict (A y xRef z T)) :=
    Integrable.of_bound ((hh.comp hJM).comp hFM).aestronglyMeasurable M
      (Filter.Eventually.of_forall fun sample => by
        simpa only [Real.norm_eq_abs] using hbound (J y xRef z (F y xRef z sample)))
  have hIntρ : Integrable (fun s => h (J y xRef z s)) (ρ y xRef z T) :=
    Integrable.of_bound (hh.comp hJM).aestronglyMeasurable M
      (Filter.Eventually.of_forall fun s => by
        simpa only [Real.norm_eq_abs] using hbound (J y xRef z s))
  have hWeightM : Measurable (fun s => ENNReal.ofReal (d y xRef z s)) :=
    hdC.measurable.ennreal_ofReal
  have hWeightTop : ∀ᵐ s ∂volume.restrict (Set.Ioc 0 (T : ℝ)),
      ENNReal.ofReal (d y xRef z s) < ⊤ :=
    Filter.Eventually.of_forall fun _ => ENNReal.ofReal_lt_top
  have hIntWeighted : Integrable (fun s => h (J y xRef z s) * d y xRef z s)
      (volume.restrict (Set.Ioc 0 (T : ℝ))) := by
    have hc := (integrable_withDensity_iff_integrable_smul' hWeightM hWeightTop).mp hIntρ
    simpa only [ENNReal.toReal_ofReal (hdn _), smul_eq_mul, mul_comm] using hc
  refine ⟨hIntMark, hIntP, hIntWeighted, ?_⟩
  calc
    (∫ sample, h (J y xRef z (F y xRef z sample)) ∂P.restrict (A y xRef z T)) =
        ∫ a, h a ∂((ρ y xRef z T).map (J y xRef z)) := by
      rw [← hmarked]
      exact (integral_map (hJM.comp hFM).aemeasurable hh.aestronglyMeasurable).symm
    _ = ∫ s, h (J y xRef z s) ∂ρ y xRef z T :=
      integral_map hJM.aemeasurable hh.aestronglyMeasurable
    _ = ∫ s, h (J y xRef z s) * d y xRef z s ∂volume.restrict (Set.Ioc 0 (T : ℝ)) := by
      rw [integral_withDensity_eq_integral_toReal_smul hWeightM hWeightTop]
      simp only [ENNReal.toReal_ofReal (hdn _), smul_eq_mul, mul_comm]
'''
anchor='\nset_option maxHeartbeats 1000000 in\ntheorem actual_finite_first_event_law\n'+header+' :\n    actual_finite_first_event_law_statement hα hαβ hV hH hη hβη := by\n'+definitions+'  change\n'+conclusion+proof+'\n'
s=s.replace('\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw',anchor+'\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw')
M.write_text(s,encoding='utf-8',newline='\n')
print('full anchor implementation written; compile pending')
