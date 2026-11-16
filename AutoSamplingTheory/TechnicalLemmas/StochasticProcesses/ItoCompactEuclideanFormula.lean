import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicHessian
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoActualTaylorRemainder
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CountableConvergenceInMeasure

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal Topology
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral ItoInitializedDrift ItoDyadicLinearTerm
  ItoDyadicHessian ItoActualTaylorRemainder CountableConvergenceInMeasure
open AutoSamplingTheory.TechnicalLemmas.Analysis.CompactTaylorRemainder

set_option maxHeartbeats 600000 in
/-- Itô's formula at the horizon for an actual finite-dimensional process
with compact state range, with its derivative integrands and genuine martingale. -/
theorem ito_formula_compact_euclidean_at_horizon
    {Ω I J : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → J → ProgressiveL2Integrand filtration μ T)
    (x : Ω → I → ℝ) (hx : ∀ i, StronglyMeasurable[filtration 0] (fun ω => x ω i))
    (b : I → ℝ≥0 → Ω → ℝ) (hb : ∀ i, IsStronglyProgressive filtration (b i))
    (hbi : ∀ i, ∀ᵐ ω ∂μ, Integrable (fun s => b i s ω) (TimeMeasure.upTo T))
    {K : Set (EuclideanSpace ℝ I)} (hK : IsCompact K) (fallback : K) (f : EuclideanSpace ℝ I → ℝ)
    (hf : ∀ x ∈ K, ContDiffAt ℝ 2 f x) :
    let A := fun (i : I) (t : ℝ≥0) (ω : Ω) => x ω i + prefixIntegralProcess (b i) t ω
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : J,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    let v := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => b i t ω)
    let σ := fun (j : J) (t : ℝ≥0) (ω : Ω) =>
      WithLp.toLp 2 (fun i : I => (η i j).process t ω)
    let H := fderiv ℝ (fderiv ℝ f)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K) →
    ∃ θ : (I × J) → ProgressiveL2Integrand filtration μ T,
      (∀ᵐ ω ∂μ, ∀ q t, (θ q).process t ω =
        fderiv ℝ f (X (min t T) ω) (EuclideanSpace.basisFun I ℝ q.1) *
          (η q.1 q.2).process t ω) ∧
      let M := fun (t : ℝ≥0) (ω : Ω) => ∑ q : I × J,
        itoIntegralProcess (θ q) hT ((coordinateFamily hB).isBrownian q.2) hUsual t ω
      Martingale M filtration μ ∧ (∀ ω, M 0 ω = 0) ∧
      (∀ᵐ ω ∂μ, f (X T ω) - f (X 0 ω) =
        (∫ s, fderiv ℝ f (X s ω) (v s ω) ∂(TimeMeasure.upTo T)) +
        (∫ s, (1 / 2 : ℝ) * (∑ j : J, H (X s ω) (σ j s ω) (σ j s ω))
          ∂(TimeMeasure.upTo T)) + M T ω) := by
  intro A X v σ H hRange
  have hf1 (y : EuclideanSpace ℝ I) (hy : y ∈ K) : ContDiffAt ℝ 1 f y :=
    (hf y hy).of_le (by decide)
  obtain ⟨θ, hθ, hM, h0, hLinear⟩ :=
    tendstoInMeasure_dyadic_linear_ito_term hB hT hUsual η x hx b hb hbi hK fallback f hf1 hRange
  let M (s : ℝ≥0) (ω : Ω) := ∑ q : I × J,
    itoIntegralProcess (θ q) hT ((coordinateFamily hB).isBrownian q.2) hUsual s ω
  refine ⟨θ, hθ, hM, h0, ?_⟩
  have hDrift (i : I) := initialized_drift_progressive_continuous_boundedVariation
    (fun ω => x ω i) (hx i) (b i) (hb i) (hbi i)
  have hAmeas (i : I) (s : ℝ≥0) (_ : s ≤ T) : AEStronglyMeasurable (A i s) μ :=
    (((hDrift i).1.stronglyAdapted s).mono (filtration.le s)).aestronglyMeasurable
  have hAc (i : I) : ∀ᵐ ω ∂μ, ContinuousOn (fun s => A i s ω) (Icc 0 T) ∧
      BoundedVariationOn (fun s => A i s ω) (Icc 0 T) := (hDrift i).2.2
  have hHessian := tendstoInMeasure_dyadic_half_hessian_increments hB hT hUsual η A
    hAmeas hAc hK fallback f hf hRange
  have hRemainder := tendstoInMeasure_dyadic_actual_ito_taylor_remainder hB hT hUsual η A
    hAmeas hAc hK fallback f hf hRange
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  let Δ (n : ℕ) (i : Fin (2 ^ n)) (ω : Ω) := X (t n i.succ) ω - X (t n i.castSucc) ω
  let L (n : ℕ) (ω : Ω) := ∑ i : Fin (2 ^ n), fderiv ℝ f (X (t n i.castSucc) ω) (Δ n i ω)
  let Q (n : ℕ) (ω : Ω) := ∑ i : Fin (2 ^ n),
    (1 / 2 : ℝ) * H (X (t n i.castSucc) ω) (Δ n i ω) (Δ n i ω)
  let R (n : ℕ) (ω : Ω) := ∑ i : Fin (2 ^ n), secondOrderRemainder f (X (t n i.castSucc) ω) (Δ n i ω)
  let D (ω : Ω) := ∫ s, fderiv ℝ f (X s ω) (v s ω) ∂(TimeMeasure.upTo T)
  let E (ω : Ω) := ∫ s, (1 / 2 : ℝ) * (∑ j : J, H (X s ω) (σ j s ω) (σ j s ω))
    ∂(TimeMeasure.upTo T)
  let F : Option Bool → ℕ → Ω → ℝ
    | none => L
    | some false => Q
    | some true => R
  let G : Option Bool → Ω → ℝ
    | none => fun ω => D ω + M T ω
    | some false => E
    | some true => fun _ => 0
  have hData (k : Option Bool) : TendstoInMeasure μ (F k) atTop (G k) := by
    cases k with
    | none => exact hLinear
    | some b =>
      cases b
      · exact hHessian
      · exact hRemainder
  obtain ⟨k, _, hPath⟩ := exists_seq_tendsto_ae_of_countable hData
  filter_upwards [hPath] with ω hω
  have hTel (n : ℕ) : L n ω + Q n ω + R n ω = f (X T ω) - f (X 0 ω) := by
    dsimp only [L, Q, R]
    rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    calc
      _ = ∑ i : Fin (2 ^ n), (f (X (t n i.succ) ω) - f (X (t n i.castSucc) ω)) := by
        apply Finset.sum_congr rfl
        intro i _
        have hInc : X (t n i.castSucc) ω + Δ n i ω = X (t n i.succ) ω := by
          dsimp only [Δ]
          abel
        rw [secondOrderRemainder, hInc, smul_eq_mul]
        dsimp only [H]
        ring
      _ = _ := by
        let g (i : Fin (2 ^ n + 1)) := f (X (t n i) ω)
        change (∑ i : Fin (2 ^ n), (g i.succ - g i.castSucc)) = _
        have hFirst : t n 0 = 0 := by simp [t, regularGridTimes]
        have hLast : t n (Fin.last (2 ^ n)) = T := regularDyadic_last_time T n
        rw [← hFirst, ← hLast, Finset.sum_sub_distrib]
        change (∑ i : Fin (2 ^ n), g i.succ) - (∑ i : Fin (2 ^ n), g i.castSucc) =
          g (Fin.last (2 ^ n)) - g 0
        linarith [Fin.sum_univ_succ g, Fin.sum_univ_castSucc g]
  have hLim : Tendsto (fun n => L (k n) ω + Q (k n) ω + R (k n) ω) atTop
      (𝓝 ((D ω + M T ω) + E ω + 0)) :=
    ((hω none).add (hω (some false))).add (hω (some true))
  have hConst : Tendsto (fun n => L (k n) ω + Q (k n) ω + R (k n) ω) atTop
      (𝓝 (f (X T ω) - f (X 0 ω))) :=
    (tendsto_congr' (Eventually.of_forall fun n => hTel (k n))).2 tendsto_const_nhds
  change f (X T ω) - f (X 0 ω) = D ω + E ω + M T ω
  rw [tendsto_nhds_unique hConst hLim]
  ring

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula
