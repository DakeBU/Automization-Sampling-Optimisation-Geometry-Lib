import AutoSamplingTheory.TechnicalLemmas.Measure.CommonNoiseContraction

/-! # Nonlinear randomized-map transport contraction

Construct a genuine synchronous common-noise coupling, without assuming an
optimal plan or finite moments. The positive finite factor commutes with the
raw extended transport infimum. State and noise inhabit the same Borel space;
the actual SPHMC phase/noise and additive-noise consumers both satisfy this.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Measure.RandomizedMapTransport
open MeasureTheory
open scoped ENNReal
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [MeasurableSpace E]
  [BorelSpace E] [SecondCountableTopology E]

/-- Lift a measurable same-noise pointwise cost bound to actual randomized
output laws, for arbitrary probability inputs, including infinite costs. -/
theorem transportCost_randomized_map_le
    (Φ : E × E → E) (hΦ : Measurable Φ) (c : E × E → ℝ≥0∞) (hc : Measurable c)
    (A : ℝ≥0∞) (hA0 : A ≠ 0) (hAtop : A ≠ ⊤)
    (hcost : ∀ x y ζ, c (Φ (x,ζ),Φ (y,ζ)) ≤ A*c (x,y))
    (μ ν Γ : Measure E) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    [IsProbabilityMeasure Γ] :
    Transport.transportCost c ((μ.prod Γ).map Φ) ((ν.prod Γ).map Φ) ≤
      A * Transport.transportCost c μ ν := by
  classical
  have candidate (γ : Measure (E × E)) (hγ : Transport.IsCoupling γ μ ν) :
      Transport.transportCost c ((μ.prod Γ).map Φ) ((ν.prod Γ).map Φ) ≤
        A * ∫⁻ z, c z ∂γ := by
    letI : IsProbabilityMeasure γ := Transport.isProbabilityMeasure_of_isCoupling_left hγ
    let S : ((E × E) × E) → E × E := fun w => (Φ (w.1.1,w.2),Φ (w.1.2,w.2))
    have hS : Measurable S := hΦ.comp (by fun_prop) |>.prodMk (hΦ.comp (by fun_prop))
    let ρ := (γ.prod Γ).map S
    have hleft : (γ.prod Γ).map (fun w : ((E × E) × E) => (w.1.1,w.2)) = μ.prod Γ :=
      CommonNoiseContraction.map_pairLeft_prod_eq hγ
    have hright : (γ.prod Γ).map (fun w : ((E × E) × E) => (w.1.2,w.2)) = ν.prod Γ :=
      CommonNoiseContraction.map_pairRight_prod_eq hγ
    have hρ : Transport.IsCoupling ρ ((μ.prod Γ).map Φ) ((ν.prod Γ).map Φ) := by
      constructor
      · rw [Measure.fst, show ρ = (γ.prod Γ).map S from rfl,
          Measure.map_map measurable_fst hS]
        rw [← hleft, Measure.map_map hΦ (by fun_prop)]
        rfl
      · rw [Measure.snd, show ρ = (γ.prod Γ).map S from rfl,
          Measure.map_map measurable_snd hS]
        rw [← hright, Measure.map_map hΦ (by fun_prop)]
        rfl
    calc
      Transport.transportCost c ((μ.prod Γ).map Φ) ((ν.prod Γ).map Φ) ≤
          ∫⁻ z, c z ∂ρ := Transport.transportCost_le_lintegral_of_isCoupling _ _ _ _ hρ
      _ = ∫⁻ w, c (S w) ∂γ.prod Γ := lintegral_map hc hS
      _ ≤ ∫⁻ w : (E × E) × E, A*c w.1 ∂γ.prod Γ := by
        apply lintegral_mono
        intro w
        exact hcost _ _ _
      _ = A * ∫⁻ w : (E × E) × E, c w.1 ∂γ.prod Γ :=
        lintegral_const_mul _ (hc.comp measurable_fst)
      _ = A * ∫⁻ z, c z ∂γ := by
        rw [← lintegral_map hc measurable_fst, Measure.map_fst_prod, measure_univ, one_smul]
  conv_rhs => rw [Transport.transportCost_eq_sInf, sInf_eq_iInf,
    ENNReal.mul_iInf_of_ne hA0 hAtop]
  apply le_iInf
  intro r
  rw [ENNReal.mul_iInf_of_ne hA0 hAtop]
  apply le_iInf
  intro hrmem
  rcases hrmem with ⟨γ,hγ,hr⟩
  simpa only [hr] using candidate γ hγ
end
end AutoSamplingTheory.TechnicalLemmas.Measure.RandomizedMapTransport
