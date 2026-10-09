import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardInputLaw
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardCenterMoment
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.RealizedProximalWork

/-! Algorithm 3.1 / D.4: both actual query layers under the full phase law.
The incoming state L2 budget is explicit. Neither run-wide D.7, the source
quadrature adapter, whole-phase direct-query execution count nor D.8 is closed.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseWork

private theorem first_input_projection_preserving
    {E ι : Type*} [MeasurableSpace E] [Fintype ι]
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (g : Measure E) [IsProbabilityMeasure g] :
    let gi := Measure.pi (fun _ : ι => g)
    MeasurePreserving
      (fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
        ((w.1, w.2.1.1), w.2.2.1))
      (ν.prod ((g.prod g).prod (gi.prod gi))) ((ν.prod g).prod gi) := by
  dsimp only
  let gi := Measure.pi (fun _ : ι => g)
  have hf : MeasurePreserving Prod.fst (g.prod g) g := measurePreserving_fst
  have ha : MeasurePreserving Prod.fst (gi.prod gi) gi := measurePreserving_fst
  have hn := hf.prod ha
  have hs := (MeasurePreserving.id ν).prod hn
  have hback := MeasurePreserving.symm MeasurableEquiv.prodAssoc
    (measurePreserving_prodAssoc ν g gi)
  exact hback.comp hs

variable {E ι : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [Fintype ι]

/-- The same q/N supplies the full Gaussian phase kernel, both actual queried
gradient moments and both actual proximal query-count expectations. The only
moment hypothesis is on the incoming state, before the first half-refresh. -/
theorem implemented_phase_query_moments_and_work {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (xstar : E) (hstar : gradient V xstar = 0)
    {h M S : ℝ} (hh : 0 ≤ h) (hM : 0 ≤ M) (hS : 0 ≤ S)
    (hstateI : Integrable (fun s : E × E => ‖s.1-xstar‖^2 + ‖s.2‖^2) ν)
    (hstate : (∫ s : E × E, ‖s.1-xstar‖^2 + ‖s.2‖^2 ∂ν) ≤ M)
    (t : ι → ℝ) (ht : ∀ i, |t i| ≤ 1) (omega : ι → ι → ℝ)
    (hrow : ∀ i, (∑ j, |omega i j|) ≤ S)
    (positionWeight momentumWeight : ι → ℝ) :
    let a := Real.exp (-h/2)
    let sigma := Real.sqrt (1-Real.exp (-h))
    let gi := Measure.pi (fun _ : ι => stdGaussian E)
    let γ := ((stdGaussian E).prod (stdGaussian E)).prod (gi.prod gi)
    let μ := ν.prod γ
    let MR := M + (1-Real.exp (-h)) * (Module.finrank ℝ E : ℝ)
    let B := 6*MR + 3*eps^2 + 3*eta*(Module.finrank ℝ E : ℝ)
    let C := 2 + (1+Real.log ((1-c)⁻¹))/(-Real.log c)
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y-p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some (q y,N y+1)) ∧
      let P0 := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
        a • w.1.2 + sigma • w.2.1.1
      let Y0 := fun i w => w.1.1 + t i • P0 w
      let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • w.2.2.1 j)
      let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
      let Z1 := fun j w => gradient V (q (Y1 j w) + Real.sqrt eta • w.2.2.2 j)
      let Φ := fun w => (w.1.1 + h • P0 w - ∑ j, positionWeight j • Z1 j w,
        a • (P0 w - ∑ j, momentumWeight j • Z1 j w) + sigma • w.2.1.2)
      Measurable Φ ∧ ∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧
      (∀ s, K s = γ.map (fun z => Φ (s,z))) ∧
      (∀ i, Integrable (fun w => ‖gradient V (Y0 i w)‖^2) μ ∧
        (∫ w, ‖gradient V (Y0 i w)‖^2 ∂μ) ≤ 2*MR ∧
        Integrable (fun w => (N (Y0 i w) : ℝ)+1) μ ∧
        (∫ w, (N (Y0 i w) : ℝ)+1 ∂μ) ≤
          C*(1+Real.log (1+Real.sqrt (2*MR)/eps))) ∧
      (∀ i, Integrable (fun w => ‖gradient V (Y1 i w)‖^2) μ ∧
        (∫ w, ‖gradient V (Y1 i w)‖^2 ∂μ) ≤ 4*MR+2*S^2*B ∧
        Integrable (fun w => (N (Y1 i w) : ℝ)+1) μ ∧
        (∫ w, (N (Y1 i w) : ℝ)+1 ∂μ) ≤
          C*(1+Real.log (1+Real.sqrt (4*MR+2*S^2*B)/eps))) := by
  classical
  dsimp only
  let gi := Measure.pi (fun _ : ι => stdGaussian E)
  let γ := ((stdGaussian E).prod (stdGaussian E)).prod (gi.prod gi)
  let μ := ν.prod γ
  let μ0 := (ν.prod (stdGaussian E)).prod gi
  let proj := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
    ((w.1,w.2.1.1),w.2.2.1)
  have hproj : MeasurePreserving proj μ μ0 :=
    first_input_projection_preserving ν (stdGaussian E)
  obtain ⟨hMR,hX0,hP0,hsI0,hs0,hG0,hGI0,hGint0⟩ :=
    PicardInputLaw.partial_refresh_with_picard_innovations (ι := ι) ν xstar hh hM hstateI hstate
  let X := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) => w.1.1
  let P := fun w : (E × E) × ((E × E) × ((ι → E) × (ι → E))) =>
    Real.exp (-h/2) • w.1.2 + Real.sqrt (1-Real.exp (-h)) • w.2.1.1
  let G := fun (j : ι) (w : (E × E) × ((E × E) × ((ι → E) × (ι → E)))) =>
    w.2.2.1 j
  have hsI : Integrable (fun w => ‖X w-xstar‖^2 + ‖P w‖^2) μ :=
    hproj.integrable_comp_of_integrable hsI0
  have hs : (∫ w, ‖X w-xstar‖^2 + ‖P w‖^2 ∂μ) ≤
      M + (1-Real.exp (-h))*(Module.finrank ℝ E : ℝ) := by
    calc
      _ = ∫ u : ((E × E) × E) × (ι → E), ‖u.1.1.1-xstar‖^2 +
          ‖Real.exp (-h/2) • u.1.1.2 + Real.sqrt (1-Real.exp (-h)) • u.1.2‖^2 ∂μ0 := by
        rw [← hproj.map_eq, integral_map hproj.measurable.aemeasurable (by fun_prop)]
      _ ≤ _ := hs0
  have hGI (j) : Integrable (fun w => ‖G j w‖^2) μ :=
    hproj.integrable_comp_of_integrable (hGI0 j)
  have hGint (j) : (∫ w, ‖G j w‖^2 ∂μ) ≤ (Module.finrank ℝ E : ℝ) := by
    calc
      _ = ∫ u : ((E × E) × E) × (ι → E), ‖u.2 j‖^2 ∂μ0 := by
        rw [← hproj.map_eq, integral_map hproj.measurable.aemeasurable (by fun_prop)]
      _ ≤ _ := le_of_eq (hGint0 j)
  obtain ⟨p,q,N,hp,hq,hN,hall,hphase⟩ :=
    ImplementedPhaseKernel.implemented_phase_kernel hκ hV hH heta hec hc heps h hh
      t omega positionWeight momentumWeight
  obtain ⟨p',N',q',hp',hN',hq',hfix',hrun',hm0,hz0,hm1⟩ :=
    PicardCenterMoment.picard_center_gradient_moment hκ hV hH heta hec hc heps μ
      X P (by fun_prop) (by fun_prop) xstar hstar t ht G (fun _ => by fun_prop)
      omega hMR hS hsI hs hGI hGint hrow
  have hid (y) := ProximalExecutionIdentity.successful_query_unique
    (gradient V) eta eps y (hall y).2.2 (hrun' y).2
  have hqeq : q = q' := funext fun y => congrArg Prod.fst (hid y)
  have hNeq : N = N' := funext fun y => Nat.add_right_cancel (congrArg Prod.snd (hid y))
  subst q'
  subst N'
  obtain ⟨hvar,hΦ,K,hK,hKlaw⟩ := hphase
  have hg : Measurable (gradient V) := by
    unfold gradient
    exact ((InnerProductSpace.toDual ℝ E).symm.continuous.comp
      (hV.continuous_fderiv (by norm_num))).measurable
  have hC : 0 ≤ 2+(1+Real.log ((1-c)⁻¹))/(-Real.log c) := by
    have hcp := heta.trans_le hec
    have hd : 0 < 1-c := sub_pos.mpr hc
    have hi : 1 ≤ (1-c)⁻¹ := (one_le_inv₀ hd).mpr (by linarith)
    have hl := Real.log_nonneg hi
    have ha := neg_pos.mpr (Real.log_neg hcp hc)
    positivity
  refine ⟨p,q,N,hp,hq,hN,hall,hΦ,K,hK,hKlaw,?_,?_⟩
  · intro i
    obtain ⟨hcI,hcB⟩ := RealizedProximalWork.realized_proximal_expected_work μ
      hκ hV hH heta hec hc heps q N (fun y => (hall y).2.2)
      (fun w => X w+t i • P w) (by fun_prop) (hm0 i).1
    refine ⟨(hm0 i).1,(hm0 i).2,hcI,hcB.trans ?_⟩
    apply mul_le_mul_of_nonneg_left _ hC
    apply add_le_add_right
    apply Real.log_le_log (by positivity)
    gcongr
    exact (hm0 i).2
  · intro i
    obtain ⟨hcI,hcB⟩ := RealizedProximalWork.realized_proximal_expected_work μ
      hκ hV hH heta hec hc heps q N (fun y => (hall y).2.2)
      (fun w => X w+t i • P w - ∑ j, omega i j •
        gradient V (q (X w+t j • P w) + Real.sqrt eta • G j w))
      (by fun_prop) (hm1 i).1
    refine ⟨(hm1 i).1,(hm1 i).2,hcI,hcB.trans ?_⟩
    apply mul_le_mul_of_nonneg_left _ hC
    apply add_le_add_right
    apply Real.log_le_log (by positivity)
    gcongr
    exact (hm1 i).2

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseWork
