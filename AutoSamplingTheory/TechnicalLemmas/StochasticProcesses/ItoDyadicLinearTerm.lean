import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoEuclideanGradientWeights
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteSumConvergenceInMeasure

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm

open Filter MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal Topology
open BrownianMotion ProgressiveL2 ElementaryItoIntegral SampledElementaryApproximation
  DyadicElementaryRefinement EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral ItoInitializedDrift ItoEuclideanGradientWeights
  ItoWeightedRiemannSums FiniteSumConvergenceInMeasure
open AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral

private noncomputable def weightedIncrementSum {Ω : Type*}
    (T : ℝ≥0) (W P : ℝ≥0 → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
  ∑ i : Fin (2 ^ n), W (t i.castSucc) ω * (P (t i.succ) ω - P (t i.castSucc) ω)

private theorem aestronglyMeasurable_weightedIncrementSum
    {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} {T : ℝ≥0}
    (hT : 0 < T) {W P : ℝ≥0 → Ω → ℝ}
    (hW : ∀ t ≤ T, AEStronglyMeasurable (W t) μ)
    (hP : ∀ t ≤ T, AEStronglyMeasurable (P t) μ) (n : ℕ) :
    AEStronglyMeasurable (weightedIncrementSum T W P n) μ := by
  let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
  have ht (i : Fin (2 ^ n + 1)) : t i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  have hCell (i : Fin (2 ^ n)) :
      AEStronglyMeasurable (fun ω => W (t i.castSucc) ω *
        (P (t i.succ) ω - P (t i.castSucc) ω)) μ :=
    (hW _ (ht _)).mul ((hP _ (ht _)).sub (hP _ (ht _)))
  exact (Finset.aestronglyMeasurable_sum Finset.univ fun i _ => hCell i).congr
    (Eventually.of_forall fun ω => by simp only [weightedIncrementSum, Finset.sum_apply, t])

open CompactStateRepresentative

set_option maxHeartbeats 700000 in
/-- The first-order Taylor sums converge to the actual drift integral plus
the terminal value of the completed martingale with the derivative integrands. -/
theorem tendstoInMeasure_dyadic_linear_ito_term
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
    (hf : ∀ x ∈ K, ContDiffAt ℝ 1 f x) :
    let A := fun (i : I) (t : ℝ≥0) (ω : Ω) => x ω i + prefixIntegralProcess (b i) t ω
    let X := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : J,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K) →
    ∃ θ : (I × J) → ProgressiveL2Integrand filtration μ T,
      (∀ᵐ ω ∂μ, ∀ q t, (θ q).process t ω =
        fderiv ℝ f (X (min t T) ω) (EuclideanSpace.basisFun I ℝ q.1) *
          (η q.1 q.2).process t ω) ∧
      let M := fun (t : ℝ≥0) (ω : Ω) => ∑ q : I × J,
        itoIntegralProcess (θ q) hT ((coordinateFamily hB).isBrownian q.2) hUsual t ω
      Martingale M filtration μ ∧ (∀ ω, M 0 ω = 0) ∧
      TendstoInMeasure μ (fun n ω =>
        let t := regularGridTimes (dyadicMesh T n) (2 ^ n)
        ∑ i : Fin (2 ^ n), fderiv ℝ f (X (t i.castSucc) ω)
          (X (t i.succ) ω - X (t i.castSucc) ω)) atTop
        (fun ω => (∫ s, fderiv ℝ f (X s ω) (WithLp.toLp 2 (fun i : I => b i s ω))
          ∂(TimeMeasure.upTo T)) + M T ω) := by
  intro A X hRange
  let e := EuclideanSpace.basisFun I ℝ
  let W (i : I) (t : ℝ≥0) (ω : Ω) :=
    fderiv ℝ f (restrictState fallback (X (min t T) ω) : EuclideanSpace ℝ I) (e i)
  let N (q : I × J) := itoIntegralProcess (η q.1 q.2) hT
    ((coordinateFamily hB).isBrownian q.2) hUsual
  have hA i := initialized_drift_progressive_continuous_boundedVariation
    (fun ω => x ω i) (hx i) (b i) (hb i) (hbi i)
  have hAp (i : I) : IsStronglyProgressive filtration (A i) := (hA i).1
  have hAeq (i : I) (s : ℝ≥0) (hs : s ≤ T) (ω : Ω) :
      A i s ω = x ω i + prefixIntegral (fun r => b i r ω) T s := (hA i).2.1 s hs ω
  have hW i := euclidean_ito_gradient_weight_progressive_bounded hB hT hUsual η A hAp
    (fun j => (hA j).2.2.mono fun _ h => h.1) hK fallback f hf i hRange
  have hWp (i : I) : IsStronglyProgressive filtration (W i) := (hW i).1
  have hWc (i : I) : ∀ᵐ ω ∂μ, ContinuousOn (fun t => W i t ω) (Icc 0 T) := (hW i).2.1
  choose C hC using fun i => (hW i).2.2
  have hNoise (q : I × J) := tendstoInMeasure_dyadic_weighted_ito_sums
    (η q.1 q.2) hT ((coordinateFamily hB).isBrownian q.2) hUsual (W q.1)
    (hWp q.1) (hWc q.1) (hC q.1)
  choose θ hθ hN using hNoise
  let L (q : I × J) := itoIntegralProcess (θ q) hT
    ((coordinateFamily hB).isBrownian q.2) hUsual
  let M (t : ℝ≥0) (ω : Ω) := ∑ q : I × J, L q t ω
  have hMart (s : Finset (I × J)) : Martingale (∑ q ∈ s, L q) filtration μ := by
    induction s using Finset.induction_on with
    | empty => simpa only [Finset.sum_empty] using (martingale_zero (E := ℝ) filtration μ)
    | insert q s hq ih =>
      rw [Finset.sum_insert hq]
      exact (itoIntegralProcess_martingale (θ q) hT
        ((coordinateFamily hB).isBrownian q.2) hUsual).add ih
  have hM : Martingale M filtration μ := by
    have hEq : M = ∑ q : I × J, L q := by
      funext t ω
      simp only [M, Finset.sum_apply]
    rw [hEq]
    exact hMart Finset.univ
  have hZero (ω : Ω) : M 0 ω = 0 := by
    simp only [M, L, itoIntegralProcess_at_zero, Pi.zero_apply, Finset.sum_const_zero]
  refine ⟨θ, ?_, hM, hZero, ?_⟩
  · filter_upwards [hRange] with ω hr q t
    rw [hθ]
    dsimp only [W, e]
    rw [coe_restrictState_of_mem fallback (hr _ (min_le_right _ _))]
  let t (n : ℕ) := regularGridTimes (dyadicMesh T n) (2 ^ n)
  have ht (n : ℕ) (i : Fin (2 ^ n + 1)) : t n i ≤ T :=
    ((regularGridTimes_strictMono (dyadicMesh_pos hT n) _).monotone (Fin.le_last i)).trans_eq
      (regularDyadic_last_time T n)
  let F (i : I) := weightedIncrementSum T (W i) (A i)
  let G (q : I × J) := weightedIncrementSum T (W q.1) (N q)
  let D (i : I) (ω : Ω) := ∫ s, W i s ω * b i s ω ∂(TimeMeasure.upTo T)
  have hFromProg {P : ℝ≥0 → Ω → ℝ} (h : IsStronglyProgressive filtration P)
      (s : ℝ≥0) (_ : s ≤ T) : AEStronglyMeasurable (P s) μ :=
    ((h.stronglyAdapted s).mono (filtration.le s)).aestronglyMeasurable
  have hFm (i : I) (n : ℕ) : AEStronglyMeasurable (F i n) μ :=
    aestronglyMeasurable_weightedIncrementSum hT (hFromProg (hWp i)) (hFromProg (hAp i)) n
  have hGm (q : I × J) (n : ℕ) : AEStronglyMeasurable (G q n) μ :=
    aestronglyMeasurable_weightedIncrementSum hT (hFromProg (hWp q.1)) (fun s _ =>
      ((itoIntegralProcess_stronglyAdapted (η q.1 q.2) hT ((coordinateFamily hB).isBrownian q.2)
        hUsual s).mono (filtration.le s)).aestronglyMeasurable) n
  have hF (i : I) : TendstoInMeasure μ (F i) atTop (D i) := by
    apply tendstoInMeasure_of_tendsto_ae (hFm i)
    filter_upwards [hWc i, hbi i] with ω hw hi
    have hlim := tendsto_dyadic_weighted_prefixIntegral_sums
      (fun s => W i s ω) (fun s => b i s ω) T hT hw hi
    refine (tendsto_congr' (Eventually.of_forall fun n => ?_)).2 hlim
    apply Finset.sum_congr rfl
    intro k _
    rw [hAeq i _ (ht n k.succ) ω, hAeq i _ (ht n k.castSucc) ω,
      add_sub_add_left_eq_sub]
  have hG (q : I × J) : TendstoInMeasure μ (G q) atTop (L q T) := hN q
  have hSum : TendstoInMeasure μ
      (fun n ω => (∑ i : I, F i n ω) + ∑ q : I × J, G q n ω) atTop
      (fun ω => (∑ i : I, D i ω) + M T ω) := by
    let S : I ⊕ (I × J) → ℕ → Ω → ℝ := Sum.elim F G
    let Q : I ⊕ (I × J) → Ω → ℝ := Sum.elim D (fun q => L q T)
    have hS (k : I ⊕ (I × J)) (n : ℕ) : AEStronglyMeasurable (S k n) μ := by
      cases k with
      | inl i => exact hFm i n
      | inr q => exact hGm q n
    have hQ (k : I ⊕ (I × J)) : TendstoInMeasure μ (S k) atTop (Q k) := by
      cases k with
      | inl i => exact hF i
      | inr q => exact hG q
    simpa only [S, Q, Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr, M] using
      tendstoInMeasure_fintype_sum hS hQ
  have hExpand (l : EuclideanSpace ℝ I →L[ℝ] ℝ) (v : EuclideanSpace ℝ I) :
      l v = ∑ i : I, l (e i) * v i := by
    have h : (∑ i : I, v i • e i) = v := by
      simpa only [e, EuclideanSpace.basisFun_repr] using e.sum_repr v
    calc
      l v = l (∑ i : I, v i • e i) := congrArg l h.symm
      _ = _ := by simp only [map_sum, map_smul, smul_eq_mul, mul_comm]
  refine TendstoInMeasure.congr ?_ ?_ hSum
  · intro n
    filter_upwards [hRange] with ω hr
    simp only [F, G, weightedIncrementSum, Fintype.sum_prod_type]
    change ((∑ i : I, ∑ k : Fin (2 ^ n), W i (t n k.castSucc) ω *
      (A i (t n k.succ) ω - A i (t n k.castSucc) ω)) +
      ∑ i : I, ∑ j : J, ∑ k : Fin (2 ^ n), W i (t n k.castSucc) ω *
        (N (i, j) (t n k.succ) ω - N (i, j) (t n k.castSucc) ω)) =
      ∑ k : Fin (2 ^ n), fderiv ℝ f (X (t n k.castSucc) ω)
        (X (t n k.succ) ω - X (t n k.castSucc) ω)
    have hSwap (i : I) : (∑ j : J, ∑ k : Fin (2 ^ n), W i (t n k.castSucc) ω *
        (N (i, j) (t n k.succ) ω - N (i, j) (t n k.castSucc) ω)) =
        ∑ k : Fin (2 ^ n), ∑ j : J, W i (t n k.castSucc) ω *
          (N (i, j) (t n k.succ) ω - N (i, j) (t n k.castSucc) ω) := Finset.sum_comm
    simp_rw [hSwap]
    simp_rw [← Finset.sum_add_distrib]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro k _
    rw [hExpand]
    apply Finset.sum_congr rfl
    intro i _
    rw [← Finset.mul_sum, ← mul_add, Finset.sum_sub_distrib]
    simp only [W, min_eq_left (ht n k.castSucc),
      coe_restrictState_of_mem fallback (hr _ (ht n k.castSucc)), X, PiLp.sub_apply, N]
    ring
  · filter_upwards [ae_all_iff.2 hWc, ae_all_iff.2 hbi, hRange] with ω hw hi hr
    let ν := TimeMeasure.upTo T
    have hMem : ∀ᵐ s ∂ν, s ∈ Icc (0 : ℝ≥0) T :=
      (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ hs => ⟨hs.1.le, hs.2⟩
    have hRest : ν.restrict (Icc 0 T) = ν := Measure.restrict_eq_self_of_ae_mem hMem
    have hInt (i : I) : Integrable (fun s => W i s ω * b i s ω) ν := by
      have hm : AEStronglyMeasurable (fun s => W i s ω) ν := by
        rw [← hRest]
        exact (hw i).aestronglyMeasurable measurableSet_Icc
      exact (hi i).bdd_mul hm (hMem.mono fun s hs => by
        simpa only [Real.norm_eq_abs] using hC i s hs.2 ω)
    apply congrArg (· + M T ω)
    change (∑ i : I, ∫ s, W i s ω * b i s ω ∂ν) =
      ∫ s, fderiv ℝ f (X s ω) (WithLp.toLp 2 (fun i : I => b i s ω)) ∂ν
    rw [← integral_finsetSum _ (fun i _ => hInt i)]
    apply integral_congr_ae
    filter_upwards [hMem] with s hs
    rw [hExpand]
    simp only [W, min_eq_left hs.2, coe_restrictState_of_mem fallback (hr s hs.2)]

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoDyadicLinearTerm
