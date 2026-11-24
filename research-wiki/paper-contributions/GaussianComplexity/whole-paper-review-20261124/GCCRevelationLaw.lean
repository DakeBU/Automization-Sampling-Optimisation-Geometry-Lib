import GCCHistoryLaw

/-! Haar revelation given an arbitrary history, in orthonormal coordinates on its
domain and range. The residual group in dimension zero is treated explicitly. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

/-- Domain and range frames determine coordinates for a forward or inverse revelation. -/
def reveal : {m : ℕ} → Bool → S (m+1) → O (m+1) → S (m+1) × O m
  | 0, back, u, W => (rotate (if back then W⁻¹ else W) u,1)
  | n+1, back, u, W => selectedHaarStep (sectionQ n) (sectionQ_col n) back u W

theorem reveal_direction {m : ℕ} (b : Bool) (u : S (m+1)) (W : O (m+1)) :
    (reveal b u W).1 = rotate (if b then W⁻¹ else W) u := by
  cases m <;> cases b <;> rfl

theorem measurable_reveal {m : ℕ} (b : Bool) :
    Measurable (fun p : S (m+1) × O (m+1) => reveal b p.1 p.2) := by
  cases m with
  | zero =>
    cases b
    · exact (continuous_rotate.measurable.comp (measurable_snd.prodMk measurable_fst)).prodMk measurable_const
    · exact (continuous_rotate.measurable.comp (measurable_snd.inv.prodMk measurable_fst)).prodMk measurable_const
  | succ n => exact measurable_selectedHaarStep _ (sectionQ_meas n) (sectionQ_col n) b

theorem orthogonalHaar_zero : orthogonalHaar 0 = Measure.dirac 1 := by
  let : Subsingleton (O 0) := ⟨fun A B => Subtype.ext (funext fun i => i.elim0)⟩
  let := (orthogonalHaar_spec 0).1
  ext s hs
  rcases s.eq_empty_or_nonempty with rfl | hn
  · simp
  · obtain ⟨w,hw⟩ := hn
    have hall : s = Set.univ := Set.eq_univ_iff_forall.mpr (fun v => (Subsingleton.elim w v) ▸ hw)
    simp [hall]

theorem reveal_law {m : ℕ} (b : Bool) (u : S (m+1)) :
    MeasurePreserving (reveal b u) (orthogonalHaar (m+1))
      ((sphereProbability (m+1)).prod (orthogonalHaar m)) := by
  refine ⟨(measurable_reveal b).of_uncurry_left,?_⟩
  cases m with
  | zero =>
    let := isProbabilityMeasure_sphereProbability (0+1)
    have hr : MeasurePreserving (fun W : O 1 => rotate (if b then W⁻¹ else W) u)
        (orthogonalHaar 1) (sphereProbability 1) := by
      have hf : MeasurePreserving (fun W : O 1 => rotate W u) (orthogonalHaar 1)
          (sphereProbability 1) :=
        ⟨(continuous_rotate.comp (continuous_id.prodMk continuous_const)).measurable,haar_rotate_fixed u⟩
      cases b
      · exact hf
      · have hi : MeasurePreserving (Inv.inv : O 1 → O 1) (orthogonalHaar 1) (orthogonalHaar 1) := by
          refine ⟨measurable_inv,?_⟩
          rw [haar_as_components, Measure.map_smul, Measure.map_add _ _ measurable_inv,
            componentHaar_map_inv, componentHaar_map_inv]
        exact hf.comp hi
    rw [orthogonalHaar_zero,Measure.prod_dirac,← hr.map_eq,Measure.map_map measurable_prodMk_right hr.measurable]
    rfl
  | succ n => exact full_haar_step_law _ (sectionQ_meas n) (sectionQ_col n) (sectionQ_det n) b u

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {m : ℕ}

/-- C.1 for arbitrary history and underlying experiment. Given the history the
new direction is uniform. Given both the old history and this direction the
restriction to the remaining perpendicular spaces is Haar. -/
theorem conditional_haar_revelation {μ : Measure Ω} [IsFiniteMeasure μ]
    {h : Ω → H} {W : Ω → O (m+1)} (hp : LawGiven μ h W (orthogonalHaar (m+1)))
    (b : Bool) (u : H → S (m+1)) (hu : Measurable u) :
    let p := fun ω => reveal b (u (h ω)) (W ω)
    LawGiven μ h (fun ω => (p ω).1) (sphereProbability (m+1)) ∧
      LawGiven μ (fun ω => (h ω,(p ω).1)) (fun ω => (p ω).2) (orthogonalHaar m) := by
  let := (orthogonalHaar_spec (m+1)).1
  let := (orthogonalHaar_spec m).1
  let := isProbabilityMeasure_sphereProbability (m+1)
  let ρ := μ.map h
  let σ := sphereProbability (m+1)
  let η := orthogonalHaar m
  let t := fun p : H × O (m+1) => reveal b (u p.1) p.2
  have ht : Measurable t := (measurable_reveal b).comp ((hu.comp measurable_fst).prodMk measurable_snd)
  have hj := pairLaw_of_constant_continuation ρ (Kernel.const H (orthogonalHaar (m+1)))
    ρ (σ.prod η) id t (MeasurePreserving.id ρ) ht (ae_of_all _ fun a => (reveal_law b (u a)).map_eq)
  rw [Measure.compProd_const] at hj
  have hall := (measurePreserving_prodAssoc ρ σ η).symm.comp (hj.comp hp)
  constructor
  · exact LawGiven.of_joint ((measurePreserving_fst (μ := ρ.prod σ) (ν := η)).comp hall)
  · exact LawGiven.of_joint hall

#print axioms conditional_haar_revelation
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
