import GC44WeightedChiSquare
import GC44GramUse
import GC41Asymptotic

open MeasureTheory ProbabilityTheory Real Matrix
open scoped BigOperators Matrix.Norms.L2Operator RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.WeightedChiSquare
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- The small matrix that results from testing the Gaussian rows with fixed weights. -/
def weightedRowMatrix {d q : ℕ} (g : Starts d q) (w : Fin d → ℝ) : Matrix (Fin (q+1)) (Fin (q+1)) ℝ :=
  ∑ j, w j • (Matrix.vecMulVec (fun a => g a j) (fun a => g a j) - 1)

theorem weightedRowMatrix_hermitian {d q : ℕ} (g : Starts d q) (w : Fin d → ℝ) :
    (weightedRowMatrix g w).IsHermitian := by
  apply Matrix.IsHermitian.ext
  intro i j
  simp only [weightedRowMatrix, Matrix.sum_apply, Matrix.smul_apply, Matrix.sub_apply,
    Matrix.vecMulVec_apply, Matrix.one_apply, star_trivial]
  apply Finset.sum_congr rfl
  intro k _
  by_cases h : i = j
  · subst j; rfl
  · simp [h,Ne.symm h,mul_comm]

private theorem row_form {d q : ℕ} (g : Starts d q) (w : Fin d → ℝ)
    (z : Space (q+1)) (hz : ‖z‖ = 1) :
    WithLp.ofLp z ⬝ᵥ (weightedRowMatrix g w *ᵥ WithLp.ofLp z) =
      ∑ j, w j *((inner ℝ z (WithLp.toLp 2 (fun a => g a j)))^2-1) := by
  have hz' : WithLp.ofLp z ⬝ᵥ WithLp.ofLp z = 1 := by
    have h := real_inner_self_eq_norm_sq z
    rw [hz, one_pow] at h
    simpa only [PiLp.inner_apply, Real.inner_apply, dotProduct] using h
  simp only [weightedRowMatrix, Matrix.sum_mulVec, dotProduct_sum, Matrix.smul_mulVec,
    dotProduct_smul, smul_eq_mul, Matrix.sub_mulVec, dotProduct_sub, Matrix.one_mulVec, hz',
    Matrix.vecMulVec_mulVec]
  apply Finset.sum_congr rfl
  intro j _
  simp only [PiLp.inner_apply, Real.inner_apply, dotProduct, op_smul_eq_mul]
  simp_rw [mul_comm (WithLp.ofLp z _) (g _ _)]
  ring

private theorem net_count {d r k : ℕ} (hd : 2 ≤ d) (hr : 0 < r) (hrd : r < d)
    (hk : k ≤ (32*r+1)^r) : 800*d*k ≤ d^(20*r) := by
  have h32 : 32 ≤ d^5 := (by decide : 32 ≤ 2^5) |>.trans (Nat.pow_le_pow_left hd 5)
  have hbase : 32*r+1 ≤ d^6 := by
    rw [show (6:ℕ)=5+1 by decide, pow_succ]
    exact (show 32*r+1 ≤ 32*d by omega).trans (Nat.mul_le_mul_right _ h32)
  have he : k ≤ d^(6*r) := hk.trans (by rw [pow_mul]; exact Nat.pow_le_pow_left hbase r)
  have hc : 800 ≤ d^10 := (by decide : 800 ≤ 2^10) |>.trans (Nat.pow_le_pow_left hd 10)
  calc
    _ ≤ d^10*d*d^(6*r) := Nat.mul_le_mul (Nat.mul_le_mul_right d hc) he
    _ = d^(10+1+6*r) := by rw [pow_add, pow_succ d 10]
    _ ≤ _ := Nat.pow_le_pow_right (by omega) (by omega)

private theorem kernel_radius {d q : ℕ} (hd : 2 ≤ d) :
    let r := (q : ℝ)+1
    let v := 2*(2*(q : ℝ)+1)/(d : ℝ)
    let u := 20*r*Real.log (d : ℝ)
    2*(4*Real.sqrt (v*u)+8*v*u) ≤ queryThreshold 2048 d q := by
  let r := (q : ℝ)+1
  let a := Real.log (d : ℝ)/(d : ℝ)
  have hd1 : 1 ≤ (d:ℝ) := by exact_mod_cast (show 1 ≤ d by omega)
  have hdp : 0 < (d : ℝ) := by linarith
  have hl : 0 ≤ Real.log (d : ℝ) := Real.log_nonneg hd1
  have ha : 0 ≤ a := div_nonneg hl hdp.le
  have hr : 0 ≤ r := by dsimp [r]; positivity
  let v := 2*(2*(q : ℝ)+1)/(d : ℝ)
  let u := 20*r*Real.log (d : ℝ)
  have hprod : v*u ≤ 80*r^2*a := by
    have h := mul_le_mul_of_nonneg_right
      (show 2*(2*(q : ℝ)+1) ≤ 4*r by dsimp [r]; linarith) (show 0 ≤ u by dsimp [u]; positivity)
    calc
      _ = (2*(2*(q : ℝ)+1)*u)/(d : ℝ) := by dsimp [v]; ring
      _ ≤ (4*r*u)/(d : ℝ) := div_le_div_of_nonneg_right h hdp.le
      _ = _ := by dsimp [u,a]; ring
  have hs : Real.sqrt (v*u) ≤ 9*r*Real.sqrt a := by
    apply Real.sqrt_le_iff.mpr ⟨by positivity, ?_⟩
    rw [mul_pow, Real.sq_sqrt ha]
    nlinarith [mul_nonneg (sq_nonneg r) ha]
  have hn : 0 ≤ r * Real.log (d : ℝ) ^ 2 / (d : ℝ) := by positivity
  change 2*(4*Real.sqrt (v*u)+8*v*u) ≤
    2048*(r*Real.sqrt a + (r*(r+Real.log (d : ℝ))*Real.log (d : ℝ))/(d : ℝ))
  have he : (r*(r+Real.log (d : ℝ))*Real.log (d : ℝ))/(d : ℝ) =
      r^2*a + r*Real.log (d : ℝ)^2/(d : ℝ) := by dsimp [a]; ring
  rw [he]
  nlinarith only [hs, hprod, hn, mul_nonneg hr (Real.sqrt_nonneg a), mul_nonneg (sq_nonneg r) ha]

