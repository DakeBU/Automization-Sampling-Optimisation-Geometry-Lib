import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoCompactEuclideanFormula
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakMeasurableEvolution
import Mathlib.Analysis.Calculus.FDeriv.CompCLM

/-!
# Expected squared chord energy for supplied synchronous sphere processes

Each matched particle pair uses one coordinate family from the same vector Brownian
motion. No independence between different particle drivers is required. Continuous
coefficient fields may depend on both complete particle configurations. The result
concerns supplied coordinate SDE solutions with fixed nonnegative temperature;
it does not assert existence of such solutions.
-/
noncomputable section

namespace SynchronousSphereCoupling

open MeasureTheory ProbabilityTheory Set
open scoped BigOperators NNReal RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses
open BrownianMotion ProgressiveL2 EuclideanBrownianCoordinates ItoIntegralProcess
  ProgressiveDriftIntegral SphereMeasurableCoordinateSDE
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise

variable {d : ℕ}
local notation "E" => EuclideanSpace ℝ (Fin d)
local notation "F" => EuclideanSpace ℝ (Bool × Fin d)

private def block (b : Bool) : F →L[ℝ] E :=
  (PiLp.continuousLinearEquiv 2 ℝ (fun _ : Fin d => ℝ)).symm.toContinuousLinearMap.comp
    (ContinuousLinearMap.pi fun j => PiLp.proj 2 (fun _ : Bool × Fin d => ℝ) (b,j))

private def difference : F →L[ℝ] E := block false - block true

private def pair (x y : E) : F :=
  WithLp.toLp 2 (fun q => if q.1 then y q.2 else x q.2)

private theorem block_pair_false (x y : E) : block false (pair x y) = x := by
  ext j
  rfl

private theorem block_pair_true (x y : E) : block true (pair x y) = y := by
  ext j
  rfl

private theorem difference_pair (x y : E) : difference (pair x y) = x - y := by
  simp only [difference, sub_apply, block_pair_false, block_pair_true]

private theorem quadratic_fderiv {V W : Type*}
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup W] [InnerProductSpace ℝ W]
    (D : V →L[ℝ] W) (z v : V) :
    fderiv ℝ (fun a => ‖D a‖ ^ 2) z v = 2 * inner ℝ (D z) (D v) := by
  rw [(D.hasFDerivAt.norm_sq).fderiv]
  simp

private theorem quadratic_hessian {V W : Type*}
    [NormedAddCommGroup V] [NormedSpace ℝ V]
    [NormedAddCommGroup W] [InnerProductSpace ℝ W]
    (D : V →L[ℝ] W) (z v w : V) :
    fderiv ℝ (fderiv ℝ (fun a => ‖D a‖ ^ 2)) z v w =
      2 * inner ℝ (D v) (D w) := by
  let K : V →L[ℝ] V →L[ℝ] ℝ :=
    2 • (((ContinuousLinearMap.compL ℝ V W ℝ).flip D).comp ((innerSL ℝ).comp D))
  have heq : fderiv ℝ (fun a => ‖D a‖ ^ 2) = K := by
    ext a b
    rw [quadratic_fderiv]
    simp [K]
  rw [heq, K.fderiv]
  simp [K]

private theorem projection_difference_sum (x y : E) (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) :
    (∑ j : Fin d, ‖projectedNoiseColumn j x - projectedNoiseColumn j y‖ ^ 2) =
      2 * (1 - (inner ℝ x y) ^ 2) := by
  have heq (j : Fin d) : projectedNoiseColumn j x - projectedNoiseColumn j y =
      y j • y - x j • x := by
    simp only [projectedNoiseColumn]
    abel
  have hterm (j : Fin d) : ‖projectedNoiseColumn j x - projectedNoiseColumn j y‖ ^ 2 =
      (x j)^2 + (y j)^2 - 2 * inner ℝ x y * (x j * y j) := by
    rw [heq, norm_sub_sq_real]
    simp only [norm_smul, hx, hy, mul_one, Real.norm_eq_abs, sq_abs,
      real_inner_smul_left, inner_smul_right, real_inner_comm y x]
    ring
  have hs (v : E) : (∑ j : Fin d, (v j)^2) = ‖v‖^2 := by
    simp only [PiLp.norm_sq_eq_of_L2, Real.norm_eq_abs, sq_abs]
  have hi : (∑ j : Fin d, x j * y j) = inner ℝ x y := by
    simp [PiLp.inner_apply, mul_comm]
  simp_rw [hterm]
  rw [Finset.sum_sub_distrib, Finset.sum_add_distrib, ← Finset.mul_sum, hs, hs, hi, hx, hy]
  ring

private theorem radial_noise_identity (lambda : ℝ) (x y : E)
    (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) :
    -2 * lambda * ((d : ℝ) - 1) * ‖x-y‖^2 +
      2 * lambda * ∑ j : Fin d, ‖projectedNoiseColumn j x - projectedNoiseColumn j y‖^2 =
      -2 * lambda * ((d : ℝ) - 3) * ‖x-y‖^2 - lambda * ‖x-y‖^4 := by
  have hchord : ‖x-y‖^2 = 2 * (1 - inner ℝ x y) := by
    rw [norm_sub_sq_real, hx, hy]
    ring
  rw [projection_difference_sum x y hx hy, show ‖x-y‖^4 = (‖x-y‖^2)^2 by ring, hchord]
  ring

private theorem quadratic_ito_at_horizon
    {Ω I J W : Type*} [MeasurableSpace Ω]
    [Fintype I] [DecidableEq I] [Fintype J] [DecidableEq J]
    [NormedAddCommGroup W] [InnerProductSpace ℝ W]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → EuclideanSpace ℝ J}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : I → J → ProgressiveL2Integrand filtration μ T)
    (x : Ω → I → ℝ) (hx : ∀ i, StronglyMeasurable[filtration 0] (fun ω => x ω i))
    (b : I → ℝ≥0 → Ω → ℝ) (hb : ∀ i, IsStronglyProgressive filtration (b i))
    (hbi : ∀ i, ∀ᵐ ω ∂μ, Integrable (fun s => b i s ω) (TimeMeasure.upTo T))
    {K : Set (EuclideanSpace ℝ I)} (hK : IsCompact K) (fallback : K)
    (D : EuclideanSpace ℝ I →L[ℝ] W) :
    let A := fun (i : I) (t : ℝ≥0) (ω : Ω) => x ω i + prefixIntegralProcess (b i) t ω
    let Z := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => A i t ω + ∑ j : J,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    let v := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : I => b i t ω)
    let σ := fun (j : J) (t : ℝ≥0) (ω : Ω) =>
      WithLp.toLp 2 (fun i : I => (η i j).process t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, Z t ω ∈ K) →
    ∃ M : ℝ≥0 → Ω → ℝ, Martingale M filtration μ ∧ (∀ ω, M 0 ω = 0) ∧
      (∀ᵐ ω ∂μ, ‖D (Z T ω)‖ ^ 2 - ‖D (Z 0 ω)‖ ^ 2 =
        (∫ s, 2 * inner ℝ (D (Z s ω)) (D (v s ω)) +
          ∑ j : J, ‖D (σ j s ω)‖ ^ 2 ∂(TimeMeasure.upTo T)) + M T ω) := by
  intro A Z v σ hRange
  let f := fun a => ‖D a‖ ^ 2
  have hf : ∀ a ∈ K, ContDiffAt ℝ 2 f a := fun _ _ =>
    (D.contDiff.norm_sq ℝ).contDiffAt
  obtain ⟨θ, _, hM, hM0, hIto⟩ :=
    ItoCompactEuclideanFormula.ito_formula_compact_euclidean_at_horizon
      hB hT hUsual η x hx b hb hbi hK fallback f hf hRange
  let M (s : ℝ≥0) (ω : Ω) := ∑ q : I × J,
    itoIntegralProcess (θ q) hT ((coordinateFamily hB).isBrownian q.2) hUsual s ω
  refine ⟨M, hM, hM0, ?_⟩
  have hA (i : I) := ItoInitializedDrift.initialized_drift_progressive_continuous_boundedVariation
    (fun ω => x ω i) (hx i) (b i) (hb i) (hbi i)
  have hAmeas (i : I) (s : ℝ≥0) (_ : s ≤ T) : AEStronglyMeasurable (A i s) μ :=
    (((hA i).1.stronglyAdapted s).mono (filtration.le s)).aestronglyMeasurable
  obtain ⟨_, hZc⟩ := ItoEuclideanRowRegularity.measurable_continuousOn_euclidean_ito_rows
    hB hT hUsual η A hAmeas (fun i => (hA i).2.2.mono fun _ h => h.1)
  have hInt := ItoGeneratorIntegrability.ae_integrable_euclidean_generator_terms
    η b hbi Z hZc hRange f hf
  filter_upwards [hIto, hInt] with ω hω hint
  change ‖D (Z T ω)‖ ^ 2 - ‖D (Z 0 ω)‖ ^ 2 =
    (∫ s, fderiv ℝ f (Z s ω) (v s ω) ∂(TimeMeasure.upTo T)) +
    (∫ s, (1 / 2 : ℝ) * ∑ j : J,
      fderiv ℝ (fderiv ℝ f) (Z s ω) (σ j s ω) (σ j s ω) ∂(TimeMeasure.upTo T)) + M T ω at hω
  rw [hω, ← integral_add hint.1 hint.2]
  congr 1
  apply integral_congr_ae
  exact Filter.Eventually.of_forall fun s => by
    simp only [f, quadratic_fderiv, quadratic_hessian,
      real_inner_self_eq_norm_sq, ← Finset.mul_sum]
    ring

private theorem sphere_pair_generator (lambda : ℝ) (hlambda : 0 ≤ lambda)
    (x y u v : E) (hx : ‖x‖ = 1) (hy : ‖y‖ = 1) :
    2 * inner ℝ (x-y)
      ((u - (lambda * ((d : ℝ)-1)) • x) - (v - (lambda * ((d : ℝ)-1)) • y)) +
      (∑ j : Fin d, ‖Real.sqrt (2*lambda) • projectedNoiseColumn j x -
        Real.sqrt (2*lambda) • projectedNoiseColumn j y‖^2) =
      2 * inner ℝ (x-y) (u-v) - 2*lambda*((d : ℝ)-3)*‖x-y‖^2 - lambda*‖x-y‖^4 := by
  have hdiff : (u - (lambda * ((d : ℝ)-1)) • x) -
      (v - (lambda * ((d : ℝ)-1)) • y) =
      (u-v) - (lambda * ((d : ℝ)-1)) • (x-y) := by
    simp only [smul_sub]
    abel
  have hroot : (Real.sqrt (2*lambda))^2 = 2*lambda := Real.sq_sqrt (by positivity)
  rw [hdiff, inner_sub_right, inner_smul_right, real_inner_self_eq_norm_sq]
  simp only [← smul_sub, norm_smul, mul_pow, Real.norm_eq_abs, sq_abs, hroot, ← Finset.mul_sum]
  have h := radial_noise_identity lambda x y hx hy
  linarith

private theorem continuous_pair : Continuous (fun z : E × E => pair z.1 z.2) := by
  apply (PiLp.continuous_toLp 2 (fun _ : Bool × Fin d => ℝ)).comp
  apply continuous_pi
  intro q
  rcases q with ⟨b,j⟩
  cases b <;> simp only [Bool.false_eq_true, if_false, if_true] <;> fun_prop

private theorem spherical_pair_ito
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    {B : ℝ≥0 → Ω → E}
    (hB : IsStandardBrownianMotionWithFiltration B filtration μ) (hT : 0 < T)
    (hUsual : SatisfiesUsualConditions filtration μ)
    (η : (Bool × Fin d) → Fin d → ProgressiveL2Integrand filtration μ T)
    (x : Ω → Bool × Fin d → ℝ)
    (hx : ∀ i, StronglyMeasurable[filtration 0] (fun ω => x ω i))
    (b : (Bool × Fin d) → ℝ≥0 → Ω → ℝ)
    (hb : ∀ i, IsStronglyProgressive filtration (b i))
    (hbi : ∀ i, ∀ᵐ ω ∂μ, Integrable (fun s => b i s ω) (TimeMeasure.upTo T))
    (X Y : ℝ≥0 → Ω → Metric.sphere (0 : E) 1)
    (fallback : Metric.sphere (0 : E) 1)
    (u v : ℝ≥0 → Ω → E) (lambda : ℝ) (hlambda : 0 ≤ lambda) :
    let A := fun (i : Bool × Fin d) (t : ℝ≥0) (ω : Ω) => x ω i + prefixIntegralProcess (b i) t ω
    let Z := fun (t : ℝ≥0) (ω : Ω) => WithLp.toLp 2 (fun i : Bool × Fin d => A i t ω + ∑ j : Fin d,
      itoIntegralProcess (η i j) hT ((coordinateFamily hB).isBrownian j) hUsual t ω)
    (∀ᵐ ω ∂μ, ∀ t ≤ T, Z t ω = pair (X t ω) (Y t ω)) →
    (∀ᵐ ω ∂μ, ∀ t ≤ T, WithLp.toLp 2 (fun i => b i t ω) =
      pair (u t ω - (lambda*((d : ℝ)-1)) • (X t ω : E))
        (v t ω - (lambda*((d : ℝ)-1)) • (Y t ω : E))) →
    (∀ᵐ ω ∂μ, ∀ t ≤ T, ∀ j : Fin d, WithLp.toLp 2 (fun i => (η i j).process t ω) =
      pair (Real.sqrt (2*lambda) • projectedNoiseColumn j (X t ω : E))
        (Real.sqrt (2*lambda) • projectedNoiseColumn j (Y t ω : E))) →
    ∃ M : ℝ≥0 → Ω → ℝ, Martingale M filtration μ ∧ (∀ ω, M 0 ω = 0) ∧
      (∀ᵐ ω ∂μ, ‖(X T ω : E)-(Y T ω : E)‖^2 - ‖(X 0 ω : E)-(Y 0 ω : E)‖^2 =
        (∫ s, 2 * inner ℝ ((X s ω : E)-(Y s ω : E)) (u s ω-v s ω) -
          2*lambda*((d : ℝ)-3)*‖(X s ω : E)-(Y s ω : E)‖^2 -
          lambda*‖(X s ω : E)-(Y s ω : E)‖^4 ∂(TimeMeasure.upTo T)) + M T ω) := by
  intro A Z hEq hDrift hNoise
  let S := Metric.sphere (0 : E) 1
  let : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  let K : Set F := Set.range (fun z : S × S => pair (z.1 : E) (z.2 : E))
  have hK : IsCompact K := isCompact_range
    (continuous_pair.comp (continuous_subtype_val.prodMap continuous_subtype_val))
  let start : K := ⟨pair (fallback : E) fallback, ⟨⟨fallback,fallback⟩,rfl⟩⟩
  have hRange : ∀ᵐ ω ∂μ, ∀ t ≤ T, Z t ω ∈ K :=
    hEq.mono fun ω h t ht => ⟨⟨X t ω,Y t ω⟩,(h t ht).symm⟩
  obtain ⟨M,hM,hM0,hIto⟩ := quadratic_ito_at_horizon hB hT hUsual η x hx b hb hbi
    hK start difference hRange
  refine ⟨M,hM,hM0,?_⟩
  filter_upwards [hEq,hDrift,hNoise,hIto] with ω heq hd hn hi
  change ‖difference (Z T ω)‖^2 - ‖difference (Z 0 ω)‖^2 =
    (∫ s, 2 * inner ℝ (difference (Z s ω))
      (difference (WithLp.toLp 2 (fun i => b i s ω))) +
      ∑ j : Fin d, ‖difference (WithLp.toLp 2 (fun i => (η i j).process s ω))‖^2
      ∂(TimeMeasure.upTo T)) + M T ω at hi
  rw [heq T le_rfl,heq 0 bot_le,difference_pair,difference_pair] at hi
  apply hi.trans
  apply congrArg (fun a : ℝ => a + M T ω)
  apply integral_congr_ae
  filter_upwards [TimeMeasure.ae_le_terminal T] with t ht
  rw [heq t ht,hd t ht,difference_pair,difference_pair]
  simp only [hn t ht,difference_pair]
  exact sphere_pair_generator (d := d) lambda hlambda (X t ω : E) (Y t ω : E) (u t ω) (v t ω)
    (mem_sphere_zero_iff_norm.mp (X t ω).property)
    (mem_sphere_zero_iff_norm.mp (Y t ω).property)

variable {N : ℕ}
local notation "S" => Metric.sphere (0 : E) 1
local notation "C" => Fin N → S

private theorem source_particle_balance
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    (P : ProbabilityMeasure Ω) (_hN : 0 < N)
    (B : Fin N → ℝ≥0 → Ω → E)
    (hB : ∀ i, IsStandardBrownianMotionWithFiltration (B i) filtration (P : Measure Ω))
    (hUsual : SatisfiesUsualConditions filtration (P : Measure Ω))
    (X Y : Fin N → ℝ≥0 → Ω → S)
    (hX : ∀ i, Measurable (Function.uncurry (X i)))
    (hY : ∀ i, Measurable (Function.uncurry (Y i)))
    (hProgressiveX : ∀ i, IsStronglyProgressive filtration (X i))
    (hProgressiveY : ∀ i, IsStronglyProgressive filtration (Y i))
    (bX bY : ℝ≥0 → C → C → Fin N → E)
    (hbX : ∀ i, Continuous (fun z : ℝ≥0 × (C × C) => bX z.1 z.2.1 z.2.2 i))
    (hbY : ∀ i, Continuous (fun z : ℝ≥0 × (C × C) => bY z.1 z.2.1 z.2.2 i))
    (lambda : ℝ) (hlambda : 0 ≤ lambda)
    (hEquation : ∀ (T : ℝ≥0) (hT : 0 < T), ∀ᵐ ω ∂(P : Measure Ω),
      ∀ t ≤ T, ∀ (i : Fin N) (k : Fin d),
        ((X i t ω : E) k = (X i 0 ω : E) k +
          prefixIntegralProcess (fun v a =>
            (bX v (fun l => X l v a) (fun l => Y l v a) i) k -
              lambda * ((d : ℝ) - 1) * (X i v a : E) k) t ω +
          ∑ j : Fin d, itoIntegralProcess
            (sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (X i)
              (hX i) (hProgressiveX i) (fun _ => lambda) measurable_const
              ⟨‖lambda‖, fun _ _ => le_rfl⟩ k j)
            hT ((coordinateFamily (hB i)).isBrownian j) hUsual t ω) ∧
        ((Y i t ω : E) k = (Y i 0 ω : E) k +
          prefixIntegralProcess (fun v a =>
            (bY v (fun l => X l v a) (fun l => Y l v a) i) k -
              lambda * ((d : ℝ) - 1) * (Y i v a : E) k) t ω +
          ∑ j : Fin d, itoIntegralProcess
            (sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (Y i)
              (hY i) (hProgressiveY i) (fun _ => lambda) measurable_const
              ⟨‖lambda‖, fun _ _ => le_rfl⟩ k j)
            hT ((coordinateFamily (hB i)).isBrownian j) hUsual t ω)) :
    ∀ (T : ℝ≥0) (_hT : 0 < T) (i : Fin N),
      ∃ M : ℝ≥0 → Ω → ℝ, Martingale M filtration (P : Measure Ω) ∧
        (∀ ω, M 0 ω = 0) ∧
        (∀ᵐ ω ∂(P : Measure Ω),
          ContinuousOn (fun t => X i t ω) (Icc 0 T) ∧
          ContinuousOn (fun t => Y i t ω) (Icc 0 T)) ∧
        (∀ᵐ ω ∂(P : Measure Ω),
          ‖(X i T ω : E)-(Y i T ω : E)‖^2 - ‖(X i 0 ω : E)-(Y i 0 ω : E)‖^2 =
          (∫ t, 2 * inner ℝ ((X i t ω : E)-(Y i t ω : E))
              (bX t (fun l => X l t ω) (fun l => Y l t ω) i -
               bY t (fun l => X l t ω) (fun l => Y l t ω) i) -
            2*lambda*((d : ℝ)-3)*‖(X i t ω : E)-(Y i t ω : E)‖^2 -
            lambda*‖(X i t ω : E)-(Y i t ω : E)‖^4 ∂(TimeMeasure.upTo T)) + M T ω) := by
  classical
  intro T hT i
  let : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  let Q := C × C
  let Z (t : ℝ≥0) (ω : Ω) : Q := (fun l => X l t ω, fun l => Y l t ω)
  have hZ : Measurable (Function.uncurry Z) :=
    (measurable_pi_lambda _ fun l => hX l).prodMk (measurable_pi_lambda _ fun l => hY l)
  have hZp : IsStronglyProgressive filtration Z := by
    intro t
    let _ : MeasurableSpace Ω := filtration t
    exact ((measurable_pi_lambda _ fun l => (hProgressiveX l t).measurable).prodMk
      (measurable_pi_lambda _ fun l => (hProgressiveY l t).measurable)).stronglyMeasurable
  let c (q : Bool × Fin d) (z : ℝ≥0 × Q) : ℝ :=
    if q.1 then (bY z.1 z.2.1 z.2.2 i) q.2 - lambda*((d : ℝ)-1)*(z.2.2 i : E) q.2
    else (bX z.1 z.2.1 z.2.2 i) q.2 - lambda*((d : ℝ)-1)*(z.2.1 i : E) q.2
  have hc (q : Bool × Fin d) : Continuous (c q) := by
    rcases q with ⟨a,k⟩
    let L : E →L[ℝ] ℝ := PiLp.proj 2 (fun _ : Fin d => ℝ) k
    cases a
    · change Continuous (fun z : ℝ≥0 × Q => L (bX z.1 z.2.1 z.2.2 i) -
        lambda*((d : ℝ)-1)*(z.2.1 i : E) k)
      exact (L.continuous.comp (hbX i)).sub (by dsimp [Q]; fun_prop)
    · change Continuous (fun z : ℝ≥0 × Q => L (bY z.1 z.2.1 z.2.2 i) -
        lambda*((d : ℝ)-1)*(z.2.2 i : E) k)
      exact (L.continuous.comp (hbY i)).sub (by dsimp [Q]; fun_prop)
  let b (q : Bool × Fin d) (t : ℝ≥0) (ω : Ω) := c q (t,Z t ω)
  have hRow (q : Bool × Fin d) : IsStronglyProgressive filtration (b q) ∧
      ∀ ω, Integrable (fun t => b q t ω) (TimeMeasure.upTo T) := by
    have hK : IsCompact (Icc (0 : ℝ≥0) T ×ˢ (univ : Set Q)) := isCompact_Icc.prod isCompact_univ
    obtain ⟨C₀,hC₀⟩ := hK.bddAbove_image (hc q).norm.continuousOn
    have hBound : ∃ C₀ : ℝ, ∀ t ≤ T, ∀ w, ‖c q (t,w)‖ ≤ C₀ :=
      ⟨C₀,fun t ht w => hC₀ ⟨(t,w),⟨⟨bot_le,ht⟩,mem_univ w⟩,rfl⟩⟩
    have h := ProgressiveCoefficientBounds.bounded_measurable_coefficient_along_progressive_process
      (μ := (P : Measure Ω)) Z hZ hZp (c q) (hc q).measurable T 1 hBound
    exact ⟨h.1,h.2.1⟩
  let η (q : Bool × Fin d) (j : Fin d) : ProgressiveL2Integrand filtration (P : Measure Ω) T :=
    if q.1 then sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (Y i)
      (hY i) (hProgressiveY i) (fun _ => lambda) measurable_const ⟨‖lambda‖,fun _ _ => le_rfl⟩ q.2 j
    else sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (X i)
      (hX i) (hProgressiveX i) (fun _ => lambda) measurable_const ⟨‖lambda‖,fun _ _ => le_rfl⟩ q.2 j
  let x (ω : Ω) (q : Bool × Fin d) := if q.1 then (Y i 0 ω : E) q.2 else (X i 0 ω : E) q.2
  have hx (q : Bool × Fin d) : StronglyMeasurable[filtration 0] (fun ω => x ω q) := by
    rcases q with ⟨a,k⟩
    let L : E →L[ℝ] ℝ := PiLp.proj 2 (fun _ : Fin d => ℝ) k
    cases a
    · exact (L.continuous.comp continuous_subtype_val).comp_stronglyMeasurable
        ((hProgressiveX i).stronglyAdapted 0)
    · exact (L.continuous.comp continuous_subtype_val).comp_stronglyMeasurable
        ((hProgressiveY i).stronglyAdapted 0)
  let A (q : Bool × Fin d) (t : ℝ≥0) (ω : Ω) := x ω q + prefixIntegralProcess (b q) t ω
  let R (t : ℝ≥0) (ω : Ω) : F := WithLp.toLp 2 (fun q => A q t ω + ∑ j : Fin d,
    itoIntegralProcess (η q j) hT ((coordinateFamily (hB i)).isBrownian j) hUsual t ω)
  have hEq : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, R t ω = pair (X i t ω) (Y i t ω) := by
    filter_upwards [hEquation T hT] with ω hω t ht
    ext ⟨a,k⟩
    cases a
    · exact (hω t ht i k).1.symm
    · exact (hω t ht i k).2.symm
  have hd : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, WithLp.toLp 2 (fun q => b q t ω) =
      pair (bX t (Z t ω).1 (Z t ω).2 i - (lambda*((d : ℝ)-1)) • (X i t ω : E))
        (bY t (Z t ω).1 (Z t ω).2 i - (lambda*((d : ℝ)-1)) • (Y i t ω : E)) := by
    exact Filter.Eventually.of_forall fun ω t _ => by
      ext ⟨a,k⟩
      cases a <;> rfl
  have hn : ∀ᵐ ω ∂(P : Measure Ω), ∀ t ≤ T, ∀ j : Fin d,
      WithLp.toLp 2 (fun q => (η q j).process t ω) =
        pair (Real.sqrt (2*lambda) • projectedNoiseColumn j (X i t ω : E))
          (Real.sqrt (2*lambda) • projectedNoiseColumn j (Y i t ω : E)) := by
    exact Filter.Eventually.of_forall fun ω t _ j => by
      ext ⟨a,k⟩
      cases a <;> rfl
  let ω₀ := Classical.choice (nonempty_of_isProbabilityMeasure (P : Measure Ω))
  obtain ⟨M,hM,hM0,hIto⟩ := spherical_pair_ito (hB i) hT hUsual η x hx b
    (fun q => (hRow q).1) (fun q => Filter.Eventually.of_forall (hRow q).2)
    (X i) (Y i) (X i 0 ω₀)
    (fun t ω => bX t (Z t ω).1 (Z t ω).2 i)
    (fun t ω => bY t (Z t ω).1 (Z t ω).2 i) lambda hlambda hEq hd hn
  refine ⟨M,hM,hM0,?_,hIto⟩
  have hA (q : Bool × Fin d) := ItoInitializedDrift.initialized_drift_progressive_continuous_boundedVariation (μ := (P : Measure Ω))
    (fun ω => x ω q) (hx q) (b q) (hRow q).1 (Filter.Eventually.of_forall (hRow q).2)
  have hAmeas (q : Bool × Fin d) (t : ℝ≥0) (_ : t ≤ T) : AEStronglyMeasurable (A q t) (P : Measure Ω) :=
    (((hA q).1.stronglyAdapted t).mono (filtration.le t)).aestronglyMeasurable
  obtain ⟨_,hRc⟩ := ItoEuclideanRowRegularity.measurable_continuousOn_euclidean_ito_rows
    (hB i) hT hUsual η A hAmeas (fun q => (hA q).2.2.mono fun _ h => h.1)
  filter_upwards [hEq,hRc] with ω heq hcR
  constructor
  · apply Topology.IsInducing.subtypeVal.continuousOn_iff.mpr
    apply ((block false).continuous.comp_continuousOn hcR).congr
    intro t ht
    change (X i t ω : E) = block false (R t ω)
    rw [heq t ht.2,block_pair_false]
  · apply Topology.IsInducing.subtypeVal.continuousOn_iff.mpr
    apply ((block true).continuous.comp_continuousOn hcR).congr
    intro t ht
    change (Y i t ω : E) = block true (R t ω)
    rw [heq t ht.2,block_pair_true]


