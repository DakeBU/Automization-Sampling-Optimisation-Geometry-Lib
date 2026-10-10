import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedTestContinuity
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.DominatedConvergence

/-! Actual PBPS bounded-test outer square-integral continuity.
PBPS arXiv2609.06905v1 AppendixA.1 Ex22 bounded-test outer square-integral ingredient.
All six original analytic conditions and the entire actual83 phase contract remain.
Exact conditional Gibbs x Gaussian probability normalization, state measurability,
square integrability, explicit4M2 domination and the outer zero-time limit are outputs.
The source uses C_c; C_b with an explicit global bound is an attributed ASTIS extension.
All-L2 AE operator/invariance/Jensen/contraction/density/Markov/main/cost remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false

private def actual_outer_bounded_l2_continuity_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop :=
    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun sample k => Real.toNNReal (sample k)
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
      (c y xRef + Real.cos t • (z.1 - c y xRef) +
          (Real.sqrt η * Real.sin t) • z.2,
       (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
    let rate : E → (E × E) → ℝ := fun xRef z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V xRef))
    let Λ : E → E → (E × E) → ℝ≥0 → ℝ := fun y xRef z t =>
      ∫ s in (0 : ℝ)..(t : ℝ), rate xRef (Φ y xRef s z)
    let τ : E → E → (E × E) → ℝ≥0 → WithTop ℝ≥0 := fun y xRef z e =>
      MeasureTheory.hittingAfter
        (fun t : ℝ≥0 => fun a : (E × E) × (E × E) × ℝ≥0 =>
          Λ a.1.1 a.1.2 a.2.1 t - (a.2.2 : ℝ))
        (Set.Ici (0 : ℝ)) 0 ((y, xRef), z, e)
    let next : E → E → ℝ≥0 → ((ℝ≥0 × (E × E)) ⊕ Unit) →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef e r =>
      match r with
      | Sum.inr _ => Sum.inr ()
      | Sum.inl a =>
        if τ y xRef a.2 e = ⊤ then Sum.inr () else
          Sum.inl (a.1 + (τ y xRef a.2 e).untopD 0,
            S xRef (Φ y xRef (((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ) a.2))
    let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
      Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
    let eventTime : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ e n => (record y xRef z₀ e n).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) →
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) →
          record y xRef z₀ (ε sample) n = Sum.inl a →
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ sample : ℕ → ℝ, ∀ t : ℝ≥0,
        (¬ ∃ n : ℕ, eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1)) →
          Z y xRef z₀ t sample = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ sample ∂P,
        (∀ t : ℝ≥0, ∃ n : ℕ, ∃ a : ℝ≥0 × (E × E),
          eventTime y xRef z₀ (ε sample) n ≤ (t : WithTop ℝ≥0) ∧
          (t : WithTop ℝ≥0) < eventTime y xRef z₀ (ε sample) (n + 1) ∧
          record y xRef z₀ (ε sample) n = Sum.inl a ∧ a.1 ≤ t ∧
          ((t - a.1 : ℝ≥0) : WithTop ℝ≥0) < τ y xRef a.2 (ε sample n) ∧
          Z y xRef z₀ t sample = Φ y xRef ((t - a.1 : ℝ≥0) : ℝ) a.2) ∧
        Z y xRef z₀ 0 sample = z₀)
 ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        (∀ t : ℝ≥0,
          MeasurableSet {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ∧
          P.real {sample : ℕ → ℝ |
            Z y xRef z₀ t sample ≠ Φ y xRef (t : ℝ) z₀} ≤
              1 - Real.exp (-Λ y xRef z₀ t)) ∧
        (∀ δ : ℝ, 0 < δ →
          (∀ t : ℝ≥0, MeasurableSet {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) ∧
          Tendsto (fun t : ℝ≥0 => P.real {sample : ℕ → ℝ |
            δ ≤ ‖Z y xRef z₀ t sample - z₀‖}) (𝓝 0) (𝓝 0)))

 ∧
      (∀ y xRef : E, ∀ z₀ : E × E,
        ∀ f : (E × E) → ℝ, Continuous f →
        ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
          (∀ t : ℝ≥0,
            Measurable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) ∧
            Integrable (fun sample : ℕ → ℝ => f (Z y xRef z₀ t sample)) P ∧
            |(∫ sample, f (Z y xRef z₀ t sample) ∂P) -
                f (Φ y xRef (t : ℝ) z₀)| ≤
              2 * M * (1 - Real.exp (-Λ y xRef z₀ t))) ∧
          Tendsto (fun t : ℝ≥0 => ∫ sample, f (Z y xRef z₀ t sample) ∂P)
            (𝓝 0) (𝓝 (f z₀)))


 ∧
      (let q : E → Measure E := fun y =>
         (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
       let ν : E → Measure (E × E) := fun y => (q y).prod (stdGaussian E)
       (∀ y : E, IsProbabilityMeasure (q y) ∧ IsProbabilityMeasure (ν y)) ∧
       (∀ y xRef : E, ∀ f : (E × E) → ℝ, Continuous f →
         ∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →
           let A : ℝ≥0 → (E × E) → ℝ := fun t z₀ =>
             ∫ sample, f (Z y xRef z₀ t sample) ∂P
           (∀ t : ℝ≥0, Measurable (A t) ∧
             Integrable (fun z₀ : E × E => (A t z₀ - f z₀) ^ 2) (ν y) ∧
             (∀ z₀ : E × E, (A t z₀ - f z₀) ^ 2 ≤ 4 * M ^ 2)) ∧
           Tendsto (fun t : ℝ≥0 =>
             ∫ z₀, (A t z₀ - f z₀) ^ 2 ∂(ν y)) (𝓝 0) (𝓝 0)))


set_option maxHeartbeats 1600000 in
/-- For the actual PBPS phase, bounded continuous tests have a measurable clock expectation
whose squared difference from the initial test tends to zero under the exact conditional
Gibbs-times-Gaussian initial law. The C_b class is an explicit ASTIS extension of the source
C_c ingredient in arXiv2609.06905v1 Appendix A.1 Ex22; this is not the all-L2 operator result. -/
theorem actual_outer_bounded_l2_continuity
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_outer_bounded_l2_continuity_statement hα hαβ hV hH hη hβη := by
  classical
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let q : E → Measure E := fun y =>
    (volume : Measure E).tilted (fun x => -V x - ‖x - y‖ ^ 2 / (2 * η))
  let ν : E → Measure (E × E) := fun y => (q y).prod (stdGaussian E)
  obtain ⟨Z, hZM, hcovered, hfallback, hAE, hshort, htest⟩ :=
    ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity
      hα hαβ hV hH hη hβη
  have hZV := (GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x v => (hH x v).1) hη).1
  have hi : Integrable (fun x : E => Real.exp (-V x)) (volume : Measure E) :=
    Integrable.of_integral_ne_zero hZV.ne'
  let μ : Measure E := (volume : Measure E).tilted (fun x => -V x)
  letI : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hi
  obtain ⟨R, hR, hRy, _⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  letI : IsMarkovKernel R := hR
  have hRq (y : E) : R y = q y := by
    rw [hRy y, show μ = (volume : Measure E).tilted (fun x => -V x) from rfl,
      tilted_tilted hi]
    congr 1
    funext z
    dsimp only [Pi.add_apply]
    ring
  have hqprob (y : E) : IsProbabilityMeasure (q y) := by
    rw [← hRq y]
    infer_instance
  have hνprob (y : E) : IsProbabilityMeasure (ν y) := by
    letI := hqprob y
    dsimp only [ν]
    infer_instance
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  refine ⟨Z, hZM, hcovered, hfallback, hAE, hshort, htest, ?_⟩
  refine ⟨fun y => ⟨hqprob y, hνprob y⟩, ?_⟩
  intro y xRef f hf M hM hbound
  letI := hνprob y
  let A : ℝ≥0 → (E × E) → ℝ := fun t z₀ => ∫ sample, f (Z y xRef z₀ t sample) ∂P
  have hAM (t : ℝ≥0) : Measurable (A t) := by
    have hargs : Measurable (fun a : (E × E) × (ℕ → ℝ) =>
        (((y, xRef), a.1), t, a.2)) :=
      (measurable_const.prodMk measurable_fst).prodMk (measurable_const.prodMk measurable_snd)
    exact ((hf.measurable.comp (hZM.comp hargs)).stronglyMeasurable.integral_prod_right').measurable
  have hAbound (t : ℝ≥0) (z₀ : E × E) : |A t z₀| ≤ M := by
    have hb : ∀ᵐ sample ∂P, ‖f (Z y xRef z₀ t sample)‖ ≤ M :=
      Filter.Eventually.of_forall fun sample => by
        simpa only [Real.norm_eq_abs] using hbound (Z y xRef z₀ t sample)
    simpa only [A, Real.norm_eq_abs, probReal_univ, mul_one] using
      norm_integral_le_of_norm_le_const hb
  have hsquare (t : ℝ≥0) (z₀ : E × E) : (A t z₀ - f z₀) ^ 2 ≤ 4 * M ^ 2 := by
    have ha := (abs_le.mp (hAbound t z₀))
    have hb := (abs_le.mp (hbound z₀))
    nlinarith [sq_nonneg (A t z₀ - f z₀ - 2 * M),
      mul_nonneg (show 0 ≤ 2 * M - (A t z₀ - f z₀) by linarith)
        (show 0 ≤ 2 * M + (A t z₀ - f z₀) by linarith)]
  have hsM (t : ℝ≥0) : Measurable (fun z₀ : E × E => (A t z₀ - f z₀) ^ 2) :=
    ((hAM t).sub hf.measurable).pow_const 2
  have hsi (t : ℝ≥0) : Integrable (fun z₀ : E × E => (A t z₀ - f z₀) ^ 2) (ν y) := by
    apply Integrable.of_bound (hsM t).aestronglyMeasurable (4 * M ^ 2)
    exact Filter.Eventually.of_forall fun z₀ => by
      simpa only [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg (A t z₀ - f z₀))] using hsquare t z₀
  refine ⟨fun t => ⟨hAM t, hsi t, hsquare t⟩, ?_⟩
  have hlimit (z₀ : E × E) : Tendsto (fun t : ℝ≥0 => (A t z₀ - f z₀) ^ 2)
      (𝓝 0) (𝓝 0) := by
    have ht : Tendsto (fun t : ℝ≥0 => A t z₀) (𝓝 0) (𝓝 (f z₀)) :=
      (htest y xRef z₀ f hf M hM hbound).2
    have hc : Tendsto (fun _ : ℝ≥0 => f z₀) (𝓝 0) (𝓝 (f z₀)) := tendsto_const_nhds
    simpa only [sub_self, zero_pow (by decide : 2 ≠ 0)] using
      (ht.sub hc).pow 2
  have hDCT := tendsto_integral_filter_of_dominated_convergence (μ := ν y)
    (F := fun t : ℝ≥0 => fun z₀ : E × E => (A t z₀ - f z₀) ^ 2)
    (f := fun _ : E × E => (0 : ℝ)) (fun _ : E × E => 4 * M ^ 2)
    (Filter.Eventually.of_forall fun t => (hsM t).aestronglyMeasurable)
    (Filter.Eventually.of_forall fun t => Filter.Eventually.of_forall fun z₀ => by
      simpa only [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg (A t z₀ - f z₀))] using hsquare t z₀)
    (integrable_const _) (Filter.Eventually.of_forall hlimit)
  simpa only [integral_zero] using hDCT

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity
#check AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let stem := "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity"
  let mut todo := #[`AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity]
  let mut seen : Array Name := #[]
  let mut externalDeps : Array Name := #[]
  while !todo.isEmpty do
    let name := todo.back!
    todo := todo.pop
    if !seen.contains name then
      seen := seen.push name
      logInfo m!"LOCAL_PROOF_CONSTANT {name}"
      let some ci := env.find? name | throwError "Missing local proof constant"
      let some value := ci.value? true | throwError "Missing local proof value"
      for dep in value.getUsedConstants do
        if dep.toString.startsWith stem then
          todo := todo.push dep
        else if dep.toString.startsWith "AutoSamplingTheory." && !externalDeps.contains dep then
          externalDeps := externalDeps.push dep
          logInfo m!"EXTERNAL_ASTIS_DEPENDENCY {dep}"
  logInfo m!"LOCAL_PROOF_CONSTANT_COUNT {seen.size}"
  let mut projectTodo := externalDeps
  let mut projectSeen : Array Name := #[]
  while !projectTodo.isEmpty do
    let name := projectTodo.back!
    projectTodo := projectTodo.pop
    if !projectSeen.contains name then
      projectSeen := projectSeen.push name
      logInfo m!"TRANSITIVE_ASTIS_CONSTANT {name}"
      if let some ci := env.find? name then
        if let some value := ci.value? true then
          for dep in value.getUsedConstants do
            if dep.toString.startsWith "AutoSamplingTheory." then
              logInfo m!"TRANSITIVE_ASTIS_EDGE {name} -> {dep}"
              projectTodo := projectTodo.push dep
  logInfo m!"TRANSITIVE_ASTIS_CONSTANT_COUNT {projectSeen.size}"
