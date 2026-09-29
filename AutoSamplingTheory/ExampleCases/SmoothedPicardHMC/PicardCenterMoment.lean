import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import Mathlib.Probability.Moments.Basic
import Mathlib.Tactic

/-!
# Second moments of the two Picard query layers

This is the explicit L2 bookkeeping suppressed in the proof of (D.7) in
Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Lemma D.4.  Starting from the
separate run-wide phase-state moment estimate, it constructs the actual stopped
approximate-proximal outputs at the first Picard layer and propagates moments
through the integrated interpolation weights to the second layer.

The theorem deliberately works on one arbitrary probability space carrying a
realized phase.  The Lean edge only needs measurable innovations satisfying
the standard Gaussian second-moment bound; Gaussianity and independence belong
to the later Algorithm 3.1 law.  Construction of that repeated kernel, the
run-wide state estimate and post-refresh adapter, the numerical parameter
substitutions, and total work (D.8) remain separate.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal RealInnerProductSpace

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardCenterMoment

private theorem norm_sub_sq_le_two (x y : E) [NormedAddCommGroup E] :
    ‖x - y‖ ^ 2 ≤ 2 * ‖x‖ ^ 2 + 2 * ‖y‖ ^ 2 := by
  have h := norm_sub_le x y
  have hs := (sq_le_sq₀ (norm_nonneg _) (by positivity)).2 h
  nlinarith [sq_nonneg (‖x‖ - ‖y‖)]

private theorem weighted_sum_norm_sq_le {ι E : Type*} [Fintype ι]
    [NormedAddCommGroup E] [NormedSpace ℝ E] (a : ι → ℝ) (z : ι → E) :
    ‖∑ j, a j • z j‖ ^ 2 ≤
      (∑ j, |a j|) * ∑ j, |a j| * ‖z j‖ ^ 2 := by
  have hn : ‖∑ j, a j • z j‖ ≤ ∑ j, |a j| * ‖z j‖ := by
    calc
      ‖∑ j, a j • z j‖ ≤ ∑ j, ‖a j • z j‖ := norm_sum_le _ _
      _ = ∑ j, |a j| * ‖z j‖ := by simp only [norm_smul, Real.norm_eq_abs]
  have hcs := Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul (Finset.univ)
    (r := fun j => |a j| * ‖z j‖) (f := fun j => |a j|)
    (g := fun j => |a j| * ‖z j‖ ^ 2)
    (fun _ _ => abs_nonneg _) (fun _ _ => mul_nonneg (abs_nonneg _) (sq_nonneg _))
    (fun j _ => by rw [mul_pow]; nlinarith [abs_nonneg (a j), sq_nonneg ‖z j‖])
  exact (sq_le_sq₀ (norm_nonneg _) (Finset.sum_nonneg fun _ _ =>
    mul_nonneg (abs_nonneg _) (norm_nonneg _))).2 hn |>.trans hcs

section

variable {E Ω ι : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [MeasurableSpace Ω] [Fintype ι]

/-- The actual stopped approximate-proximal program, followed by one finite
Picard weighted update, gives explicit square-integrability bounds for the
gradients at both query layers.  Center moments are proved internally.  The
hypotheses `hstate` and `hnoise` are the separate post-refresh state and
innovation-moment inputs in the source proof. -/
theorem picard_center_gradient_moment {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X P : Ω → E) (hX : Measurable X) (hP : Measurable P)
    (xstar : E) (hstar : gradient V xstar = 0)
    (t : ι → ℝ) (ht : ∀ i, |t i| ≤ 1)
    (G : ι → Ω → E) (hG : ∀ j, Measurable (G j))
    (omega : ι → ι → ℝ) {M S : ℝ} (hM : 0 ≤ M) (hS : 0 ≤ S)
    (hstateI : Integrable (fun w => ‖X w - xstar‖ ^ 2 + ‖P w‖ ^ 2) μ)
    (hstate : MeasureTheory.integral μ
      (fun w => ‖X w - xstar‖ ^ 2 + ‖P w‖ ^ 2) ≤ M)
    (hnoiseI : ∀ j, Integrable (fun w => ‖G j w‖ ^ 2) μ)
    (hnoise : ∀ j, MeasureTheory.integral μ (fun w => ‖G j w‖ ^ 2) ≤
      (Module.finrank ℝ E : ℝ))
    (hrow : ∀ i, (∑ j, |omega i j|) ≤ S) :
    let Y0 := fun i w => X w + t i • P w
    let B := 6 * M + 3 * eps ^ 2 + 3 * eta * (Module.finrank ℝ E : ℝ)
    ∃ p : E → E, ∃ N : E → ℕ, ∃ q : E → E,
      Measurable p ∧ Measurable N ∧ Measurable q ∧
      (∀ y, p y + eta • gradient V (p y) = y) ∧
      (∀ y, ‖q y - p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y + 1) y =
          some (q y, N y + 1)) ∧
      let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • G j w)
      let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
      (∀ i, Integrable (fun w => ‖gradient V (Y0 i w)‖ ^ 2) μ ∧
        MeasureTheory.integral μ (fun w => ‖gradient V (Y0 i w)‖ ^ 2) ≤ 2 * M) ∧
      (∀ j, Integrable (fun w => ‖Z0 j w‖ ^ 2) μ ∧
        MeasureTheory.integral μ (fun w => ‖Z0 j w‖ ^ 2) ≤ B) ∧
      (∀ i, Integrable (fun w => ‖gradient V (Y1 i w)‖ ^ 2) μ ∧
        MeasureTheory.integral μ (fun w => ‖gradient V (Y1 i w)‖ ^ 2) ≤
          4 * M + 2 * S ^ 2 * B) := by
  classical
  dsimp only
  obtain ⟨p, N, hp, hN, hq, hall⟩ :=
    ApproximateProximalExecution.approximate_proximal_execution
      hκ hV hH heta hec hc heps
  let q := fun y => (fun x : E => y - eta • gradient V x)^[N y] y
  have hq' : Measurable q := by simpa only [q] using hq
  have hH' : ∀ x v : E, ((κ⁻¹ : ℝ≥0) : ℝ) * ‖v‖ ^ 2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (1 : ℝ≥0) * ‖v‖ ^ 2 := by
    simpa only [NNReal.coe_inv, NNReal.coe_one, one_mul] using hH
  have hreg :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := 0) hV hH' (0 : E)
  have hLip : LipschitzWith 1 (gradient V) := by simpa using hreg.2
  have hsc : StrongConvexOn Set.univ ((κ : ℝ)⁻¹) V := by simpa using hreg.1
  have hmono (x y : E) : 0 ≤ inner ℝ (gradient V x - gradient V y) (x - y) := by
    have hb :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
        hsc (fun z _ => (hV.differentiable (by norm_num) z).hasGradientAt)
        (x := y) (y := x) (Set.mem_univ _) (Set.mem_univ _)
    exact (mul_nonneg (inv_nonneg.mpr (NNReal.coe_nonneg κ)) (sq_nonneg _)).trans hb
  have hpLip : LipschitzWith 1 p := by
    apply LipschitzWith.of_dist_le_mul
    intro y z
    simp only [NNReal.coe_one, one_mul, dist_eq_norm]
    have he : y - z = (p y - p z) + eta • (gradient V (p y) - gradient V (p z)) := by
      calc
        y - z = (p y + eta • gradient V (p y)) -
            (p z + eta • gradient V (p z)) :=
          congrArg₂ (fun a b : E => a - b) (hall y).1.symm (hall z).1.symm
        _ = _ := by module
    have hpair : ‖p y - p z‖ ^ 2 ≤ inner ℝ (y - z) (p y - p z) := by
      calc
        _ ≤ ‖p y - p z‖ ^ 2 +
            eta * inner ℝ (gradient V (p y) - gradient V (p z)) (p y - p z) :=
          le_add_of_nonneg_right (mul_nonneg heta.le (hmono (p y) (p z)))
        _ = inner ℝ (y - z) (p y - p z) := by
          conv_rhs => rw [he]
          rw [inner_add_left, real_inner_smul_left, real_inner_self_eq_norm_sq]
    have hb := hpair.trans (real_inner_le_norm (y - z) (p y - p z))
    by_cases hz : ‖p y - p z‖ = 0
    · simpa only [hz] using norm_nonneg (y - z)
    · have hp : 0 < ‖p y - p z‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
      nlinarith
  have hpstar : p xstar = xstar := by
    have he := (hall xstar).1
    have hm := hmono (p xstar) xstar
    have hEq : p xstar - xstar = -eta • (gradient V (p xstar) - gradient V xstar) := by
      calc
        p xstar - xstar = p xstar - (p xstar + eta • gradient V (p xstar)) :=
          congrArg (fun z => p xstar - z) he.symm
        _ = -eta • (gradient V (p xstar) - gradient V xstar) := by
          rw [hstar, sub_zero]
          module
    have hsq : ‖p xstar - xstar‖ ^ 2 =
        -eta * inner ℝ (gradient V (p xstar) - gradient V xstar)
          (p xstar - xstar) := by
      calc
        _ = inner ℝ (p xstar - xstar) (p xstar - xstar) :=
          (real_inner_self_eq_norm_sq _).symm
        _ = inner ℝ (-eta • (gradient V (p xstar) - gradient V xstar))
            (p xstar - xstar) := by rw [hEq]
        _ = _ := by rw [real_inner_smul_left]
    have hz : ‖p xstar - xstar‖ = 0 := by
      have hle : ‖p xstar - xstar‖ ^ 2 ≤ 0 := by rw [hsq]; exact mul_nonpos_of_nonpos_of_nonneg (by linarith) hm
      nlinarith [sq_nonneg ‖p xstar - xstar‖]
    exact sub_eq_zero.mp (norm_eq_zero.mp hz)
  have hgrad (y : E) : ‖gradient V y‖ ≤ ‖y - xstar‖ := by
    have hh := hLip.dist_le_mul y xstar
    simpa only [hstar, sub_zero, NNReal.coe_one, one_mul, dist_eq_norm] using hh
  let Y0 := fun i w => X w + t i • P w
  have hY0m (i) : Measurable (Y0 i) := hX.add (hP.const_smul (t i))
  have hY0bound (i w) : ‖Y0 i w - xstar‖ ^ 2 ≤
      2 * (‖X w - xstar‖ ^ 2 + ‖P w‖ ^ 2) := by
    have he : Y0 i w - xstar = (X w - xstar) + t i • P w := by dsimp [Y0]; module
    rw [he]
    have hn := norm_add_le (X w - xstar) (t i • P w)
    rw [norm_smul, Real.norm_eq_abs] at hn
    have hti := ht i
    have hmul : |t i| * ‖P w‖ ≤ ‖P w‖ := by
      simpa only [one_mul] using mul_le_mul_of_nonneg_right hti (norm_nonneg _)
    have hn' : ‖X w - xstar + t i • P w‖ ≤ ‖X w - xstar‖ + ‖P w‖ :=
      hn.trans (add_le_add_right hmul _)
    have hnsq := (sq_le_sq₀ (norm_nonneg _) (by positivity)).2 hn'
    nlinarith [norm_nonneg (X w - xstar), norm_nonneg (P w),
      sq_nonneg (‖X w - xstar‖ - ‖P w‖)]
  have hY0I (i) : Integrable (fun w => ‖Y0 i w - xstar‖ ^ 2) μ := by
    apply (hstateI.const_mul 2).mono'
      (((hY0m i).sub measurable_const).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact hY0bound i w
  have hY0int (i) : MeasureTheory.integral μ
      (fun w => ‖Y0 i w - xstar‖ ^ 2) ≤ 2 * M := by
    calc
      _ ≤ MeasureTheory.integral μ
          (fun w => 2 * (‖X w - xstar‖ ^ 2 + ‖P w‖ ^ 2)) :=
        integral_mono (hY0I i) (hstateI.const_mul 2) (hY0bound i)
      _ = 2 * MeasureTheory.integral μ
          (fun w => ‖X w - xstar‖ ^ 2 + ‖P w‖ ^ 2) := integral_const_mul 2 _
      _ ≤ 2 * M := mul_le_mul_of_nonneg_left hstate (by norm_num)
  have hgradI (i) : Integrable (fun w => ‖gradient V (Y0 i w)‖ ^ 2) μ := by
    apply (hY0I i).mono'
      ((hLip.continuous.measurable.comp (hY0m i)).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 (hgrad _)
  have hgradInt (i) : MeasureTheory.integral μ
      (fun w => ‖gradient V (Y0 i w)‖ ^ 2) ≤ 2 * M := by
    exact (integral_mono (hgradI i) (hY0I i) fun w =>
      (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 (hgrad _)).trans (hY0int i)
  let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • G j w)
  have hZ0m (j) : Measurable (Z0 j) := hLip.continuous.measurable.comp
    ((hq'.comp (hY0m j)).add ((hG j).const_smul (Real.sqrt eta)))
  have hqcenter (y : E) : ‖q y - xstar‖ ≤ ‖y - xstar‖ + eps := by
    calc
      ‖q y - xstar‖ ≤ ‖q y - p y‖ + ‖p y - xstar‖ := by
        simpa only [sub_add_sub_cancel] using norm_add_le (q y - p y) (p y - xstar)
      _ ≤ eps + ‖p y - p xstar‖ := by rw [hpstar]; gcongr; exact (hall y).2.2.2.2.1
      _ ≤ eps + ‖y - xstar‖ := by
        gcongr
        simpa only [NNReal.coe_one, one_mul, dist_eq_norm] using hpLip.dist_le_mul y xstar
      _ = ‖y - xstar‖ + eps := add_comm _ _
  have hZbound (j w) : ‖Z0 j w‖ ^ 2 ≤
      3 * (‖Y0 j w - xstar‖ ^ 2 + eps ^ 2 + eta * ‖G j w‖ ^ 2) := by
    have hg0 := hgrad (q (Y0 j w) + Real.sqrt eta • G j w)
    have he : q (Y0 j w) + Real.sqrt eta • G j w - xstar =
        (q (Y0 j w) - xstar) + Real.sqrt eta • G j w := by abel
    have htri : ‖q (Y0 j w) + Real.sqrt eta • G j w - xstar‖ ≤
        ‖Y0 j w - xstar‖ + eps + Real.sqrt eta * ‖G j w‖ := by
      calc
        _ ≤ ‖q (Y0 j w) - xstar‖ + ‖Real.sqrt eta • G j w‖ := by
          rw [he]
          exact norm_add_le _ _
        _ ≤ (‖Y0 j w - xstar‖ + eps) + Real.sqrt eta * ‖G j w‖ := by
          rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg (Real.sqrt_nonneg eta)]
          gcongr
          exact hqcenter (Y0 j w)
    have hsqrt := Real.sq_sqrt heta.le
    have hsq : (‖Y0 j w - xstar‖ + eps + Real.sqrt eta * ‖G j w‖) ^ 2 ≤
        3 * (‖Y0 j w - xstar‖ ^ 2 + eps ^ 2 + eta * ‖G j w‖ ^ 2) := by
      nlinarith [norm_nonneg (Y0 j w - xstar), norm_nonneg (G j w),
        Real.sqrt_nonneg eta, sq_nonneg (‖Y0 j w - xstar‖ - eps),
        sq_nonneg (‖Y0 j w - xstar‖ - Real.sqrt eta * ‖G j w‖),
        sq_nonneg (eps - Real.sqrt eta * ‖G j w‖)]
    exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 hg0 |>.trans
      ((sq_le_sq₀ (norm_nonneg _) (by positivity)).2 htri |>.trans hsq)
  let B := 6 * M + 3 * eps ^ 2 + 3 * eta * Module.finrank ℝ E
  have hB : 0 ≤ B := by positivity
  have hZdomI (j) : Integrable (fun w =>
      3 * (‖Y0 j w - xstar‖ ^ 2 + eps ^ 2 + eta * ‖G j w‖ ^ 2)) μ := by
    exact (((hY0I j).add (integrable_const (eps ^ 2))).add
      ((hnoiseI j).const_mul eta)).const_mul 3
  have hZI (j) : Integrable (fun w => ‖Z0 j w‖ ^ 2) μ := by
    apply (hZdomI j).mono' ((hZ0m j).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact hZbound j w
  have hZint (j) : MeasureTheory.integral μ (fun w => ‖Z0 j w‖ ^ 2) ≤ B := by
    have houter := integral_add ((hY0I j).add (integrable_const (eps ^ 2)))
      ((hnoiseI j).const_mul eta)
    have hinner := integral_add (hY0I j) (integrable_const (eps ^ 2))
    calc
      _ ≤ MeasureTheory.integral μ (fun w =>
          3 * (‖Y0 j w - xstar‖ ^ 2 + eps ^ 2 + eta * ‖G j w‖ ^ 2)) :=
        integral_mono (hZI j) (hZdomI j) (hZbound j)
      _ = 3 * (MeasureTheory.integral μ (fun w => ‖Y0 j w - xstar‖ ^ 2) + eps ^ 2 +
          eta * MeasureTheory.integral μ (fun w => ‖G j w‖ ^ 2)) := by
        rw [integral_const_mul 3]
        have ho : MeasureTheory.integral μ (fun w =>
            (‖Y0 j w - xstar‖ ^ 2 + eps ^ 2) + eta * ‖G j w‖ ^ 2) =
            MeasureTheory.integral μ (fun w => ‖Y0 j w - xstar‖ ^ 2 + eps ^ 2) +
              MeasureTheory.integral μ (fun w => eta * ‖G j w‖ ^ 2) := by
          simpa only [Pi.add_apply] using houter
        rw [ho]
        have hi : MeasureTheory.integral μ (fun w => ‖Y0 j w - xstar‖ ^ 2 + eps ^ 2) =
            MeasureTheory.integral μ (fun w => ‖Y0 j w - xstar‖ ^ 2) +
              MeasureTheory.integral μ (fun _w => eps ^ 2) := by
          simpa only [Pi.add_apply] using hinner
        rw [hi, integral_const, probReal_univ, smul_eq_mul, one_mul, integral_const_mul]
      _ ≤ B := by dsimp [B]; nlinarith [hY0int j, hnoise j]
  let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
  have hsumM (i) : Measurable (fun w => ∑ j, omega i j • Z0 j w) := by fun_prop
  have hY1m (i) : Measurable (Y1 i) := (hY0m i).sub (hsumM i)
  have hweighted (i w) : ‖∑ j, omega i j • Z0 j w‖ ^ 2 ≤
      S * ∑ j, |omega i j| * ‖Z0 j w‖ ^ 2 := by
    calc
      _ ≤ (∑ j, |omega i j|) * ∑ j, |omega i j| * ‖Z0 j w‖ ^ 2 :=
        weighted_sum_norm_sq_le (omega i) (fun j => Z0 j w)
      _ ≤ S * ∑ j, |omega i j| * ‖Z0 j w‖ ^ 2 := by
        gcongr
        exact hrow i
  have hsumSqI (i) : Integrable (fun w => ‖∑ j, omega i j • Z0 j w‖ ^ 2) μ := by
    have hi : Integrable (fun w => S * ∑ j, |omega i j| * ‖Z0 j w‖ ^ 2) μ :=
      (integrable_finsetSum Finset.univ fun j _ => (hZI j).const_mul |omega i j|).const_mul S
    apply hi.mono' ((hsumM i).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact hweighted i w
  have hsumInt (i) : MeasureTheory.integral μ
      (fun w => ‖∑ j, omega i j • Z0 j w‖ ^ 2) ≤ S ^ 2 * B := by
    calc
      _ ≤ MeasureTheory.integral μ
          (fun w => S * ∑ j, |omega i j| * ‖Z0 j w‖ ^ 2) :=
        integral_mono (hsumSqI i)
          ((integrable_finsetSum Finset.univ fun j _ => (hZI j).const_mul |omega i j|).const_mul S)
          (hweighted i)
      _ = S * ∑ j, |omega i j| *
          MeasureTheory.integral μ (fun w => ‖Z0 j w‖ ^ 2) := by
        rw [integral_const_mul, integral_finsetSum]
        · simp_rw [integral_const_mul]
        · intro j _; exact (hZI j).const_mul _
      _ ≤ S * ∑ j, |omega i j| * B := by
        gcongr with j
        exact hZint j
      _ ≤ S ^ 2 * B := by
        calc
          S * ∑ j, |omega i j| * B = S * ((∑ j, |omega i j|) * B) := by
            rw [Finset.sum_mul]
          _ ≤ S * (S * B) := by gcongr; exact hrow i
          _ = S ^ 2 * B := by ring
  have hY1I (i) : Integrable (fun w => ‖Y1 i w - xstar‖ ^ 2) μ := by
    have hi := ((hY0I i).const_mul 2).add ((hsumSqI i).const_mul 2)
    apply hi.mono'
      (((hY1m i).sub measurable_const).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    have he : Y1 i w - xstar = (Y0 i w - xstar) - ∑ j, omega i j • Z0 j w := by
      dsimp [Y1]; module
    change |‖Y1 i w - xstar‖ ^ 2| ≤
      2 * ‖Y0 i w - xstar‖ ^ 2 + 2 * ‖∑ j, omega i j • Z0 j w‖ ^ 2
    rw [abs_of_nonneg (sq_nonneg _), he]
    exact norm_sub_sq_le_two _ _
  have hY1int (i) : MeasureTheory.integral μ
      (fun w => ‖Y1 i w - xstar‖ ^ 2) ≤ 4 * M + 2 * S ^ 2 * B := by
    calc
      _ ≤ MeasureTheory.integral μ (fun w => 2 * ‖Y0 i w - xstar‖ ^ 2 +
          2 * ‖∑ j, omega i j • Z0 j w‖ ^ 2) := by
        apply integral_mono (hY1I i) (((hY0I i).const_mul 2).add ((hsumSqI i).const_mul 2))
        intro w
        have he : Y1 i w - xstar = (Y0 i w - xstar) - ∑ j, omega i j • Z0 j w := by
          dsimp [Y1]; module
        simpa only [Pi.add_apply, he] using
          norm_sub_sq_le_two (Y0 i w - xstar) (∑ j, omega i j • Z0 j w)
      _ = 2 * MeasureTheory.integral μ (fun w => ‖Y0 i w - xstar‖ ^ 2) +
          2 * MeasureTheory.integral μ (fun w => ‖∑ j, omega i j • Z0 j w‖ ^ 2) := by
        rw [integral_add, integral_const_mul, integral_const_mul]
        exacts [(hY0I i).const_mul 2, (hsumSqI i).const_mul 2]
      _ ≤ 4 * M + 2 * S ^ 2 * B := by nlinarith [hY0int i, hsumInt i]
  have hgrad1I (i) : Integrable (fun w => ‖gradient V (Y1 i w)‖ ^ 2) μ := by
    apply (hY1I i).mono'
      ((hLip.continuous.measurable.comp (hY1m i)).norm.pow_const 2).aestronglyMeasurable
    filter_upwards with w
    rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
    exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 (hgrad _)
  refine ⟨p, N, q, hp, hN, hq', fun y => (hall y).1, ?_, ?_, ?_, ?_⟩
  · intro y
    exact ⟨by simpa only [q] using (hall y).2.2.2.2.1,
      by simpa only [q] using (hall y).2.2.2.2.2.2⟩
  · exact fun i => ⟨hgradI i, hgradInt i⟩
  · exact fun j => ⟨hZI j, hZint j⟩
  · intro i
    refine ⟨hgrad1I i, ?_⟩
    exact (integral_mono (hgrad1I i) (hY1I i) fun w =>
      (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 (hgrad _)).trans (hY1int i)

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.PicardCenterMoment