private theorem continuous_paths_of_horizon
    {Ω V : Type*} [MeasurableSpace Ω] [TopologicalSpace V]
    (μ : Measure Ω) (X : ℝ≥0 → Ω → V)
    (h : ∀ T : ℝ≥0, 0 < T → ∀ᵐ ω ∂μ, ContinuousOn (fun t => X t ω) (Icc 0 T)) :
    ∀ᵐ ω ∂μ, Continuous (fun t => X t ω) := by
  have hcount : ∀ᵐ ω ∂μ, ∀ n : ℕ, ContinuousOn (fun t => X t ω) (Icc 0 (n+1 : ℝ≥0)) :=
    ae_all_iff.mpr (fun n => h (n+1) (by positivity))
  filter_upwards [hcount] with ω hω
  rw [continuous_iff_continuousAt]
  intro t
  obtain ⟨n,hn⟩ := exists_nat_gt t
  have ht : t < (n+1 : ℝ≥0) := hn.trans (by exact_mod_cast Nat.lt_succ_self n)
  apply (hω n t ⟨bot_le,ht.le⟩).continuousAt
  simpa only [show (0 : ℝ≥0) = ⊥ from rfl, Icc_bot] using (Iic_mem_nhds ht)

private theorem upTo_integral_real (f : ℝ≥0 → ℝ) (T : ℝ≥0) :
    (∫ s, f s ∂(TimeMeasure.upTo T)) = ∫ s in (0 : ℝ)..(T : ℝ), f s.toNNReal := by
  rw [← TimeMeasure.restrict_upTo_Ioc_zero T]
  rw [TimeMeasureRealBridge.integral_upTo_restrict_Ioc_eq_real f (a := 0) (b := T) (T := T) bot_le le_rfl]
  apply intervalIntegral.integral_congr_ae
  filter_upwards with t ht
  have ht0 : 0 ≤ t := (by simpa only [NNReal.coe_zero,uIcc_of_le T.coe_nonneg, mem_Icc] using uIoc_subset_uIcc ht :
    0 ≤ t ∧ t ≤ (T : ℝ)).1
  simp [TimeMeasureRealBridge.realZeroExtension,ht0]

private theorem continuous_compact_expectation_balance
    {Ω V : Type*} [MeasurableSpace Ω] [TopologicalSpace V] [CompactSpace V]
    [SecondCountableTopology V] [MeasurableSpace V] [BorelSpace V]
    (P : ProbabilityMeasure Ω) (Z : ℝ≥0 → Ω → V)
    (hZ : Measurable (Function.uncurry Z))
    (hPaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => Z t ω))
    (g : V → ℝ) (hg : Continuous g)
    (A : ℝ≥0 → V → ℝ) (hA : Continuous (Function.uncurry A))
    (hbalance : ∀ t : ℝ≥0, ∃ M : Ω → ℝ, Integrable M (P : Measure Ω) ∧
      (∫ ω, M ω ∂(P : Measure Ω)) = 0 ∧
      (∀ᵐ ω ∂(P : Measure Ω), g (Z t ω) - g (Z 0 ω) =
        (∫ v in (0 : ℝ)..(t : ℝ), A v.toNNReal (Z v.toNNReal ω)) + M ω)) :
    let φ := fun t : ℝ => ∫ ω, g (Z t.toNNReal ω) ∂(P : Measure Ω)
    let γ := fun t : ℝ => ∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)
    Continuous γ ∧ LocallyIntegrable γ volume ∧
      (∀ a b : ℝ≥0, φ b - φ a = ∫ t in (a : ℝ)..(b : ℝ), γ t) ∧
      (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval φ 0 (T : ℝ)) ∧
      (∀ t : ℝ, 0 < t → HasDerivAt φ (γ t) t) ∧
      HasDerivWithinAt φ (γ 0) (Ici 0) 0 := by
  intro φ γ
  let hSlice (t : ℝ≥0) : Measurable (Z t) := hZ.comp (measurable_const.prodMk measurable_id)
  let ρ (t : ℝ≥0) := P.map (hSlice t).aemeasurable
  have hρ : Continuous ρ :=
    WeakDiffusionLaw.continuous_marginal_law_of_ae_continuous P Z hSlice hPaths
  have hMap (t : ℝ≥0) (f : V → ℝ) (hf : Continuous f) :
      (∫ w, f w ∂(ρ t : Measure V)) = ∫ ω, f (Z t ω) ∂(P : Measure Ω) := by
    rw [ProbabilityMeasure.toMeasure_map]
    exact integral_map (hSlice t).aemeasurable hf.measurable.aestronglyMeasurable
  have hGc : Continuous γ := by
    have h := AutoSamplingTheory.TechnicalLemmas.Measure.WeakProbabilityIntegral.continuous_integral_of_compact hA hρ
    have hAc (t : ℝ≥0) : Continuous (A t) := hA.comp (continuous_const.prodMk continuous_id)
    simpa only [γ,hMap _ _ (hAc _),Function.comp_def] using h.comp continuous_real_toNNReal
  have hBound (T : ℝ≥0) : ∃ K : ℝ, ∀ t ≤ T, ∀ w, ‖A t w‖ ≤ K := by
    have hK : IsCompact (Icc (0 : ℝ≥0) T ×ˢ (univ : Set V)) := isCompact_Icc.prod isCompact_univ
    obtain ⟨K,hK⟩ := hK.bddAbove_image hA.norm.continuousOn
    exact ⟨K,fun t ht w => hK ⟨(t,w),⟨⟨bot_le,ht⟩,mem_univ w⟩,rfl⟩⟩
  have hweak := WeakMeasurableEvolution.marginal_balance_of_locally_bounded_generator
    P Z hZ g hg A hA.measurable hBound hbalance
  change LocallyIntegrable (fun t : ℝ => ∫ w, A t.toNNReal w ∂(ρ t.toNNReal : Measure V)) volume ∧
    (∀ a b : ℝ≥0, (∫ w, g w ∂(ρ (b : ℝ).toNNReal : Measure V)) -
      (∫ w, g w ∂(ρ (a : ℝ).toNNReal : Measure V)) =
      ∫ v in (a : ℝ)..(b : ℝ), ∫ w, A v.toNNReal w ∂(ρ v.toNNReal : Measure V)) ∧
    (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval
      (fun t : ℝ => ∫ w, g w ∂(ρ t.toNNReal : Measure V)) 0 (T : ℝ)) ∧ _ at hweak
  have hAc (t : ℝ≥0) : Continuous (A t) := hA.comp (continuous_const.prodMk continuous_id)
  simp only [hMap _ _ hg,hMap _ _ (hAc _)] at hweak
  obtain ⟨hLoc,hTwo,hAC,_⟩ := hweak
  refine ⟨hGc,hLoc,hTwo,hAC,?_,?_⟩
  · intro t ht
    have hp : HasDerivAt (fun u => ∫ v in t..u, γ v) (γ t) t :=
      intervalIntegral.integral_hasDerivAt_right (hGc.intervalIntegrable t t)
        hGc.stronglyMeasurable.stronglyMeasurableAtFilter hGc.continuousAt
    apply (hp.const_add (φ t)).congr_of_eventuallyEq
    filter_upwards [Ioi_mem_nhds ht] with u hu
    have h := hTwo t.toNNReal u.toNNReal
    rw [Real.coe_toNNReal t ht.le,Real.coe_toNNReal u hu.le] at h
    exact eq_add_of_sub_eq' h
  · have hp : HasDerivAt (fun u => ∫ v in (0 : ℝ)..u, γ v) (γ 0) 0 :=
      intervalIntegral.integral_hasDerivAt_right (hGc.intervalIntegrable 0 0)
        hGc.stronglyMeasurable.stronglyMeasurableAtFilter hGc.continuousAt
    apply ((hp.const_add (φ 0)).hasDerivWithinAt).congr_of_mem _ (show (0 : ℝ) ∈ Ici 0 from by simp)
    intro u hu
    have h := hTwo 0 u.toNNReal
    rw [Real.coe_toNNReal u hu] at h
    exact eq_add_of_sub_eq' h