/-- A finite family of signed weights and unit directions, tested on the same draw
of all starts. The cardinality accounts for both weights at every grid point. -/
theorem finite_symbol_tests {d q : ℕ} (hq : 2*q+1 < d) (S : Finset (Space (q+1)))
    (hunit : ∀ z ∈ S, ‖z‖ = 1) (hcard : S.card ≤ (32*(q+1)+1)^(q+1))
    (w : Bool → Fin d → Fin d → ℝ)
    (hw : ∀ b i, (∀ j, |w b i j| ≤ 2*(2*(q : ℝ)+1)/(d : ℝ)) ∧
      ∑ j, (w b i j)^2 ≤ 2*(2*(q : ℝ)+1)/(d : ℝ)) :
    let μ := Measure.pi (fun _ : Fin (q+1) => stdGaussian (Space d))
    (199/200 : ℝ) ≤ μ.real {g : Starts d q | ∀ b i, ∀ z ∈ S,
      |WithLp.ofLp z ⬝ᵥ (weightedRowMatrix g (w b i) *ᵥ WithLp.ofLp z)| ≤
        queryThreshold 2048 d q / 2} := by
  classical
  let μ := Measure.pi (fun _ : Fin (q+1) => stdGaussian (Space d))
  have : IsProbabilityMeasure μ := by dsimp [μ]; infer_instance
  let r := q+1
  let v := 2*(2*(q : ℝ)+1)/(d : ℝ)
  let u := 20*(r : ℝ)*Real.log (d : ℝ)
  let T := 4*Real.sqrt (v*u)+8*v*u
  let J := Bool × Fin d × ↥S
  let bad (k : J) := {g : Starts d q | T ≤
    |∑ j : Fin d, w k.1 k.2.1 j *
      ((inner ℝ k.2.2.val (WithLp.toLp 2 (fun a => g a j)))^2-1)|}
  have hd : 2 ≤ d := by omega
  have hdp : 1 < (d:ℝ) := by exact_mod_cast (show 1 < d by omega)
  have hr : 0 < r := Nat.succ_pos _
  have hv : 0 < v := by dsimp [v]; positivity
  have hu : 0 < u := by dsimp [u]; exact mul_pos (by positivity) (Real.log_pos hdp)
  have hsum : μ.real (⋃ k : J, bad k) ≤ 1/200 := by
    have hp (k : J) : μ.real (bad k) ≤ 2*exp (-u) := projected_source_row_tail hq
      k.2.2.val (hunit _ k.2.2.property) _ hv hv hu (hw k.1 k.2.1).2 (hw k.1 k.2.1).1
    have hn := net_count hd hr (show r < d by dsimp [r]; omega) hcard
    have hcard' : Fintype.card J = 2*d*S.card := by simp [J, Nat.mul_assoc]
    have hep : exp (-u) = ((d : ℝ)^(20*r))⁻¹ := by
      rw [Real.exp_neg, ← Real.exp_log (by positivity : 0 < (d : ℝ)^(20*r))]
      congr 2
      dsimp [u]
      rw [Real.log_pow]
      push_cast
      ring
    calc
      _ ≤ ∑ k : J, μ.real (bad k) := measureReal_iUnion_fintype_le bad
      _ ≤ ∑ _ : J, 2*exp (-u) := Finset.sum_le_sum (fun k _ => hp k)
      _ = (2*d*S.card : ℕ)*(2*((d : ℝ)^(20*r))⁻¹) := by
        simp [hep,hcard']
      _ ≤ _ := by
        push_cast
        rw [show (2*(d:ℝ)*(S.card : ℝ))*(2*((d : ℝ)^(20*r))⁻¹) =
          (4*d*S.card)/((d : ℝ)^(20*r)) by ring]
        apply (div_le_iff₀ (by positivity)).mpr
        have hh : (800:ℝ)*d*S.card ≤ (d : ℝ)^(20*r) := by exact_mod_cast hn
        linarith
  have hm (k : J) : MeasurableSet (bad k) := by
    have hc (j : Fin d) : Continuous (fun g : Starts d q =>
      inner ℝ k.2.2.val (WithLp.toLp 2 (fun a => g a j))) := by
      apply Continuous.inner continuous_const
      apply (PiLp.continuous_toLp 2 _).comp
      exact continuous_pi fun a => (EuclideanSpace.proj j).continuous.comp (continuous_apply a)
    exact measurableSet_le measurable_const ((Finset.measurable_sum _ (fun j _ =>
      (((hc j).measurable.pow_const 2).sub_const 1).const_mul _)).abs)
  have hτ : 2*T ≤ queryThreshold 2048 d q := by
    simpa only [T,v,u,r,Nat.cast_add,Nat.cast_one] using (kernel_radius (q := q) hd)
  refine le_trans ?_ (measureReal_mono (μ := μ) (s₁ := (⋃ k : J, bad k)ᶜ) ?_ (measure_ne_top _ _))
  · rw [probReal_compl_eq_one_sub (MeasurableSet.iUnion hm)]
    linarith
  · intro g hg b i z hz
    have hn : g ∉ bad (b,i,⟨z,hz⟩) := fun h => hg (Set.mem_iUnion.mpr ⟨_,h⟩)
    rw [row_form _ _ _ (hunit z hz)]
    change ¬ T ≤ |∑ j : Fin d, w b i j * ((inner ℝ z (WithLp.toLp 2 (fun a => g a j)))^2-1)| at hn
    linarith [lt_of_not_ge hn]

#print axioms finite_symbol_tests

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
