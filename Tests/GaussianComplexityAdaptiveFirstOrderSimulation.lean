import AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
open AutoSamplingTheory.TechnicalLemmas.Probability.AdaptiveOracleSimulation
set_option autoImplicit false
universe uS uΩ

/-!
Actual two-direction seeded adaptive simulation for the literal fixed-spectrum
precision family. Every seed retains its terminal state, some-output or none
exhaustion, and actual query count; both full joint laws and ordinary expected
query costs are preserved. The genuine source gradient is supplied internally
by the canonical producer. No source-class representation, successful-sampling,
Haar-joint law, TV accuracy, approximate oracle or main lower bound is asserted.
-/
namespace AutoSamplingTheory.Tests.GaussianComplexityAdaptiveFirstOrderSimulation

set_option backward.isDefEq.respectTransparency false in
private theorem actual_fixed_spectrum_first_order_matvec_joint_laws_and_costs :
  ∀ {d : ℕ}, 2 ≤ d →
      ∀ {κ : ℝ}, 2 ≤ κ →
      letI : MeasurableSpace (EuclideanSpace ℝ (Fin d)) := borel _
      letI : MeasurableSpace (Option (EuclideanSpace ℝ (Fin d))) := MeasurableSpace.comap
        (fun x : Option (EuclideanSpace ℝ (Fin d)) =>
          x.elim (Sum.inl () : Unit ⊕ EuclideanSpace ℝ (Fin d)) Sum.inr) inferInstance
      ∀ {S : Type uS} {Ω : Type uΩ} [MeasurableSpace S] [MeasurableSpace Ω]
        (μ : Measure Ω) [IsProbabilityMeasure μ]
        (next : S → Sum (EuclideanSpace ℝ (Fin d)) (EuclideanSpace ℝ (Fin d)))
        (updateFO : S → EuclideanSpace ℝ (Fin d) →
          (ℝ × EuclideanSpace ℝ (Fin d)) → S)
        (updateMV : S → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) → S)
        (initial : Ω → S),
        Measurable next →
        Measurable (fun p : S × EuclideanSpace ℝ (Fin d) ×
          (ℝ × EuclideanSpace ℝ (Fin d)) => updateFO p.1 p.2.1 p.2.2) →
        Measurable (fun p : S × EuclideanSpace ℝ (Fin d) ×
          EuclideanSpace ℝ (Fin d) => updateMV p.1 p.2.1 p.2.2) →
        Measurable initial →
        ∀ (fuel : ℕ) (O : Matrix.orthogonalGroup (Fin d) ℝ),
          let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
          let A : Matrix (Fin d) (Fin d) ℝ :=
            (O : Matrix (Fin d) (Fin d) ℝ) *
            Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
            (O : Matrix (Fin d) (Fin d) ℝ).transpose
          let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
            (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
          let mv : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
            WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
          let fo := fun x => (f x, gradient f x)
          let foRun := fun ω => run next updateFO fo fuel (initial ω)
          let foViaMV := fun ω => run next
            (fun s x y => updateFO s x (inner ℝ x y / 2, y)) mv fuel (initial ω)
          let mvRun := fun ω => run next updateMV mv fuel (initial ω)
          let mvViaFO := fun ω => run next
            (fun s x (y : ℝ × EuclideanSpace ℝ (Fin d)) => updateMV s x y.2)
            fo fuel (initial ω)
          Measurable foViaMV ∧ Measurable foRun ∧
          (∀ ω, foViaMV ω = foRun ω ∧ (foViaMV ω).2 ≤ fuel) ∧
          μ.map foViaMV = μ.map foRun ∧ IsProbabilityMeasure (μ.map foViaMV) ∧
          Integrable (fun ω => ((foViaMV ω).2 : ℝ)) μ ∧
          (∫ ω, ((foViaMV ω).2 : ℝ) ∂μ) = (∫ ω, ((foRun ω).2 : ℝ) ∂μ) ∧
          (∫ ω, ((foViaMV ω).2 : ℝ) ∂μ) ≤ (fuel : ℝ) ∧
          Measurable mvViaFO ∧ Measurable mvRun ∧
          (∀ ω, mvViaFO ω = mvRun ω ∧ (mvViaFO ω).2 ≤ fuel) ∧
          μ.map mvViaFO = μ.map mvRun ∧ IsProbabilityMeasure (μ.map mvViaFO) ∧
          Integrable (fun ω => ((mvViaFO ω).2 : ℝ)) μ ∧
          (∫ ω, ((mvViaFO ω).2 : ℝ) ∂μ) = (∫ ω, ((mvRun ω).2 : ℝ) ∂μ) ∧
          (∫ ω, ((mvViaFO ω).2 : ℝ) ∂μ) ≤ (fuel : ℝ) := by
  intro d hd κ hκ
  let E := EuclideanSpace ℝ (Fin d)
  let : MeasurableSpace E := borel E
  let : BorelSpace E := ⟨rfl⟩
  let : MeasurableSpace (Option E) := MeasurableSpace.comap
    (fun x : Option E => x.elim (Sum.inl () : Unit ⊕ E) Sum.inr) inferInstance
  dsimp only
  intro S Ω mS mΩ μ hμ next updateFO updateMV initial hnext hupdateFO hupdateMV
    hinitial fuel O
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
    (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : E → ℝ := fun x => (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let mv : E → E := fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  let fo : E → ℝ × E := fun x => (f x, gradient f x)
  let H : E →L[ℝ] E := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A
  have hmv : Measurable mv := by
    change Measurable H
    exact H.continuous.measurable
  have hactual (x : E) : fo x = (inner ℝ x (mv x) / 2, mv x) :=
    (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
      hd hκ O x).2
  have hdecoder : Measurable (fun p : E × E => (inner ℝ p.1 p.2 / 2, p.2)) :=
    (show Continuous (fun p : E × E => (inner ℝ p.1 p.2 / 2, p.2)) by fun_prop).measurable
  have hfo : Measurable fo := by
    have heq : fo = fun x => (inner ℝ x (mv x) / 2, mv x) := funext hactual
    have hpair : Measurable (fun x : E => (x, mv x)) := measurable_id.prodMk hmv
    have hcomp := hdecoder.comp hpair
    exact heq.symm ▸ hcomp
  have hfwd := measurable_simulation_joint_law_and_cost
    (S := S) (Q := E) (A := E) (B := ℝ × E) (X := E) (Ω := Ω)
    μ next updateFO mv fo
    (fun x y => (inner ℝ x y / 2, y)) initial hnext hupdateFO hmv hdecoder
    hinitial (fun x => (hactual x).symm) fuel
  have hprojection : Measurable (fun p : E × (ℝ × E) => p.2.2) := measurable_snd.snd
  have hrev := measurable_simulation_joint_law_and_cost
    (S := S) (Q := E) (A := ℝ × E) (B := E) (X := E) (Ω := Ω)
    μ next updateMV fo mv
    (fun _ y => y.2) initial hnext hupdateMV hfo hprojection hinitial
    (fun x => congrArg Prod.snd (hactual x)) fuel
  rcases hfwd with ⟨hf1, hf2, hf3, hf4, hf5, hf6, hf7, hf8⟩
  rcases hrev with ⟨hr1, hr2, hr3, hr4, hr5, hr6, hr7, hr8⟩
  exact ⟨hf1, hf2, hf3, hf4, hf5, hf6, hf7, hf8,
    hr1, hr2, hr3, hr4, hr5, hr6, hr7, hr8⟩

end AutoSamplingTheory.Tests.GaussianComplexityAdaptiveFirstOrderSimulation