private theorem integrable_compact_observable
    {Ω V : Type*} [MeasurableSpace Ω] [TopologicalSpace V] [CompactSpace V]
    [MeasurableSpace V] [BorelSpace V] {μ : Measure Ω} [IsFiniteMeasure μ]
    (g : V → ℝ) (hg : Continuous g) (Z : Ω → V) (hZ : Measurable Z) :
    Integrable (fun ω => g (Z ω)) μ := by
  let gb := BoundedContinuousFunction.mkOfCompact ⟨g,hg⟩
  exact Integrable.of_bound (hg.measurable.comp hZ).aestronglyMeasurable ‖gb‖
    (Filter.Eventually.of_forall fun ω => gb.norm_coe_le_norm (Z ω))

private theorem integrable_compact_time_observable
    {V : Type*} [TopologicalSpace V] [CompactSpace V] [MeasurableSpace V] [BorelSpace V]
    (Z : ℝ≥0 → V) (hZ : Measurable Z) (c : ℝ≥0 → V → ℝ)
    (hc : Continuous (Function.uncurry c)) (T : ℝ≥0) :
    Integrable (fun t => c t (Z t)) (TimeMeasure.upTo T) := by
  have hK : IsCompact (Icc (0 : ℝ≥0) T ×ˢ (univ : Set V)) := isCompact_Icc.prod isCompact_univ
  obtain ⟨K,hK⟩ := hK.bddAbove_image hc.norm.continuousOn
  have hm : Measurable (fun t => c t (Z t)) := hc.measurable.comp (measurable_id.prodMk hZ)
  apply Integrable.of_bound hm.aestronglyMeasurable K
  filter_upwards [TimeMeasure.ae_le_terminal T] with t ht
  exact hK ⟨(t,Z t),⟨⟨bot_le,ht⟩,mem_univ _⟩,rfl⟩

/-- The exact averaged squared-chord balance, with its actual fourth-moment term,
positive-time derivative, and derivative from the right at zero. -/
theorem synchronous_sphere_expected_chord_energy_balance
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    (P : ProbabilityMeasure Ω) (hN : 0 < N)
    (B : Fin N → ℝ≥0 → Ω → E)
    (hB : ∀ i, IsStandardBrownianMotionWithFiltration (B i) filtration (P : Measure Ω))
    (hUsual : SatisfiesUsualConditions filtration (P : Measure Ω))
    (X Y : Fin N → ℝ≥0 → Ω → S)
    (hX : ∀ i, Measurable (Function.uncurry (X i)))
    (hY : ∀ i, Measurable (Function.uncurry (Y i)))
    (hProgressiveX : ∀ i, IsStronglyProgressive filtration (X i))
    (hProgressiveY : ∀ i, IsStronglyProgressive filtration (Y i))
    (bX bY : ℝ≥0 → C → C → Fin N → E)
    (hbX : ∀ i, Continuous (fun z : ℝ≥0 × (C × C) => bX z.1 z.2.1 z.2.2 i))
    (hbY : ∀ i, Continuous (fun z : ℝ≥0 × (C × C) => bY z.1 z.2.1 z.2.2 i))
    (lambda : ℝ) (hlambda : 0 ≤ lambda)
    (hEquation : ∀ (T : ℝ≥0) (hT : 0 < T), ∀ᵐ ω ∂(P : Measure Ω),
      ∀ t ≤ T, ∀ (i : Fin N) (k : Fin d),
        ((X i t ω : E) k = (X i 0 ω : E) k +
          prefixIntegralProcess (fun v a =>
            (bX v (fun l => X l v a) (fun l => Y l v a) i) k -
              lambda * ((d : ℝ) - 1) * (X i v a : E) k) t ω +
          ∑ j : Fin d, itoIntegralProcess
            (sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (X i)
              (hX i) (hProgressiveX i) (fun _ => lambda) measurable_const
              ⟨‖lambda‖, fun _ _ => le_rfl⟩ k j)
            hT ((coordinateFamily (hB i)).isBrownian j) hUsual t ω) ∧
        ((Y i t ω : E) k = (Y i 0 ω : E) k +
          prefixIntegralProcess (fun v a =>
            (bY v (fun l => X l v a) (fun l => Y l v a) i) k -
              lambda * ((d : ℝ) - 1) * (Y i v a : E) k) t ω +
          ∑ j : Fin d, itoIntegralProcess
            (sphereMeasurableNoiseIntegrand (μ := (P : Measure Ω)) T (Y i)
              (hY i) (hProgressiveY i) (fun _ => lambda) measurable_const
              ⟨‖lambda‖, fun _ _ => le_rfl⟩ k j)
            hT ((coordinateFamily (hB i)).isBrownian j) hUsual t ω)) :
    let delta := fun (i : Fin N) (t : ℝ) (ω : Ω) =>
      (X i t.toNNReal ω : E) - (Y i t.toNNReal ω : E)
    let D := fun t : ℝ => (N : ℝ)⁻¹ * ∑ i : Fin N,
      ∫ ω, ‖delta i t ω‖ ^ 2 ∂(P : Measure Ω)
    let R4 := fun t : ℝ => (N : ℝ)⁻¹ * ∑ i : Fin N,
      ∫ ω, ‖delta i t ω‖ ^ 4 ∂(P : Measure Ω)
    let L := fun t : ℝ => 2 * (N : ℝ)⁻¹ * ∑ i : Fin N,
      ∫ ω, inner ℝ (delta i t ω)
        (bX t.toNNReal (fun l => X l t.toNNReal ω) (fun l => Y l t.toNNReal ω) i -
         bY t.toNNReal (fun l => X l t.toNNReal ω) (fun l => Y l t.toNNReal ω) i)
        ∂(P : Measure Ω)
    let G := fun t : ℝ => L t - 2 * lambda * ((d : ℝ) - 3) * D t - lambda * R4 t
    Continuous G ∧ LocallyIntegrable G volume ∧
      (∀ a b : ℝ≥0, D b - D a = ∫ t in (a : ℝ)..(b : ℝ), G t) ∧
      (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval D 0 (T : ℝ)) ∧
      (∀ t : ℝ, 0 < t → HasDerivAt D (G t) t) ∧
      HasDerivWithinAt D (G 0) (Ici 0) 0 := by
  classical
  intro delta D R4 L G
  let : CompactSpace S := isCompact_iff_compactSpace.mp (isCompact_sphere _ _)
  let Q := C × C
  let Z (t : ℝ≥0) (ω : Ω) : Q := (fun l => X l t ω,fun l => Y l t ω)
  have hZ : Measurable (Function.uncurry Z) :=
    (measurable_pi_lambda _ fun l => hX l).prodMk (measurable_pi_lambda _ fun l => hY l)
  have hSlice (t : ℝ≥0) : Measurable (Z t) := hZ.comp (measurable_const.prodMk measurable_id)
  have hParticle := source_particle_balance (d := d) (N := N) P hN B hB hUsual X Y hX hY
    hProgressiveX hProgressiveY bX bY hbX hbY lambda hlambda hEquation
  clear hEquation hB hUsual hProgressiveX hProgressiveY B
  have hPaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => Z t ω) := by
    apply continuous_paths_of_horizon
    intro T hT
    have h := ae_all_iff.mpr (fun i : Fin N => (hParticle T hT i).choose_spec.2.2.1)
    filter_upwards [h] with ω hω
    exact (continuousOn_pi.mpr fun i => (hω i).1).prodMk
      (continuousOn_pi.mpr fun i => (hω i).2)
  let δ (i : Fin N) (q : Q) : E := (q.1 i : E)-(q.2 i : E)
  have hδ (i : Fin N) : Continuous (δ i) := by dsimp [δ,Q]; fun_prop
  let e (i : Fin N) (q : Q) : ℝ := ‖δ i q‖^2
  let r (i : Fin N) (q : Q) : ℝ := ‖δ i q‖^4
  let a (i : Fin N) (t : ℝ≥0) (q : Q) : ℝ :=
    inner ℝ (δ i q) (bX t q.1 q.2 i-bY t q.1 q.2 i)
  have he (i : Fin N) : Continuous (e i) := (hδ i).norm.pow 2
  have hr (i : Fin N) : Continuous (r i) := (hδ i).norm.pow 4
  have ha (i : Fin N) : Continuous (Function.uncurry (a i)) :=
    ((hδ i).comp continuous_snd).inner ((hbX i).sub (hbY i))
  let c (i : Fin N) (t : ℝ≥0) (q : Q) :=
    2*a i t q-2*lambda*((d : ℝ)-3)*e i q-lambda*r i q
  have hc (i : Fin N) : Continuous (Function.uncurry (c i)) :=
    ((continuous_const.mul (ha i)).sub (continuous_const.mul ((he i).comp continuous_snd))).sub
      (continuous_const.mul ((hr i).comp continuous_snd))
  let g (q : Q) := (N : ℝ)⁻¹ * ∑ i : Fin N, e i q
  let A (t : ℝ≥0) (q : Q) := (N : ℝ)⁻¹ * ∑ i : Fin N, c i t q
  have hg : Continuous g := continuous_const.mul (continuous_finsetSum _ fun i _ => he i)
  have hA : Continuous (Function.uncurry A) :=
    continuous_const.mul (continuous_finsetSum _ fun i _ => hc i)
  have hcInt (T : ℝ≥0) (i : Fin N) (ω : Ω) :
      Integrable (fun t => c i t (Z t ω)) (TimeMeasure.upTo T) := by
    have hZω : Measurable (fun t : ℝ≥0 => Z t ω) :=
      hZ.comp (measurable_id.prodMk measurable_const)
    exact integrable_compact_time_observable (fun t => Z t ω) hZω (c i) (hc i) T
  have hbalance : ∀ T : ℝ≥0, ∃ M : Ω → ℝ, Integrable M (P : Measure Ω) ∧
      (∫ ω, M ω ∂(P : Measure Ω)) = 0 ∧
      (∀ᵐ ω ∂(P : Measure Ω), g (Z T ω)-g (Z 0 ω) =
        (∫ v in (0 : ℝ)..(T : ℝ), A v.toNNReal (Z v.toNNReal ω)) + M ω) := by
    intro T
    by_cases hT : T = 0
    · subst T
      exact ⟨fun _ => 0,integrable_zero _ _ _ ,by simp,Filter.Eventually.of_forall fun ω => by simp⟩
    have hTpos : 0 < T := lt_of_le_of_ne bot_le (Ne.symm hT)
    choose M hM hM0 hMp hMi using hParticle T hTpos
    have hMean (i : Fin N) : ∫ ω, M i T ω ∂(P : Measure Ω) = 0 := by
      have h := (hM i).setIntegral_eq (i := 0) (j := T) bot_le (s := univ) MeasurableSet.univ
      simpa only [setIntegral_univ,hM0 i,integral_zero] using h.symm
    let m (ω : Ω) := (N : ℝ)⁻¹ * ∑ i : Fin N, M i T ω
    refine ⟨m,(integrable_finsetSum _ fun i _ => (hM i).integrable T).const_mul _,?_,?_⟩
    · dsimp only [m]
      rw [integral_const_mul,integral_finsetSum _ (fun i _ => (hM i).integrable T)]
      simp only [hMean,Finset.sum_const_zero,mul_zero]
    · filter_upwards [ae_all_iff.mpr hMi] with ω hω
      calc
        g (Z T ω)-g (Z 0 ω) = (N : ℝ)⁻¹ * ∑ i : Fin N, (e i (Z T ω)-e i (Z 0 ω)) := by
          dsimp only [g]
          rw [Finset.sum_sub_distrib]
          ring
        _ = (N : ℝ)⁻¹ * ∑ i : Fin N,
            ((∫ t, c i t (Z t ω) ∂(TimeMeasure.upTo T))+M i T ω) := by
          congr 1
          apply Finset.sum_congr rfl
          intro i _
          exact hω i
        _ = (∫ t, A t (Z t ω) ∂(TimeMeasure.upTo T))+m ω := by
          dsimp only [A,m]
          rw [integral_const_mul,integral_finsetSum _ (fun i _ => hcInt T i ω),Finset.sum_add_distrib]
          ring
        _ = (∫ v in (0 : ℝ)..(T : ℝ), A v.toNNReal (Z v.toNNReal ω))+m ω := by
          rw [upTo_integral_real]
  have hAll := continuous_compact_expectation_balance P Z hZ hPaths g hg A hA hbalance
  have heI (i : Fin N) (t : ℝ≥0) : Integrable (fun ω => e i (Z t ω)) (P : Measure Ω) := by
    exact integrable_compact_observable (Ω := Ω) (V := Q) (μ := (P : Measure Ω))
      (e i) (he i) (Z t) (hSlice t)
  have hrI (i : Fin N) (t : ℝ≥0) : Integrable (fun ω => r i (Z t ω)) (P : Measure Ω) := by
    exact integrable_compact_observable (Ω := Ω) (V := Q) (μ := (P : Measure Ω))
      (r i) (hr i) (Z t) (hSlice t)
  have haI (i : Fin N) (t : ℝ≥0) : Integrable (fun ω => a i t (Z t ω)) (P : Measure Ω) := by
    exact integrable_compact_observable (Ω := Ω) (V := Q) (μ := (P : Measure Ω)) (a i t)
      ((ha i).comp (continuous_const.prodMk continuous_id)) (Z t) (hSlice t)
  have hcI (i : Fin N) (t : ℝ≥0) : Integrable (fun ω => c i t (Z t ω)) (P : Measure Ω) :=
    (((haI i t).const_mul 2).sub ((heI i t).const_mul _)).sub ((hrI i t).const_mul _)
  have hD (t : ℝ) : (∫ ω, g (Z t.toNNReal ω) ∂(P : Measure Ω)) = D t := by
    dsimp only [g,D]
    rw [integral_const_mul,integral_finsetSum _ (fun i _ => heI i t.toNNReal)]
  have hG (t : ℝ) : (∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) = G t := by
    have hci (i : Fin N) : (∫ ω, c i t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) =
        2*(∫ ω, a i t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) -
        2*lambda*((d : ℝ)-3)*(∫ ω, e i (Z t.toNNReal ω) ∂(P : Measure Ω)) -
        lambda*(∫ ω, r i (Z t.toNNReal ω) ∂(P : Measure Ω)) := by
      dsimp only [c]
      have hsplit := integral_sub
        (((haI i t.toNNReal).const_mul 2).sub ((heI i t.toNNReal).const_mul (2*lambda*((d : ℝ)-3))))
        ((hrI i t.toNNReal).const_mul lambda)
      simp only [Pi.sub_apply] at hsplit
      rw [hsplit, integral_sub ((haI i t.toNNReal).const_mul 2)
        ((heI i t.toNNReal).const_mul (2*lambda*((d : ℝ)-3)))]
      simp only [integral_const_mul]
    dsimp only [A]
    rw [integral_const_mul,integral_finsetSum _ (fun i _ => hcI i t.toNNReal)]
    rw [Finset.sum_congr rfl (fun i _ => hci i)]
    simp only [Finset.sum_sub_distrib,← Finset.mul_sum]
    dsimp only [G,L,D,R4,delta,a,e,r,δ,Z]
    ring
  have hDf := funext hD
  have hGf := funext hG
  change Continuous (fun t : ℝ => ∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) ∧
    LocallyIntegrable (fun t : ℝ => ∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) volume ∧
    (∀ a b : ℝ≥0, (∫ ω, g (Z (b : ℝ).toNNReal ω) ∂(P : Measure Ω)) -
      (∫ ω, g (Z (a : ℝ).toNNReal ω) ∂(P : Measure Ω)) =
      ∫ t in (a : ℝ)..(b : ℝ), ∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) ∧
    (∀ T : ℝ≥0, AbsolutelyContinuousOnInterval
      (fun t : ℝ => ∫ ω, g (Z t.toNNReal ω) ∂(P : Measure Ω)) 0 (T : ℝ)) ∧
    (∀ t : ℝ, 0 < t → HasDerivAt (fun t : ℝ => ∫ ω, g (Z t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, A t.toNNReal (Z t.toNNReal ω) ∂(P : Measure Ω)) t) ∧
    HasDerivWithinAt (fun t : ℝ => ∫ ω, g (Z t.toNNReal ω) ∂(P : Measure Ω))
      (∫ ω, A (0 : ℝ).toNNReal (Z (0 : ℝ).toNNReal ω) ∂(P : Measure Ω)) (Ici 0) 0 at hAll
  rw [hDf,hGf] at hAll
  refine ⟨hAll.1,hAll.2.1,?_,hAll.2.2.2.1,?_,?_⟩
  · intro a b
    have h := hAll.2.2.1 a b
    rw [hD,hD] at h
    exact h
  · intro t ht
    have h := hAll.2.2.2.2.1 t ht
    rw [hG] at h
    exact h
  · have h := hAll.2.2.2.2.2
    rw [hG] at h
    exact h

end SynchronousSphereCoupling

set_option pp.universes false
set_option pp.explicit false
set_option pp.fullNames false
set_option pp.fieldNotation true
set_option pp.notation true
set_option pp.proofs false

#check @SynchronousSphereCoupling.synchronous_sphere_expected_chord_energy_balance
#print axioms SynchronousSphereCoupling.synchronous_sphere_expected_chord_energy_balance
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsStandardBrownianMotion
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.projectedIncrementVariance
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsStandardBrownianMotionWithFiltration
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.BrownianMotion.IsBrownianMotionWithFiltration
#print ProbabilityTheory.IsBrownianReal
#print MeasureTheory.IsStronglyProgressive
#print MeasureTheory.StronglyAdapted
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.SatisfiesUsualConditions
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.ProgressiveL2Integrand
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.ProgressiveL2Integrand.toLp
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2.processFunction
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.FiniteDimensionalItoProcess.CoordinateBrownianFamilyWithFiltration
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.EuclideanBrownianCoordinates.coordinateFamily
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.SphereMeasurableCoordinateSDE.sphereMeasurableNoiseIntegrand
#print AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise.projectedNoiseColumn
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveDriftIntegral.prefixIntegralProcess
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.TimeMeasure.upTo
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.processTimeMeasure
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.ElementaryAdaptedProcess
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.ElementaryAdaptedProcess.value
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ElementaryItoIntegral.elementaryItoIntegral
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.itoIntegralProcess
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.canonicalPathLimit
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.uniformBadSet
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.uniformCauchyEvent
#print AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.canonicalItoProcess
#check @AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.itoIntegralProcess_at_zero
#check @AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.itoIntegralProcess_terminal_eq
#check @AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoIntegralProcess.itoIntegralProcess_martingale
#print Real.toNNReal
#print WithLp.toLp
namespace SynchronousSphereCoupling
#print block
#print difference
#print pair
end SynchronousSphereCoupling